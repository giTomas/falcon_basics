import json
import sys
import os
import os.path as path

class ReadWriteJson:
    def __init__(self, archiveDir='archive', runningDir='running'):

        self._absPath = path.dirname(path.abspath(__file__))
        self._pathToArchive = path.join(self._absPath, archiveDir)
        self._pathToRunning  = path.join(self._absPath, runningDir)

        if path.isdir(self._pathToArchive):
        	print('Directory archive  exists')
        else:
        	print('create directory {}'.format(self._pathToArchive))
        	os.makedirs(_pathToArchive, exist_ok=True)

        if path.isdir(self._pathToRunning  ):
        	print('Directory running exists')
        else:
        	print('create directory {}'.format(self._pathToRunning ))
        	os.makedirs(_pathToRunning , exist_ok=True)

        self._running_test_file = path.join(self._pathToRunning , 'running.json')
        self.setRunningNone()


    def listArchive(self):
    	jsonfiles = [f for f in os.listdir(self._pathToArchive) if path.isfile(path.join(self._pathToArchive, f))]
    	ids 	  = [path.splitext(f)[0] for f in jsonfiles]
    	return json.dumps(ids, ensure_ascii=False)

    def writeToRunning(self, data):
        with open(self._running_test_file, 'w') as f:
            json.dump(data, f)

    def writeToArchive(self, data, id):
        # file_name = '{}/{}.json'.format(_pathToArchive, id)
        file_name = path.join(self._pathToArchive, id+'.json')
        with open(file_name, 'w') as f:
            json.dump(data, f)

    def readFromArchive(self, id):
        file_name = path.join(self._pathToArchive, id+'.json')
        with open(file_name, 'r') as f:
            try:
                data = json.load(f)
            except ValueError as e:
                data = {'ValueError': '{}'.format(e)}
            except:
                e =  sys.exc_info()
                data = {'error': '{} {}'.format(e[0], e[1])}
        return json.dumps(data, ensure_ascii=False)

    def readFromRunning(self):
        with open(self._running_test_file, 'r') as f:
            # json.loads not working
            # TypeError: the JSON object must be str, not 'TextIOWrapper'
            # only json.load can read
            data = json.load(f)
        return json.dumps(data, ensure_ascii=False)

    def  setRunningNone(self):
        with open(self._running_test_file, 'w') as f:
            json.dump({'status': 'none', 'id': 'none'}, f)
