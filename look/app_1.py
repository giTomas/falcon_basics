import falcon

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

api = application = falcon.API()
api.add_route('/quote', QuoteResource())
api.add_route('/sayHello', HelloResource())