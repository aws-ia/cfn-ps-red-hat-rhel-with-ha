import boto3
import botocore
import subprocess

s3_client = boto3.client('s3')

# error if argv length is not 3
# sys.argv[1] = the bucket name to store the files
# sys.argv[2] = the hostname

subprocess.call('touch $(hostname)', shell=True)

s3_client.upload_file('./' + sys.argv[2], sys.argv[1], 'hostnames/' + sys.argv[2])