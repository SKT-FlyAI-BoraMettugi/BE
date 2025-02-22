import asyncio
from core.redis_client import redis_client
from core.websocket_manager import active_connections


async def redis_subscriber():
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("user:*")

    while True:
        try:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                channel = message["channel"].decode()
                user_id = int(channel.split(":")[1])
                if user_id in active_connections:
                    await active_connections[user_id].send_text(message["data"].decode())
        except Exception as e:
            print(f"Error in redis subscriber: {e}")
            await asyncio.sleep(1)


def start_redis_subscriber():
    asyncio.create_task(redis_subscriber())
