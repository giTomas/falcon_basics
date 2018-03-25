# https://codereview.stackexchange.com/questions/147731/simple-rest-api-using-python-with-falcon
import falcon
import json
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

class TestsResource:
	def on_get(self, req, resp):
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
api.add_route('/tests', TestsResource())
api.add_route('/tests/{id}', TestFromTestsResource())
