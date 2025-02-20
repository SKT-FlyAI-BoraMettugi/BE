from fastapi import APIRouter, Depends, BackgroundTasks, WebSocket
from sqlalchemy.orm import Session
from database.nolly import get_db
from schemas.notification import Notification
from core.notification import create_and_send_notification

router = APIRouter()

@router.post("/{comment_id}")
async def create_notification(notification: Notification, backgroundtasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 여기에 알림 생성 로직 추가 (예: DB에 저장)

    # 백그라운드에서 알림 전송
    backgroundtasks.add_task(create_and_send_notification, notification)

    return {"status": "Notification created and sent"}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await connect_websocket(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 필요한 경우 여기서 클라이언트로부터의 메시지 처리
    except WebSocketDisconnect:
        await disconnect_websocket(user_id)