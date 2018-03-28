# https://codereview.stackexchange.com/questions/147731/simple-rest-api-using-python-with-falcon
import falcon
from .readWriteJson import ReadWriteJson
from .resources import *

storage = ReadWriteJson()

api = application = falcon.API()
api.add_route('/tests/archive/', TestsResource(storage))
api.add_route('/tests/archive/{id}', TestFromTestsResource(storage))
api.add_route('/test/running', RunningTestResource(storage))
api.add_route('/test/done/{id}', TestDoneResource(storage))
