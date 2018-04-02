# https://www.journaldev.com/19178/python-io-bytesio-stringio
# https://www.programcreek.com/python/example/1734/io.BytesIO

# import json
import io
import os
import re
import uuid
import mimetypes

import falcon
import msgpack

class Collection(object):

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp):

        image_list = [f for f in os.listdir(self._image_store.storage_path)
                      if  self._image_store.IMAGE_NAME_PATTERN.match(f)]
        doc = {
            'images': [ { 'href': f } for f in image_list ]
        }

        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name

class Item(object):

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, name):
        resp.content_type = mimetypes.guess_type(name)[0]
        resp.stream, resp.stream_len = self._image_store.open(name)

class ImageStore(object):

    _CHUNK_SIZE_BYTES = 4096
    IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.[a-z]{2,4}$'
    )

    # dependency injection - named arguments
    def __init__(self, storage_path, uuidgen=uuid.uuid4, fopen=io.open):
        self.storage_path = storage_path
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, image_stream, image_content_type):
        ext = mimetypes.guess_extension(image_content_type)
        name = '{uuid}{ext}'.format(uuid=self._uuidgen(), ext=ext)
        image_path = os.path.join(self.storage_path, name)

        with self._fopen(image_path, 'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        return name

    def open(self, name):
        if not self.IMAGE_NAME_PATTERN.match(name):
            raise IOError('File not found')

        image_path = os.path.join(self.storage_path, name)
        stream = self._fopen(image_path, 'rb')
        stream_len = os.path.getsize(image_path)

        return stream, stream_len

# msgpack.unpackb(r, raw=False)


