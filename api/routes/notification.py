import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# WebSocket 연결
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    redis = websocket.app.state.redis
    await websocket.accept()

    pubsub = redis.pubsub()
    await pubsub.subscribe(f"user:{user_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    await websocket.send_text(json.dumps(data, ensure_ascii=False))
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: user={user_id}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await pubsub.unsubscribe(f"user:{user_id}")
        await pubsub.close()