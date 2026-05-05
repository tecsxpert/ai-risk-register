# I am the /batch-process endpoint. I process up to 20 risk items through describe and categorise,
# with a 100ms delay between items to respect Groq rate limits.
import time
import json
import logging
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
from services.ai_cache import get_cached, set_cached
from services.response_builder import build_meta, estimate_tokens

logger = logging.getLogger(__name__)
batch_process_bp = Blueprint('batch_process', __name__)

MAX_BATCH_SIZE = 20
INTER_ITEM_DELAY_SECONDS = 0.1  # 100ms per spec

# I've defined this fallback for a single item when Groq fails mid-batch.
def _fallback_item_result(item_text: str, index: int) -> dict:
    return {
        "index": index,
        "input": item_text[:200],
        "description": "AI description unavailable — manual review required.",
        "category": "OPERATIONAL",
        "confidence": 0.0,
        "is_fallback": True,
        "meta": build_meta(0.0, False, 0.0, 0)
    }


def _load_prompt(filename: str) -> str:
    """I'm loading a prompt template from my prompts directory."""
    try:
        with open(f'prompts/{filename}', 'r') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"I couldn't find my prompt file: prompts/{filename}")
        return ""


@batch_process_bp.route('/batch-process', methods=['POST'])
def batch_process():
    """
    I process up to 20 risk items through describe and categorise.
    Request body: {"items": ["risk text 1", "risk text 2", ...]}
    Response: {"results": [...], "total": N, "processed": N, "failed": N, "generated_at": "..."}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "I need a JSON request body with an 'items' array."}), 400

    items = data.get("items")
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "My 'items' field must be a non-empty array of strings."}), 400

    if len(items) > MAX_BATCH_SIZE:
        return jsonify({
            "error": f"My batch size exceeds the maximum of {MAX_BATCH_SIZE} items. I received {len(items)}."
        }), 400

    # I'm validating that all items are non-empty strings before I start processing.
    for i, item in enumerate(items):
        if not isinstance(item, str) or not item.strip():
            return jsonify({"error": f"Item at index {i} must be a non-empty string."}), 400

    describe_template = _load_prompt("describe_prompt.txt")
    categorise_template = _load_prompt("categorise_prompt.txt")

    results = []
    processed = 0
    failed = 0

    logger.info(f"I'm starting a batch process for {len(items)} items.")

    for index, item_text in enumerate(items):
        item_text = item_text.strip()
        item_start = time.time()

        # Step 1: I check my cache for describe.
        cached_describe = get_cached("describe", item_text)
        if cached_describe:
            desc_dict = cached_describe
            desc_from_cache = True
        else:
            desc_from_cache = False
            desc_dict = call_groq('describe', item_text, temperature=0.3, max_tokens=300)

        # Step 2: I check my cache for categorise.
        cached_cat = get_cached("categorise", item_text)
        if cached_cat:
            cat_dict = cached_cat
            cat_from_cache = True
        else:
            cat_from_cache = False
            cat_dict = call_groq('categorise', item_text, temperature=0.1, max_tokens=150)

        item_time_ms = round((time.time() - item_start) * 1000, 1)
        
        # If describe failed, the whole item is a fallback.
        if not desc_dict:
            failed += 1
            result = _fallback_item_result(item_text, index)
        else:
            processed += 1
            
            # Extract fields from desc_dict (could be from cache or fresh)
            # Note: cached_describe stores the whole response body (including meta), 
            # while call_groq returns the parsed JSON dict from the prompt.
            description_text = desc_dict.get("description", "AI description unavailable.")
            
            # Extract fields from cat_dict
            category = "OPERATIONAL"
            confidence = 0.0
            if cat_dict:
                category = cat_dict.get("category", "OPERATIONAL").upper()
                confidence = float(cat_dict.get("confidence", 0.0))

            result = {
                "index": index,
                "input": item_text[:200],
                "description": description_text,
                "category": category,
                "confidence": round(min(max(confidence, 0.0), 1.0), 2),
                "is_fallback": False,
                "meta": build_meta(
                    response_time_ms=item_time_ms,
                    cached=(desc_from_cache and cat_from_cache),
                    confidence=confidence,
                    tokens_used=estimate_tokens(description_text)
                )
            }

            # I cache the describe result if it was a fresh hit.
            if not desc_from_cache and desc_dict:
                set_cached("describe", item_text, {
                    **desc_dict,
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "is_fallback": False
                })
            
            if not cat_from_cache and cat_dict:
                set_cached("categorise", item_text, {
                    **cat_dict,
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "is_fallback": False
                })

        results.append(result)
        logger.info(f"I've processed batch item {index + 1}/{len(items)}. Time: {item_time_ms}ms. Fallback: {not bool(desc_dict)}.")

        # I wait 100ms between items as per my spec — but I skip the delay after the last item.
        if index < len(items) - 1:
            time.sleep(INTER_ITEM_DELAY_SECONDS)

    return jsonify({
        "results": results,
        "total": len(items),
        "processed": processed,
        "failed": failed,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }), 200
