# I am a simple in-memory job queue for my async report generation.
# Each job I manage has a unique ID, status, and result. I use background threads to update my job states.
import uuid
import threading
import logging
import requests
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# I'm using this in-memory job store, keyed by job_id.
# Format: {job_id: {"status": JobStatus, "result": dict|None, "error": str|None, "created_at": str}}
_jobs: dict = {}
_jobs_lock = threading.Lock()


def create_job() -> str:
    """
    I create a new job entry with a PENDING status.
    I return the unique job_id string.
    """
    job_id = str(uuid.uuid4())
    with _jobs_lock:
        _jobs[job_id] = {
            "job_id": job_id,
            "status": JobStatus.PENDING,
            "result": None,
            "error": None,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    logger.info(f"I've created a new job: {job_id}")
    return job_id


def get_job(job_id: str) -> dict | None:
    """
    I retrieve a job by its ID.
    I return the job dict or None if I can't find it.
    """
    with _jobs_lock:
        return _jobs.get(job_id)


def update_job_status(job_id: str, status: JobStatus, result: dict = None, error: str = None) -> None:
    """
    I update the status, result, and/or error for a specific job.
    """
    with _jobs_lock:
        if job_id not in _jobs:
            logger.error(f"I was asked to update an unknown job_id: {job_id}")
            return
        _jobs[job_id]["status"] = status
        if result is not None:
            _jobs[job_id]["result"] = result
        if error is not None:
            _jobs[job_id]["error"] = error
        _jobs[job_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    logger.info(f"I've updated job {job_id} to status: {status}")


import urllib.parse
import ipaddress
import socket

def is_safe_url(url: str) -> bool:
    """
    I perform basic SSRF validation on my webhook URLs.
    I ensure they use HTTPS and don't point to private or loopback IP ranges.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https":
            logger.warning(f"I'm blocking a non-HTTPS webhook URL: {url}")
            return False
        
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Resolve hostname to IP to check for private ranges
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        
        if ip_obj.is_private or ip_obj.is_loopback:
            logger.warning(f"I'm blocking a webhook URL pointing to a private/loopback IP: {url} ({ip})")
            return False
            
        return True
    except Exception as e:
        logger.error(f"I encountered an error during webhook URL validation: {e}")
        return False


def notify_webhook(webhook_url: str, job_id: str, result: dict) -> None:
    """
    I POST the completed job result to the provided webhook URL.
    I fail silently here — my webhook notification is best-effort only.
    """
    if not webhook_url:
        return
    
    # I'm validating the URL to prevent SSRF attacks.
    if not is_safe_url(webhook_url):
        logger.error(f"I'm skipping the webhook for job {job_id} because the URL failed my safety checks.")
        return

    try:
        payload = {"job_id": job_id, "status": JobStatus.COMPLETED, "result": result}
        response = requests.post(webhook_url, json=payload, timeout=10)
        logger.info(f"I've delivered the webhook for job {job_id}. Status: {response.status_code}.")
    except Exception as e:
        logger.warning(f"My webhook call failed for job {job_id}: {e}. I'm continuing without notification.")
