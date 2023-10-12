# file-uploader-s3-gc
Creating a Python module that can upload files to both AWS S3 and Google Cloud Storage based on configurable file types requires several steps

# First clone this repo using below command
git clone https://github.com/singhajay2/file-uploader-s3-gc.git

# Create virtaul enviorment for your project to install dependent libraries

# install virtualenv first using below command
sudo apt install virtualenv

# create virtualenv with your correspondence python version
virtualenv <env-name> --python=python3.8

# Just activate your virtaul enviorment by below command
source <env-name>/bin/activate

# You'll need to use the Boto3 library for AWS S3 and the google-cloud-storage library for Google Cloud Storage so install the necessary libraries for this
pip install boto3 google-cloud-storage

# Install pytest to run unit test cases for this project
pip install pytest
