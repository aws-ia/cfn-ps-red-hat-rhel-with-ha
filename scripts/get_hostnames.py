import boto3
import botocore
import subprocess
import sys
import os

s3_client = boto3.client('s3')
hostname = os.uname()[1]

# error if argv length is not 2
# sys.argv[1] = the bucket name to store the files
# sys.argv[2] = the cluster password
# sys.argv[3] = the AWS region
# sys.argv[4] = the floating ip address for fencing/rerouting
# sys.argv[5] = the route table ID
# sys.argv[6-9] = the instance IDs of the nodes


hostnames = s3_client.list_objects_v2(Bucket=sys.argv[1], Prefix='hostnames/')['Contents']
hostlist = []
hostmap = ''
for obj in hostnames:
    hostlist.append(obj['Key'].split('/')[1])

hostlist.append(hostname)

if len(hostlist) == 2:
    subprocess.call('sudo pcs host auth ' + hostlist[0] + ' ' + hostlist[1] + ' -u hacluster -p ' + sys.argv[2], shell=True)
    subprocess.call('sudo pcs cluster setup --name newcluster ' + hostlist[0] + ' ' + hostlist[1] + ' -u hacluster -p ' + sys.argv[2] + ' --force', shell=True)
    subprocess.call('sudo pcs cluster start --all --wait', shell=True)
elif len(hostlist) == 3:
    subprocess.call('sudo pcs host auth ' + hostlist[0] + ' ' + hostlist[1] + ' ' + hostlist[2] + ' -u hacluster -p ' + sys.argv[2], shell=True)
    subprocess.call('sudo pcs cluster setup --name newcluster ' + hostlist[0] + ' ' + hostlist[1] + ' -u hacluster -p ' + sys.argv[2] + ' --force', shell=True)
    subprocess.call('sudo pcs cluster start --all --wait', shell=True)
elif len(hostlist) == 4:
    subprocess.call('sudo pcs host auth ' + hostlist[0] + ' ' + hostlist[1] + ' ' + hostlist[2] + ' ' + hostlist[3] + ' -u hacluster -p ' + sys.argv[2], shell=True)
    subprocess.call('sudo pcs cluster setup --name newcluster ' + hostlist[0] + ' ' + hostlist[1] + ' -u hacluster -p ' + sys.argv[2] + ' --force', shell=True)
    subprocess.call('sudo pcs cluster start --all --wait', shell=True)
else:
    print('invalid number of hostnames')




