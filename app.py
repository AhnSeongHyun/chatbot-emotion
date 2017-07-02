# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from lang_detect import LanguageDetection
from sentiment import Sentiment
from config import conf
from flask import Flask, request, jsonify
from message import Message

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def get_text():
    try:
        user_msg = request.form.get('user_msg', None)
        message = Message()
        print(user_msg)
        if user_msg:

            lang_detect = LanguageDetection(**conf)
            request_id = datetime.now().strftime('%Y%m%d%H%M%S')
            lang_detect_result = lang_detect.detect_language(id=request_id, text=user_msg)
            message.append({'text': "%s 로 말씀하셨습니다. " % lang_detect_result.name})

            if lang_detect_result.lang_code in conf['approval_lang_code']:
                sentiment = Sentiment(**conf)
                sentiment_score = sentiment.detect_sentiment(id=request_id,
                                                             text=user_msg,
                                                             language=lang_detect_result.lang_code)
                message.append({'text': sentiment_score.get_sentiment_text()})
            else:
                message.append({'text': '해당언어로는 제가 기분을 알 수 없습니다.'})
                message.append({'text': '%s 언어로 이야기 해주세요.' % (conf.conf['approval_lang_code'].values())})
        return jsonify(message.to_dict()), 200
    except Exception:
        import traceback
        print(traceback.format_exc())
        d = {
            "messages": [
                {"text": "알아들을수가 없습니다. 다른애기를 해주세요."}
            ]
        }
        return jsonify(d), 200






