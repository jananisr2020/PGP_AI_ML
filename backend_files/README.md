---
title: SuperKart Backend
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# SuperKart Sales Prediction - Backend API

Flask REST API serving the tuned XGBoost model for the SuperKart sales forecasting project.

- `GET /` - health check
- `POST /v1/predict` - online (single-record) inference
- `POST /v1/predictbatch` - batch inference from an uploaded CSV
