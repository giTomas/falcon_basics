# https://codereview.stackexchange.com/questions/147731/simple-rest-api-using-python-with-falcon
import falcon
import json
import pickle

import os 
import os.path as path

absPath = path.dirname(path.abspath(__file__))
testDir = 'archive'
pathToArchive = path.join(absPath, testDir)

if path.isdir(path.join(absPath, testDir)):
	print('Directory archive  exists')
else:
	print('create directory {}'.format(pathToArchive))
	os.makedirs(pathToArchive, exist_ok=True)

def isRunning(data):
	# data = json.loads(data)
	return data['status'] == 'running'

class RunningTestResource:
	running_test = dict({'status': 'none', 'id': 'none'})


	def on_post(self, req, resp):
		self.running_test = req.media
		if isRunning(req.media):
			print('updated {}'.format(self.running_test))
			self.running_test = req.media
		else:
			print('test done')
			file_name = '{}/{}.json'.format(pathToArchive, self.running_test['id'])
			with open(file_name, 'w') as f:
				json.dump(self.running_test, f)
			self.running_test = dict({'status': 'none', 'id': 'none'})		

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		if isRunning(self.running_test):
			resp.body = json.dumps(self.running_test,  ensure_ascii=False)
			print('Send data - running test')
		else:
			resp.body = json.dumps(self.running_test, ensure_ascii=False)	
			print('Send data - no running test')

class TestsResource:
	def on_get(self, req, resp):
		jsonfiles = [f for f in os.listdir(pathToArchive) if path.isfile(path.join(pathToArchive, f))]
		ids = [path.splitext(f)[0] for f in jsonfiles]
		urls = [path.join('tests', f) for f in ids]
		resp.status = falcon.HTTP_200
		resp.body = json.dumps(urls, ensure_ascii=False)
		print('Send data - all tests from archive')

class TestFromTestsResource:
	def on_get(self, req, resp, id):
		testName = '{}/{}.json'.format(pathToArchive, id)
		with open(testName, 'r') as f:
			data = json.load(f)
			resp.body =json.dumps(data, ensure_ascii=False)
		print('Send data - test {}'.format(id))		

api = application = falcon.API()
api.add_route('/running-test', RunningTestResource())
api.add_route('/tests', TestsResource())
api.add_route('/tests/{id}', TestFromTestsResource())
