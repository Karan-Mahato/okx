from fastapi import FastAPI
import socketio
import asyncio
from websocket_handler import orderbook_stream, handle_start_simulation, handle_disconnect  # Make sure this is defined

# Initialize Socket.IO server with proper CORS
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

sio.on("start_simulation")(handle_start_simulation)
sio.on("disconnect")(handle_disconnect)

app = FastAPI()

# Combine FastAPI and Socket.IO using ASGIApp
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Store for client configs (sid -> input)
client_configs = {}

# FastAPI route
@app.get("/")
async def root():
    return {"message": "Trade Simulator Backend Running"}

# Start orderbook stream on app startup
@app.on_event("startup")
async def start_orderbook_stream():
    asyncio.create_task(orderbook_stream(sio, client_configs))
