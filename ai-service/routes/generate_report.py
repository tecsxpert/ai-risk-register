# I am the /generate-report endpoint. I produce a structured executive risk report from risk register data.
import json
import logging
import time
import threading
from flask import Blueprint, request, jsonify, Response, stream_with_context
from datetime import datetime, timezone
from services.groq_client import call_groq, stream_groq
from services.ai_cache import get_cached, set_cached
from services.response_builder import build_meta, estimate_tokens
from services.job_queue import create_job, get_job, update_job_status, notify_webhook, JobStatus

logger = logging.getLogger(__name__)
generate_report_bp = Blueprint('generate_report', __name__)

# I've defined this fallback report in case my Groq service is unavailable.
FALLBACK_REPORT = {
    "title": "AI Risk Register Report — Service Unavailable",
    "executive_summary": "The AI report generation service is temporarily unavailable.",
    "overview": "Report generation could not be completed. Manual review of risk items is recommended.",
    "top_items": [
        {"rank": 1, "name": "N/A", "category": "N/A", "severity": "N/A", "rationale": "AI service unavailable."}
    ],
    "recommendations": [
        {"priority": "IMMEDIATE", "action": "Retry report generation later.", "owner": "Risk Manager"}
    ]
}


def _load_prompt_template() -> str:
    # I'm loading my report prompt from the prompts directory.
    try:
        with open('prompts/generate_report_prompt.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error("I couldn't find prompts/generate_report_prompt.txt.")
        return ""


@generate_report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    # I'm handling the full JSON report generation here.
    data = request.get_json(silent=True)
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "I need a 'text' field to generate a report."}), 400

    input_text = data["text"].strip()

    # I'm checking my cache first to see if I've already generated this report.
    cached_response = get_cached("generate_report", input_text)
    if cached_response is not None:
        logger.info("I've served the POST /generate-report from my Redis cache.")
        return jsonify(cached_response), 200

    template = _load_prompt_template()
    if not template:
        return jsonify({**FALLBACK_REPORT, "is_fallback": True}), 200

    prompt = template.replace("{input_text}", input_text)
    messages = [{"role": "user", "content": prompt}]

    # I hit a cache miss, so I'm calling Groq now.
    start_time = time.time()
    raw_response = call_groq(messages, temperature=0.4, max_tokens=1000)
    response_time_ms = (time.time() - start_time) * 1000
    ts = datetime.now(timezone.utc).isoformat()

    if raw_response is None:
        return jsonify({**FALLBACK_REPORT, "generated_at": ts, "is_fallback": True}), 200

    try:
        # I'm cleaning up the response from Groq to ensure it's valid JSON.
        clean = raw_response.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        parsed = json.loads(clean)
        
        response_body = {
            **parsed,
            "generated_at": ts,
            "is_fallback": False,
            "meta": build_meta(
                response_time_ms=response_time_ms,
                cached=False,
                confidence=0.9,
                tokens_used=estimate_tokens(raw_response)
            )
        }

        # I'm storing the successful report in my cache for future use.
        set_cached("generate_report", input_text, response_body)
        return jsonify(response_body), 200

    except Exception as e:
        logger.error(f"I failed to parse the Groq report JSON: {e}")
        return jsonify({**FALLBACK_REPORT, "generated_at": ts, "is_fallback": True}), 200


@generate_report_bp.route('/generate-report/async', methods=['POST'])
def generate_report_async():
    """
    I'm starting an async report generation job here. I return a job_id immediately.
    Request body: {"text": "risk data", "webhook_url": "https://... (optional)"}
    Response: {"job_id": "uuid", "status": "PENDING", "poll_url": "/generate-report/status/{job_id}"}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "I need a JSON request body with a 'text' field."}), 400

    input_text = data.get("text", "").strip()
    if not input_text:
        return jsonify({"error": "My 'text' field is required and must not be empty."}), 400

    if len(input_text) > 10000:
        return jsonify({"error": "My 'text' field must not exceed 10000 characters."}), 400

    webhook_url = data.get("webhook_url", "").strip()

    # I'm creating the job and starting my background thread immediately.
    job_id = create_job()
    logger.info(f"I've created an async report job: {job_id}. Starting my background thread.")

    def run_report_job():
        """My background thread: runs my report generation and updates my job status."""
        update_job_status(job_id, JobStatus.PROCESSING)
        try:
            template = _load_prompt_template()
            if not template:
                update_job_status(job_id, JobStatus.FAILED, error="I couldn't find my prompt template.")
                return

            prompt = template.replace("{input_text}", input_text)
            messages = [{"role": "user", "content": prompt}]

            raw_response = call_groq(messages, temperature=0.4, max_tokens=1000)

            if raw_response is None:
                # I'm returning a fallback report — I never set FAILED for Groq errors.
                fallback = {**FALLBACK_REPORT,
                            "generated_at": datetime.now(timezone.utc).isoformat(),
                            "is_fallback": True}
                update_job_status(job_id, JobStatus.COMPLETED, result=fallback)
                notify_webhook(webhook_url, job_id, fallback)
                return

            try:
                clean = raw_response.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
                parsed = json.loads(clean)
                required_keys = {"title", "executive_summary", "overview", "top_items", "recommendations"}
                if required_keys - set(parsed.keys()):
                    raise ValueError("I'm missing some required report keys in the AI response.")
                parsed["generated_at"] = datetime.now(timezone.utc).isoformat()
                parsed["is_fallback"] = False
                update_job_status(job_id, JobStatus.COMPLETED, result=parsed)
                notify_webhook(webhook_url, job_id, parsed)

            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"I encountered a parse error for job {job_id}: {e}")
                fallback = {**FALLBACK_REPORT,
                            "generated_at": datetime.now(timezone.utc).isoformat(),
                            "is_fallback": True}
                update_job_status(job_id, JobStatus.COMPLETED, result=fallback)
                notify_webhook(webhook_url, job_id, fallback)

        except Exception as e:
            logger.error(f"My background thread for job {job_id} failed: {e}")
            update_job_status(job_id, JobStatus.FAILED, error=str(e))

    thread = threading.Thread(target=run_report_job, daemon=True)
    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": JobStatus.PENDING,
        "poll_url": f"/generate-report/status/{job_id}"
    }), 202


@generate_report_bp.route('/generate-report/status/<job_id>', methods=['GET'])
def get_report_status(job_id: str):
    """
    I use this to poll the status of my async report generation job.
    """
    if not job_id or not job_id.strip():
        return jsonify({"error": "I need a valid job_id."}), 400

    job = get_job(job_id)
    if job is None:
        return jsonify({"error": f"I couldn't find job '{job_id}'."}), 404

    return jsonify(job), 200


@generate_report_bp.route('/generate-report/stream', methods=['POST'])
def generate_report_stream():
    """
    I've added this SSE streaming version of /generate-report.
    I return raw text chunks as they are generated by my model.
    Note: I've decided NOT to cache streaming responses to keep things simple.
    """
    data = request.get_json(silent=True)
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "I need a 'text' field to start streaming."}), 400

    input_text = data["text"].strip()
    template = _load_prompt_template()
    if not template:
        return jsonify({"error": "My prompt template is missing."}), 500

    prompt = template.replace("{input_text}", input_text)
    messages = [{"role": "user", "content": prompt}]

    @stream_with_context
    def generate():
        logger.info("I'm starting an SSE stream for /generate-report/stream.")
        yield "data: [START]\n\n"
        for chunk in stream_groq(messages):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')

