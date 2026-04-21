# Bug Fix Log

This document tracks all issues discovered and resolved during development.

---

## 1. Redis connection failure (Worker)

* **File:** `worker/worker.py`
* **Line:** ~6
* **Issue:** Used `localhost` instead of Docker service name
* **Fix:**

```python
host=os.getenv("REDIS_HOST", "redis")
```

---

## 2. Queue name mismatch

* **File:** `api/main.py`, `worker/worker.py`
* **Line:** ~25 / ~15
* **Issue:** API used `"jobs"` while worker used `"job"`
* **Fix:** Standardized to `"jobs"` across all services

---

## 3. `.decode()` crash in worker

* **File:** `worker/worker.py`
* **Line:** ~20
* **Issue:** `.decode()` used with `decode_responses=True`
* **Fix:**

```python
process_job(job_id)
```

---

## 4. Trivy image scan failure

* **File:** `.github/workflows/ci-cd.yml`
* **Issue:** Scanned `api:latest` instead of registry image
* **Fix:**

```bash
trivy image localhost:5000/api:latest
```

---

## 5. Lint failures (E302)

* **File:** `api/main.py`, `api/test_api.py`
* **Issue:** Missing blank lines before functions
* **Fix:** Added proper spacing (PEP8 compliance)

---

## 6. Unused import in tests

* **File:** `api/test_api.py`
* **Issue:** `pytest` imported but unused
* **Fix:** Removed unused import

---

## 7. Worker startup race condition

* **File:** `worker/worker.py`
* **Issue:** Worker attempted Redis connection before readiness
* **Fix:** Added retry loop with `r.ping()`

---

## 8. Missing health checks

* **Files:** API, frontend, Dockerfiles
* **Issue:** No health endpoints
* **Fix:** Added `/health` endpoints and Docker HEALTHCHECK

---

## 9. Hardcoded configuration

* **Files:** API, worker, frontend
* **Issue:** Hardcoded Redis/API URLs
* **Fix:** Replaced with environment variables

---

## 10. Missing restart policy

* **File:** `docker-compose.yml`
* **Issue:** Worker did not restart after crash
* **Fix:**

```yaml
restart: always
```

---

## Summary

All issues were resolved with:

* Environment-based configuration
* Consistent naming
* Proper container networking
* CI/CD validation
* Lint and security enforcement

---
