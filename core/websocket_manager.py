from fastapi import WebSocket

active_connections = {}

async def connect_websocket(user_id: int, websocket: WebSocket):
    await websocket.accept()
    active_connections[user_id] = websocket

async def disconnect_websocket(user_id: int):
    if user_id in active_connections:
        del active_connections[user_id]
