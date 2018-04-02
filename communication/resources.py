import falcon

class Resource(object):
	def __init__(self, storage, cors):
		self.storage = storage
		self.cors = cors

class RunningTestResource(Resource):
	def __init__(self, storage, cors='*'):
		super().__init__(storage, cors)

	def on_post(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', self.cors)
		self.storage.writeToRunning(req.media)
		print('Running test updated {}'.format(req.media))

	def on_get(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')
		resp.body = self.storage.readFromRunning()
		resp.status = falcon.HTTP_200
		print('Sent data - running test')

class TestDoneResource(Resource):
	def __init__(self, storage, cors='*'):
		super().__init__(storage, cors)

	def on_post(self, req, resp, id):
		resp.set_header('Access-Control-Allow-Origin', self.cors)
		self.storage.setRunningNone()
		print('Test done - remove running')
		self.storage.writeToArchive(req.media, id)
		print('Test done - added to archive')

class TestsResource(Resource):
	def __init__(self, storage, cors='*'):
		super().__init__(storage, cors)

	def on_get(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', self.cors)
		resp.status = falcon.HTTP_200
		resp.body = self.storage.listArchive()
		print('Sent data - all tests from archive')

class TestFromTestsResource(Resource):
	def __init__(self, storage, cors='*'):
		super().__init__(storage, cors)

	def on_get(self, req, resp, id):
		resp.set_header('Access-Control-Allow-Origin', self.cors)
		resp.status = falcon.HTTP_200
		resp.body = self.storage.readFromArchive(id)
		print('Sent data - test {}'.format(id))