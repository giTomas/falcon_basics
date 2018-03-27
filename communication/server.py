# https://codereview.stackexchange.com/questions/147731/simple-rest-api-using-python-with-falcon
import falcon
import json
import os
import os.path as path
from .readWriteJson import ReadWriteJson

# absPath = path.dirname(path.abspath(__file__))
# archiveDir = 'archive'
# runningDir = 'running'
# pathToArchive = path.join(absPath, archiveDir)
# pathToRunning = path.join(absPath, runningDir)

# if path.isdir(pathToArchive):
# 	print('Directory archive  exists')
# else:
# 	print('create directory {}'.format(pathToArchive))
# 	os.makedirs(pathToArchive, exist_ok=True)
#
# if path.isdir(pathToRunning):
# 	print('Directory running exists')
# else:
# 	print('create directory {}'.format(pathToRunning))
# 	os.makedirs(pathToRunning, exist_ok=True)
#
# running_test_file = '{}/running.json'.format(pathToRunning, 'running')
# with open(running_test_file, 'w') as f:
# 	json.dump({'status': 'none', 'id': 'none'}, f)
#
# def listUrls(archivePath=pathToArchive):
# 	jsonfiles = [f for f in os.listdir(archivePath) if path.isfile(path.join(archivePath, f))]
# 	ids 	  = [path.splitext(f)[0] for f in jsonfiles]
# 	urls      = [path.join('tests', f) for f in ids]
# 	return urls

storage = ReadWriteJson()

#####

class RunningTestResource:
	def on_post(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')
		storage.writeToRunning(req.media)
		print('Running test updated {}'.format(req.media))

	def on_get(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')
		resp.body = storage.readFromRunning
		resp.status = falcon.HTTP_200
		print('Sent data - running test')

class RunningTestDoneResource:
	def on_post(self, req, resp, id):
		resp.set_header('Access-Control-Allow-Origin', '*')
		storage.setRunningNone()
		print('Test done - remove running')
		storage.writeToArchive(req.media, id)
		print('Test done - added to archive')

class TestsResource:
	def on_get(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')
		resp.status = falcon.HTTP_200
		resp.body = storage.listArchive()
		print('Sent data - all tests from archive')

class TestFromTestsResource:
	def on_get(self, req, resp, id):
		resp.set_header('Access-Control-Allow-Origin', '*')
		resp.status = falcon.HTTP_200
		resp.body = storage.readFromArchive(id)
		print('Sent data - test {}'.format(id))

api = application = falcon.API()
api.add_route('/tests/archive/', TestsResource())
api.add_route('/tests/archive/{id}', TestFromTestsResource())
api.add_route('/test/running', RunningTestResource())
api.add_route('/test/done/{id}', RunningTestDoneResource())
