import os
import boto3
import google.cloud.storage as storage
import pytest
from google.cloud import storage as gcs_storage
from file_upload_module import FileUploader

# test configuration
AWS_BUCKET_NAME = "test-aws-bucket"
GCS_BUCKET_NAME = "test-gcs-bucket"
TEST_DIRECTORY = "test-directory"
S3_FILE_TYPES = ["jpg", "png"]
GCS_FILE_TYPES = ["pdf"]

@pytest.fixture
def s3_client():
    yield boto3.client("s3")

@pytest.fixture
def gcs_client():
    """
        Its need a DefaultCredentials to run, Hence this line will raise a DefaultCredentialsError 
        I am not creating service account because of its asking for my debit/credit card info 
        without this I cannot create service account
    """
    yield gcs_storage.Client()

@pytest.fixture
def file_uploader(s3_client, gcs_client):
    return FileUploader(AWS_BUCKET_NAME, GCS_BUCKET_NAME, s3_client, gcs_client)

def create_test_files():
    # Create test files in the test directory
    os.makedirs(TEST_DIRECTORY, exist_ok=True)
    with open(os.path.join(TEST_DIRECTORY, "test.jpg"), "w") as f:
        f.write("Test content")
    with open(os.path.join(TEST_DIRECTORY, "test.png"), "w") as f:
        f.write("Test content")
    with open(os.path.join(TEST_DIRECTORY, "test.pdf"), "w") as f:
        f.write("Test content")

def test_upload_to_s3(file_uploader, s3_client):
    create_test_files()
    file_uploader.upload_to_s3(os.path.join(TEST_DIRECTORY, "test.jpg"))
    objects = s3_client.list_objects(Bucket=AWS_BUCKET_NAME)
    assert len(objects.get("Contents")) == 1

def test_upload_to_gcs(file_uploader, gcs_client):
    create_test_files()
    file_uploader.upload_to_gcs(os.path.join(TEST_DIRECTORY, "test.pdf"))
    bucket = gcs_client.get_bucket(GCS_BUCKET_NAME)
    blob = storage.Blob("test.pdf", bucket)
    assert blob.exists()

def test_upload_files(file_uploader, s3_client, gcs_client):
    create_test_files()
    file_uploader.upload_files(TEST_DIRECTORY, S3_FILE_TYPES, GCS_FILE_TYPES)
    # Check S3 uploads
    objects = s3_client.list_objects(Bucket=AWS_BUCKET_NAME)
    assert len(objects.get("Contents")) == 2
    # Check GCS uploads
    bucket = gcs_client.get_bucket(GCS_BUCKET_NAME)
    blob = storage.Blob("test.pdf", bucket)
    assert blob.exists()

if __name__ == "__main__":
    pytest.main([__file__])
