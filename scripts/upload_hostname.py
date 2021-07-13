import boto3
import botocore
import subprocess
import os
import sys

s3_client = boto3.client('s3')
hostname = os.uname()[1]

# error if argv length is not 2
# sys.argv[1] = the bucket name to store the files

subprocess.call('touch $(hostname)', shell=True)

s3_client.upload_file('./' + hostname, sys.argv[1], 'hostnames/' + hostname)