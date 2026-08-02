#!/bin/bash
set -e

docker network create superkart-net || true

cd backend_files
docker build -t superkart-backend .
docker rm -f superkart-backend 2>/dev/null || true
docker run -d --network superkart-net --name superkart-backend -p 7860:7860 superkart-backend

cd ../frontend_files
docker build -t superkart-frontend .
docker rm -f superkart-frontend 2>/dev/null || true
docker run -d --network superkart-net --name superkart-frontend \
    -e BACKEND_URL=http://superkart-backend:7860 -p 8501:8501 superkart-frontend
