# travel-multiagent
A sample Travel Booking backend demonstrating a **multi-agent** architecture (PlannerAgent, AvailabilityAgent, ValidationAgent, BookingAgent, PaymentAgent) implemented in Python with a lightweight orchestrator. 

This repository is designed to be easy to import into GitHub. It provides:
- FastAPI backend with REST + WebSocket streaming
- In-memory session service (per-user sessions)
- Agent implementations (simple, illustrative)
- Detailed logging
- Dockerfile for running locally

This is **sample/demo code** and intentionally simple to show the multi-agent flow. Replace provider integrations with real APIs when moving to production.

## Quick start (local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for API docs. Use the WebSocket `/ws/booking` endpoint to stream search and booking progress.

## Files
- backend/: backend service with agents and orchestrator
- Dockerfile: simple dockerfile for the backend
