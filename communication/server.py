# https://codereview.stackexchange.com/questions/147731/simple-rest-api-using-python-with-falcon
import falcon
import json
import os
import os.path as path

absPath = path.dirname(path.abspath(__file__))
archiveDir = 'archive'
runningDir = 'running'
pathToArchive = path.join(absPath, archiveDir)
pathToRunning = path.join(absPath, runningDir)


if path.isdir(pathToArchive):
	print('Directory archive  exists')
else:
	print('create directory {}'.format(pathToArchive))
	os.makedirs(pathToArchive, exist_ok=True)

if path.isdir(pathToRunning):
	print('Directory running exists')
else:
	print('create directory {}'.format(pathToRunning))
	os.makedirs(pathToRunning, exist_ok=True)

running_test_file = '{}/running.json'.format(pathToRunning, 'running')
with open(running_test_file, 'w') as f:
	json.dump({'status': 'none', 'id': 'none'}, f)

def isRunning(data):
	# data = json.loads(data)
	return data['status'] == 'running'

def listUrls(archivePath=pathToArchive):
	jsonfiles = [f for f in os.listdir(archivePath) if path.isfile(path.join(archivePath, f))]
	ids 	  = [path.splitext(f)[0] for f in jsonfiles]
	urls      = [path.join('tests', f) for f in ids]
	return urls

class RunningTestResource:
	running_test = dict({'status': 'none', 'id': 'none'})

	def on_post(self, req, resp):
		if isRunning(req.media):
			self.running_test = req.media
			print('Running test updated {}'.format(self.running_test))
		else:
			file_name = '{}/{}.json'.format(pathToArchive, self.running_test['id'])
			with open(file_name, 'w') as f:
				json.dump(self.running_test, f)
			self.running_test = dict({'status': 'none', 'id': 'none'})
			print('Test done - added to archive')

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(self.running_test, ensure_ascii=False)
		if isRunning(self.running_test):
			print('Sent data - running test')
		else:
			print('Sendt data - no running test')

class RunningTestResource2:
	def on_post(self, req, resp):
		with open(running_test_file, 'w') as f:
			json.dump(req.media, f)
		print('Running test updated {}'.format(req.media))

	def on_get(self, req, resp):
		with open(running_test_file, 'r') as f:
			data = json.load(f)
			resp.body = json.dumps(data, ensure_ascii=False)
		resp.status = falcon.HTTP_200
		print('Sent data - running test')

class RunningTestDoneResource:
	def on_post(self, req, resp, id):
		with open(running_test_file, 'w') as f:
			json.dump({'status': 'none', 'id': 'none'}, f)
		file_name = '{}/{}.json'.format(pathToArchive, id)
		print('Test done - remove running')
		with open(file_name, 'w') as f:
			json.dump(req.media, f)
		print('Test done - added to archive')

class TestsResource:
	def on_get(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')
		# print(resp.headers)
		resp.status = falcon.HTTP_200
		urls = listUrls()
		resp.body = json.dumps(urls, ensure_ascii=False)
		print('Sent data - all tests from archive')

class TestFromTestsResource:
	def on_get(self, req, resp, id):
		resp.status = falcon.HTTP_200
		testName = '{}/{}.json'.format(pathToArchive, id)
		with open(testName, 'r') as f:
			data = json.load(f)
			resp.body =json.dumps(data, ensure_ascii=False)
		print('Sent data - test {}'.format(id))

api = application = falcon.API()
api.add_route('/running-test', RunningTestResource())
api.add_route('/tests/archive/', TestsResource())
api.add_route('/tests/archive/{id}', TestFromTestsResource())
api.add_route('/test/running', RunningTestResource2())
api.add_route('/test/done/{id}', RunningTestDoneResource())
# tests/running/{id}
# tests/running/done/{id}
