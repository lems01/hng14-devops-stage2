from fastapi import FastAPI, HTTPException
import redis
import uuid
import os
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

QUEUE_NAME = "jobs"

@app.on_event("startup")
def startup_event():
    try:
        r.ping()
        logger.info("Connected to Redis")
    except redis.exceptions.ConnectionError:
        raise RuntimeError("Redis is not available")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush(QUEUE_NAME, job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    logger.info(f"Job created: {job_id}")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
