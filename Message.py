from pydantic import BaseModel, AnyUrl


class Msg(BaseModel):
    tg_chat_id: int
    tg_message_id: int
    user_msg: AnyUrl

