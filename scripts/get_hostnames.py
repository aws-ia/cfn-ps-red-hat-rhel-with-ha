import boto3
import botocore
import subprocess
import sys
import os

s3_client = boto3.client('s3')
hostname = os.uname()[1]

# error if argv length is not 2
# sys.argv[1] = the bucket name to store the files

hostnames = s3_client.list_objects_v2(Bucket=sys.argv[1], Prefix='hostnames/')['Contents']
hostlist = []
for obj in hostnames:
    hostlist.append(obj['Key'].split('/')[1])

hostlist.append(hostname)

# want to run 
# pcs host auth hostlist[0] hostlist[1] hostlist[2]
# pcs cluster setup hostlist[0] hostlist[1] hostlist[2]

if len(hostlist) == 2:
    subprocess.call('pcs host auth ' + hostlist[0] + ' ' + hostlist[1], shell=True)
    subprocess.call('pcs cluster setup ' + hostlist[0] + ' ' + hostlist[1], shell=True)
elif len(hostlist) == 3:
    subprocess.call('pcs host auth ' + hostlist[0] + ' ' + hostlist[1] + ' ' + hostlist[2], shell=True)
    subprocess.call('pcs cluster setup ' + hostlist[0] + ' ' + hostlist[1], shell=True)
elif len(hostlist) == 4:
    subprocess.call('pcs host auth ' + hostlist[0] + ' ' + hostlist[1] + ' ' + hostlist[2] + ' ' + hostlist[3], shell=True)
    subprocess.call('pcs cluster setup ' + hostlist[0] + ' ' + hostlist[1], shell=True)
else:
    print('invalid number of hostnames')
