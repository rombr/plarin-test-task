#!/usr/bin/env bash
#Set environment variable APP=actions to run another app from one base image, you can add more that one conditions, for run multiple containers from one entrypoint
set -e

role=${APP:-app}

if [ "$role" = "app" ]; then
    uvicorn main:app --host 0.0.0.0 --port 8000

else
    echo "Could not match the container role \"$role\""
    exit 1
fi