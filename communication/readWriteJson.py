import json
import sys
import os
import os.path as path

class ReadWriteJson(object):

    def __init__(self, archiveDir='archive', runningDir='running'):

        self._absPath = path.dirname(path.abspath(__file__))
        self._pathToArchive = path.join(self._absPath, archiveDir)
        self._pathToRunning  = path.join(self._absPath, runningDir)

        if path.isdir(self._pathToArchive):
            print('Directory archive  exists')
        else:
            print('create directory {}'.format(self._pathToArchive))
            os.makedirs(self._pathToArchive, exist_ok=True)

        if path.isdir(self._pathToRunning  ):
            print('Directory running exists')
        else:
            print('create directory {}'.format(self._pathToRunning ))
            os.makedirs(self._pathToRunning , exist_ok=True)

        self._running_test_file = path.join(self._pathToRunning , 'running.json')
        self.setRunningNone()


    def listArchive(self):
        files_list = [f for f in os.listdir(self._pathToArchive) if path.isfile(path.join(self._pathToArchive, f))]
        # os.path.splitext - divide file name from ending
    	ids 	  = [path.splitext(f)[0] for f in files_list]
        return json.dumps(ids, ensure_ascii=False)

    def writeToRunning(self, data):
        with open(self._running_test_file, 'w') as f:
            json.dump(data, f)

    def writeToArchive(self, data, id):
        file_name = '{}.json'.format(id)
        file_path = path.join(self._pathToArchive, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def readFromArchive(self, id):
        file_name = '{}.json'.format(id)
        file_path = path.join(self._pathToArchive, file_name)
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except ValueError as err:
                data = {'error': 'ValueError - {}'.format(err)}
            except:
                err, msg =  sys.exc_info()
                data = {'error': '{err} - {msg}'.format(err=err, msg=msg)}
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
