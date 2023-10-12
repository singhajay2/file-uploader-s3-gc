import os
import boto3
from google.cloud import storage

class FileUploader:
    def __init__(self, aws_bucket, gcs_bucket, s3_client=None, gcs_client=None):
        self.aws_bucket = aws_bucket
        self.gcs_bucket = gcs_bucket
        self.s3_client = s3_client or boto3.client('s3')
        self.gcs_client = gcs_client or storage.Client()

    def upload_files(self, directory, s3_types, gcs_types):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = file.split('.')[-1]
                if file_extension in s3_types:
                    self.upload_to_s3(file_path)
                elif file_extension in gcs_types:
                    self.upload_to_gcs(file_path)

    def upload_to_s3(self, file_path):
        s3_key = os.path.relpath(file_path, start=directory)
        self.s3_client.upload_file(file_path, self.aws_bucket, s3_key)

    def upload_to_gcs(self, file_path):
        blob_name = os.path.relpath(file_path, start=directory)
        bucket = self.gcs_client.get_bucket(self.gcs_bucket)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)

if __name__ == "__main__":
    aws_bucket_name = "aws-bucket-name"
    gcs_bucket_name = "gcs-bucket-name"
    directory = "path-to-directory"
    s3_file_types = ["jpg", "png", "svg", "webp", "mp3", "mp4", "mpeg4", "wmv", "3gp", "webm"]
    gcs_file_types = ["doc", "docx", "csv", "pdf"]

    uploader = FileUploader(aws_bucket_name, gcs_bucket_name)
    uploader.upload_files(directory, s3_file_types, gcs_file_types)
