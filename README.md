# Distributed Job Processing System (DevOps Stage 2)

This project implements a distributed system consisting of:

* **Frontend (Express)** – submits jobs and checks status
* **API (FastAPI)** – queues jobs in Redis
* **Worker (Python)** – processes jobs asynchronously
* **Redis** – acts as a message queue and state store

All services are containerized and orchestrated using Docker Compose, with a full CI/CD pipeline via GitHub Actions.

---

## Architecture

```
Frontend → API → Redis Queue → Worker → Redis (status update)
```

---

## Prerequisites

Ensure the following are installed on your machine:

* Docker (v24+)
* Docker Compose (v2+)
* Git

Verify:

```bash
docker --version
docker compose version
git --version
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

---

### 2. Create environment file

```bash
cp .env.example .env
```

Edit `.env` if needed.

---

### 3. Build and start the system

```bash
docker compose up --build
```

---

## Access the application

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:3000 |
| API      | http://localhost:8000 |

---

## Test the system

### Submit a job

```bash
curl -X POST http://localhost:8000/jobs
```

Response:

```json
{ "job_id": "..." }
```

---

### Check job status

```bash
curl http://localhost:8000/jobs/<job_id>
```

Expected flow:

```json
{ "status": "queued" }
→
{ "status": "completed" }
```

---

## What successful startup looks like

### API logs

```
Connected to Redis
Uvicorn running on http://0.0.0.0:8000
```

### Worker logs

```
Processing job ...
Done: ...
```

### Redis logs

```
Ready to accept connections
```

---

## Stop the system

```bash
docker compose down
```

---

## CI/CD Pipeline

The pipeline runs on GitHub Actions with the following stages:

```
lint → test → build → security scan → integration test → deploy
```

### Key features:

* Linting (flake8, eslint, hadolint)
* Unit tests with coverage
* Docker image build + local registry push
* Security scanning with Trivy
* Full-stack integration testing
* Rolling deployment with health checks

---

## Security Notes

* No secrets are stored in the repository
* `.env` is excluded via `.gitignore`
* Images run as non-root users
* Redis is not exposed publicly

---

## Notes

* This project is designed to run locally and in CI (no cloud required)
* All configuration is environment-driven
* Fully reproducible setup

---
