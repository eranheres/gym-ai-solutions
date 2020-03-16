from google.cloud import storage
from urllib.parse import urlparse
import os
from shutil import copyfile


class GCPUploader:
    def __init__(self, dest_folder):
        self._dest_bucket = urlparse(dest_folder).netloc
        self._dest_folder = urlparse(dest_folder).path[1:]
        self._storage_client = storage.Client()
        self._bucket = self._storage_client.get_bucket(self._dest_bucket)

    def upload(self, src_folder, filename):
        blob = self._bucket.blob(os.path.join(self._dest_folder, filename))
        blob.upload_from_filename(os.path.join(src_folder, filename))
        print(f'Uploaded {filename} to "{self._bucket}" bucket.')


class LocalUploader:
    def __init__(self, dest_folder):
        self._dest_folder = dest_folder
        if not os.path.exists(self._dest_folder):
            os.makedirs(self._dest_folder)

    def upload(self, src_folder, file):
        copyfile(os.path.join(src_folder, file), os.path.join(self._dest_folder, file))
