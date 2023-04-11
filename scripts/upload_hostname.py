import boto3
import botocore
import subprocess
import os
import sys

s3_client = boto3.client('s3')
hostname = os.uname()[1]

# sys.argv[1] = the bucket name to store the files
# sys.argv[2] = the node number
# sys.argv[3] = the AWS region

filename = hostname + '+' + sys.argv[2]

subprocess.call('touch $(hostname)' + '+' + sys.argv[2], shell=True)
subprocess.call('sudo aws configure set default.region ' + sys.argv[3], shell=True)

s3_client.upload_file('./' + filename, sys.argv[1], 'hostnames/' + filename)
