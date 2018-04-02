import os
import os.path
import requests

def test_posted_image_gets_saved():
	file_save_prefix = '/tmp'
	location_prefix = '/images/'
	fake_images_bytes = b'fake_image_bytes'

	response = requests.post(
		'http://127.0.0.1:8000/images',
		data=b'fake_image_bytes',
		headers={'content-type': 'image/png'}
	)

	assert response.status_code == 201
	location = response.headers['location']
	assert location.startswith(location_prefix)
	image_name = location.replace(location_prefix, '')

	file_path = os.path.join(file_save_prefix, image_name)
	print(file_path)
	with open(file_path, 'rb') as image_file:
		assert image_file.read() == fake_images_bytes

	os.remove(file_path)