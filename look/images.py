import json
import falcon
import msgpack

class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

class HelloResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        msg = {
            'msg': 'Hello!'
        }

        resp.media = msg

class Resource(object):
    def on_get(self, req, resp):
        doc = {
            'images': [
                {
                    'href': '/images/abc.png'
                }
            ]
        }

        # resp.body = json.dumps(doc, ensure_ascii=False)
        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200
