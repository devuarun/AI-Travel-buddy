import json
import logging
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import JSONResponse
from .schemas import SearchQuery, ReserveRequest, PaymentRequest
from orchestrator import SimpleAgentSystem
import uvicorn

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s - %(message)s')
logger = logging.getLogger("backend")

app = FastAPI(title="Travel Multi-Agent Orchestrator")
agent_system = SimpleAgentSystem()

# Simple in-memory session tracking
sessions = {}  # session_id -> websocket

@app.post('/start-booking')
async def start_booking(query: SearchQuery):
    # In a production system, you'd return a task id and require client to connect via WS.
    return JSONResponse({"task": "started", "message": "Connect to WebSocket /ws/booking for streaming results"})

@app.websocket('/ws/booking')
async def ws_booking(websocket: WebSocket):
    await websocket.accept()
    logger.info('WebSocket client connected')
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
            except Exception:
                await websocket.send_text(json.dumps({"error": "invalid_json"}))
                continue
            action = payload.get('action')
            if action == 'search':
                query = payload.get('query')
                # define a send helper
                async def client_send(obj):
                    await websocket.send_text(json.dumps(obj))
                # run discovery
                await agent_system.discovery_flow(query, client_send)
            elif action == 'reserve':
                option_id = payload.get('option_id')
                pax = payload.get('pax', {})
                async def client_send(obj):
                    await websocket.send_text(json.dumps(obj))
                await agent_system.reserve_tentative(option_id, pax, client_send)
            elif action == 'pay':
                tentative_id = payload.get('tentative_id')
                payment_info = payload.get('payment_info', {})
                async def client_send(obj):
                    await websocket.send_text(json.dumps(obj))
                await agent_system.process_payment_and_confirm(tentative_id, payment_info, client_send)
            else:
                await websocket.send_text(json.dumps({"error": "unknown action"}))
    except WebSocketDisconnect:
        logger.info('WebSocket disconnected')
    except Exception as e:
        logger.exception('WebSocket error: %s', e)

if __name__ == '__main__':
    uvicorn.run('backend.api.main:app', host='0.0.0.0', port=8000, reload=True)
