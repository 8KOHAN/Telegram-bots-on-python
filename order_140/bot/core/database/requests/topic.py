from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from core.database.models import Topic

async def save_topic(session, chat_id: int, topic_id: int):
    stmt = insert(Topic).values(chat_id=chat_id, topic_id=topic_id)

    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
