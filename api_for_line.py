from linebot.models import TextSendMessage
from linebot import LineBotApi
from flask import Flask, request, abort

from app.app_for_chat import chat

line_access_token = "Channel access token"
line_bot_api = LineBotApi(line_access_token)

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world book", 200


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        payload = request.json

        print(payload)
        reply_token = payload['events'][0]['replyToken']
        print(reply_token)
        msg = payload['events'][0]['message']['text']
        print("message")
        reply_msg = chat(msg)
        print(reply_msg)
        reply_obj = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(reply_token, reply_obj)
        return "", 200
    elif request.method == "GET":
        return "this is method GET", 200

    else:
        abort(400)


if __name__ == '__main__':
    app.run(port=200)
