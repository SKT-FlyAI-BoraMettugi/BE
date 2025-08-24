import json
from fastapi import Request
from sqlalchemy.orm import Session
from schemas.comment import CommentCreate
from schemas.notification import NotificationCreate
from crud.comment import get_comment
from crud.discussion import get_discussion
from crud.notification import create_notification
from crud.user import get_user_info

async def like_discussion_notification(user_id: int, discussion_id: int, request: Request, db: Session):
    discussion = get_discussion(db, discussion_id)
    like_user = get_user_info(user_id, db)
    content = f"{like_user.nickname}님이 회원님의 토론에 좋아요를 눌렀습니다."
    notification_data = NotificationCreate(
        user_id = discussion.user_id,
        discussion_id = discussion_id,
        content = content
    )
    notification = create_notification(db, notification_data)

    redis = request.app.state.redis
    channel = f"user:{discussion.user_id}"
    message = {
        "type": "like_discussion", 
        "discussion_id": discussion_id, 
        "user_id": user_id, 
        "nickname": like_user.nickname,
        "content": content,
    }
    try:
        await redis.publish(channel, json.dumps(message))
    except Exception as e:
        print(f"Notification error: {e}")
    

async def post_comment_notification(user_id: int, discussion_id: int, comment_data: CommentCreate, request: Request, db: Session):
    discussion = get_discussion(db, discussion_id)
    comment_user = get_user_info(user_id, db)
    content = f"{comment_user.nickname}님이 회원님의 토론에 답글을 달았습니다."
    notification_data = NotificationCreate(
        user_id = discussion.user_id,
        discussion_id = discussion_id,
        content = content
    )
    notification = create_notification(db, notification_data)
    
    redis = request.app.state.redis
    channel = f"user:{discussion.user_id}"
    message = {
        "type": "post_comment", 
        "discussion_id": discussion_id, 
        "user_id": user_id, 
        "nickname": comment_user.nickname,
        "content": content,
        "comment": comment_data.content,
    }
    try:
        await redis.publish(channel, json.dumps(message))
    except Exception as e:
        print(f"Notification error: {e}")

async def like_comment_notification(comment_id: int, user_id: int, request: Request, db: Session):
    comment = get_comment(db, comment_id)
    like_user = get_user_info(user_id, db)    
    content = f"{like_user.nickname}님이 회원님의 답글에 좋아요를 눌렀습니다."
    notification_data = NotificationCreate(
        user_id = comment.user_id,
        comment_id = comment_id,
        content = content
    )
    notification = create_notification(db, notification_data)

    redis = request.app.state.redis
    channel = f"user:{comment.user_id}"
    message = {
        "type": "like_comment", 
        "comment_id": comment_id, 
        "user_id": user_id, 
        "nickname": like_user.nickname,
        "content": content,
    }   
    try:
        await redis.publish(channel, json.dumps(message))
    except Exception as e:
        print(f"Notification error: {e}")