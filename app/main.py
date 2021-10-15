from typing import List
from pydantic import BaseModel

from fastapi import FastAPI
from linebot.models import TextSendMessage
from linebot import LineBotApi

from chatbot.app_for_chat import chat

line_access_token = "doophzmTYAIB8/IYooSiQSFyP09sKbchX/Q0x/p7NCuR3dfVEWaCvBLMTM9sqJINCD7fP8wLrpDgozvHKzAhgzP3JxtKQXeBNH/eBERP2qDi5IBoarjV/zZ4RqOcrL9/w07mfr8Pxz2z00uvqtV+XwdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(line_access_token)
app = FastAPI()


class Message(BaseModel):
    type: str
    id: str
    text: str


class Source(BaseModel):
    type: str
    userId: str


class Event(BaseModel):
    type: str
    message: Message
    timestamp: int
    source: Source
    replyToken: str
    mode: str


class Model(BaseModel):
    destination: str
    events: List[Event]


@app.get('/')
async def root():
    return "Hello, world!"


@app.post("/webhook", status_code=200)
def webhook(inp: Model):
    reply_token = inp.events[0].replyToken
    print(reply_token)

    msg = inp.events[0].message.text
    print("message")

    reply_msg = chat(msg)
    print(reply_msg)

    reply_obj = TextSendMessage(text=reply_msg)
    line_bot_api.reply_message(reply_token, reply_obj)
    return ""
