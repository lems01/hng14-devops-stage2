#!/bin/bash
set -e

JOB_ID=$(curl -s -X POST http://localhost:8000/jobs | jq -r .job_id)

for i in {1..10}; do
  STATUS=$(curl -s http://localhost:8000/jobs/$JOB_ID | jq -r .status)
  if [ "$STATUS" = "completed" ]; then
    echo "Success"
    exit 0
  fi
  sleep 2
done

echo "Failed"
exit 1
