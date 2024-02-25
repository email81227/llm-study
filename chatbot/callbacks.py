
import hashlib
import uuid

from langfuse.callback import CallbackHandler as LangFuseCallbackHandler

from chatbot.config import settings


def get_langfuse_callback(session_id: str = None, user_id: str = None):
    callback = LangFuseCallbackHandler(
        settings.LANGFUSE_PUBLIC_KEY,
        settings.LANGFUSE_SECRET_KEY
    )

    if user_id is None:
        user_id = settings.USER_EMAIL.split("@")[0]

    if session_id is None:
        session_id = uuid.uuid1()

    setattr(callback, 'session_id', session_id)
    setattr(callback, 'user_id', user_id)

    return callback
