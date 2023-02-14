from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import random
# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    words = ['早安~你好，今天好嗎？', '早安 你好～～',
             'Good Morning!!', 'Bojour!!', '快中午了，肚子好餓']
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    text = event.message.text
                    if '電影' in text or 'movie' in text:
                        message = 'https://movies.yahoo.com.tw/chart.html'
                    elif '台北捷運' in text:
                        message = 'https://kuopoting.github.io/k1/'
                    elif '高雄捷運' in text:
                        message = 'https://assets.piliapp.com/s3pxy/mrt_taiwan/kaohsiung/202210_zh.png'
                    elif '早安' in text:
                        message = random.choice(words)
                    elif '樂透' in text or 'lotto' in text:
                        message = lotto()
                    else:
                        message = text
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=message)
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='無法辨識！')
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def lotto():
    numbers = sorted(random.sample(range(1, 50), 6))
    result = ' '.join(map(str, numbers))
    n = random.randint(1, 50)
    return f'{result} 特別號為： {n}'
