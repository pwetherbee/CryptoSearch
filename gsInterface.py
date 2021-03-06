import os
from dotenv import load_dotenv
from google.api_core.exceptions import GoogleAPICallError, GoogleAPIError
from google.cloud import storage


# instantiate client
load_dotenv()
path = os.getenv("KEY_PATH")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

storage_client = storage.Client()


class GoogleStorage:
    def __init__(self):
        pass

    def createBucket(self, name):
        name = name.lower()
        try:
            bucket = storage_client.create_bucket(name)
            print("Bucket {} created".format(bucket.name))
            return
        except GoogleAPICallError as e:
            print(f'Bucket name already exists: {e}')

    def getBuckets(self):
        return [i for i in storage_client.list_buckets()]

    def uploadFile(self, bucket_name, source_file_name, destination_name):
        try:
            bucket = storage_client.get_bucket(bucket_name)
        except GoogleAPIError:
            print(f'Bucket name {bucket_name} does not exist')
            return
        blob = bucket.blob(destination_name)
        try:
            blob.upload_from_filename(source_file_name)
            print(
                f'Successfully uploaded file {source_file_name} to google-cloud: {bucket_name}/{destination_name}')
        except GoogleAPIError as e:
            print(f'Upload failed: {e}')
            return
        except FileNotFoundError as fnf:
            print(f'File not found in path {source_file_name}: {fnf}')
