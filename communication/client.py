import requests
import uuid
import random
import time
import json

url = 'http://127.0.0.1:8000/running-test'
tn = 5

def result_generator():
	coin = random.randint(0,10)
	
	if coin < 3:
		return 'passed'
	else:
		return 'failed'

for i in range(1, tn+1):
	test = {}
	test['id'] = int(uuid.uuid4())
	test['status'] = 'running'
	test['steps'] = random.randint(4,8)
	test['results'] = []
	
	requests.post(url, data=json.dumps(test))
		
	for j in range(1, test['steps']+1):	
		(test['results']).append({'step': j, 'result': result_generator()})
		requests.post(url , data=json.dumps(test))
		print('test no {}/{}  step {}/{}'.format(i, tn, j, test['steps'] ))   
		time.sleep(random.randint(1,10))
		
				
		
	test['status'] = 'done'
	requests.post(url , data=json.dumps(test))
	print(test)	
			
print('done')
