import json
from schemas.notification import Notification
from core.redis_client import redis_client
from core.websocket_manager import active_connections

async def create_and_send_notification(notification: Notification):
    notification_json = notification.json()
    await redis_client.publish(f"user:{notification.user_id}", notification_json)

    if notification.user_id in active_connections:
        await active_connections[notification.user_id].send_text(notification_json)