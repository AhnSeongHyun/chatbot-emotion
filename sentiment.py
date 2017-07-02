# -*- coding:utf-8 -*-
import traceback
import requests
from attrdict import AttrDict
from requests import HTTPError
from urlparse import urljoin


class SentimentScore(object):
    def __init__(self, score):
        self.score = score

    def get_sentiment_text(self):
        if 0.0 <= self.score <= 0.2:
            return "기분이 나시군요."
        elif 0.2 <= self.score <= 0.4:
            return "기분이 별로시네요."
        elif 0.4 <= self.score <= 0.6:
            return "기분이 그저 그렇군요"
        elif 0.6 <= self.score <= 0.8:
            return "기분이 좋아보이네요 "
        else:
            return "기분이 매우 좋아보이네요"


class Sentiment(object):

    def __init__(self, **kwargs):
        self.api_key = kwargs['api_key']
        self.url = urljoin(kwargs['base_url'], "sentiment")

    def detect_sentiment(self,id, text, language='en'):

        try:
            if not self.url or not self.api_key:
                raise Exception('self.url or self.api_key is None')

            if id is not None and text:
                id = str(id)
                text = str(text)
            else:
                raise Exception('id and text is required')

            headers = {
                # Request headers
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            payload = {'documents':
                [
                    {'id': id,
                     'text': text,
                     "language": language
                     }

                ]
            }

            result = requests.post(self.url, headers=headers, json=payload)
            print result
            if result.status_code == 200:
                json_result = AttrDict(result.json())
                print json_result
                doc = json_result.documents[0]
                return SentimentScore(score=doc.score)

            else:
                raise HTTPError
        except Exception as e:
            print(traceback.format_exc())
            raise e

