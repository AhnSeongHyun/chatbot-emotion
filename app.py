# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from lang_detect import LanguageDetection
from sentiment import Sentiment
from config import conf
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def get_text():
    try:
        user_msg = request.form.get('user_msg', None)
        d = {
            "messages": [
                {"text": "기분이 어떠세요?"}
            ]
        }
        print(user_msg)
        if user_msg:

            lang_detect = LanguageDetection(**conf)
            request_id = datetime.now().strftime('%Y%m%d%H%M%S')
            lang, lang_code = lang_detect.detect_language(id=request_id, text=user_msg)
            print(lang)
            print(lang_code)
            d['messages'][0]['text'] = "%s 로 말씀하셨습니다. " % lang

            if lang_code in conf['approval_lang_code']:
                sentiment = Sentiment(**conf)
                sentiment_score = sentiment.detect_sentiment(id=request_id, text=user_msg, language=lang_code)
                d['messages'].append({'text': sentiment_score.get_sentiment_text()})
            else:
                d['messages'].append({'text': '해당언어로는 제가 기분을 알 수 없습니다.'})
                d['messages'].append({'text': '%s 언어로 이야기 해주세요.' % (conf.conf['approval_lang_code'].values())})
        return jsonify(d), 200
    except Exception:
        import traceback
        print(traceback.format_exc())
        d = {
            "messages": [
                {"text": "알아들을수가 없습니다. 다른애기를 해주세요."}
            ]
        }
        return jsonify(d), 200






