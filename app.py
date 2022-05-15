from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('vnuB8TsyvyjrlPPI6fk7XU8vuw3ZGLVDXYuYTmpcScSwGiw/6/hvTC5O82hPIMhY2WjQmPZBXL5B8OnXmX+WYSkbdHUs3DY7tVjPcPRDLG3Z+I+JcFAl59pmn/h+6AcPCRTibGWjdXAEmmXxrqQz3QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a0f2480fd9735408577c61ea51b81855')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
