---
title: SuperKart Frontend
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
---

# SuperKart Sales Prediction - Frontend

Streamlit app that calls the backend Space's Flask API to get online and batch sales predictions.
The backend URL is supplied to this Space via the `BACKEND_URL` Space variable (set automatically
by the deployment cell in the notebook), rather than being hardcoded.
