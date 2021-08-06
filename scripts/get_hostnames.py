import boto3
import botocore
import subprocess
import sys
import os
import urllib.request

s3_client = boto3.client('s3')
hostname = os.uname()[1]

# error if argv length is not 2
# sys.argv[1] = the bucket name to store the files
# sys.argv[2] = the cluster password
# sys.argv[3] = the AWS region
# sys.argv[4] = the floating ip address for fencing/rerouting
# sys.argv[5] = the route table ID
# sys.argv[6-8] = the instance IDs

hostnames = s3_client.list_objects_v2(Bucket=sys.argv[1], Prefix='hostnames/')['Contents']
hostdict = {}
hostmap_1 = ''
hostmap_2 = ''
hostmap_3 = ''
hostmap_4 = ''
numhosts = 1
for obj in hostnames:
    filename = obj['Key'].split('/')[1]
    split_name = filename.split('+')
    if split_name[1] == 'node1':
        hostdict['first'] = split_name[0]
        hostmap_1 = split_name[0] + ':' + sys.argv[6] + ';'
    elif split_name[1] == 'node2':
        hostdict['extra1'] = split_name[0]
        hostmap_2 = split_name[0] + ':' + sys.argv[7] + ';'
    elif split_name[1] == 'node3':
        hostdict['extra2'] = split_name[0]
        hostmap_3 = split_name[0] + ':' + sys.argv[8] + ';'
    numhosts += 1

hostdict['last'] = hostname
instanceid = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
hostmap_4 = hostname + ':' + instanceid

if numhosts == 2:
    subprocess.call('sudo pcs host auth ' + hostdict['first'] + ' ' + hostdict['last'] + ' -u hacluster -p ' + sys.argv[2], shell=True)
    subprocess.call('sudo pcs cluster setup newcluster ' + hostdict['first'] + ' ' + hostdict['last'] + ' --force', shell=True)
    subprocess.call('sudo pcs cluster start --all --wait', shell=True)
    subprocess.call('sudo pcs stonith create clusterfence fence_aws region=' + sys.argv[3] + ' pcmk_host_map=' + '\"' + hostmap_1 + hostmap_4 + '\"' + ' power_timeout=240 pcmk_reboot_timeout=480 pcmk_reboot_retries=4 --force', shell=True)
elif numhosts == 3:
    subprocess.call('sudo pcs host auth ' + hostdict['first'] + ' ' + hostdict['extra1'] + ' ' + hostdict['last'] + ' -u hacluster -p ' + sys.argv[2], shell=True)
    subprocess.call('sudo pcs cluster setup newcluster ' + hostdict['first'] + ' ' + hostdict['extra1'] + ' ' + hostdict['last'] + ' --force', shell=True)
    subprocess.call('sudo pcs cluster start --all --wait', shell=True)
    subprocess.call('sudo pcs stonith create clusterfence fence_aws region=' + sys.argv[3] + ' pcmk_host_map=' + '\"' + hostmap_1 + hostmap_2 + hostmap_4 + '\"' + ' power_timeout=240 pcmk_reboot_timeout=480 pcmk_reboot_retries=4 --force', shell=True)
elif numhosts == 4:
    subprocess.call('sudo pcs host auth ' + hostdict['first'] + ' ' + hostdict['extra1'] + ' ' + hostdict['extra2'] + ' ' + hostdict['last'] + ' -u hacluster -p ' + sys.argv[2], shell=True)
    subprocess.call('sudo pcs cluster setup newcluster ' + hostdict['first'] + ' ' + hostdict['extra1'] + ' ' + hostdict['extra2'] + ' ' + hostdict['last'] + ' --force', shell=True)
    subprocess.call('sudo pcs cluster start --all --wait', shell=True)
    subprocess.call('sudo pcs stonith create clusterfence fence_aws region=' + sys.argv[3] + ' pcmk_host_map=' + '\"' + hostmap_1 + hostmap_2 + hostmap_3 + hostmap_4 + '\"' + ' power_timeout=240 pcmk_reboot_timeout=480 pcmk_reboot_retries=4 --force', shell=True)
else:
    print('invalid number of hostnames')

subprocess.call('sudo aws configure set default.region ' + sys.argv[3], shell=True)
subprocess.call('sudo pcs resource create ha_listener ocf:heartbeat:aws-vpc-move-ip ip=' + sys.argv[4] + ' interface="eth0" routing_table=' + sys.argv[5] + ' op monitor timeout="30s" interval="60s"', shell=True)

subprocess.call('sudo pcs property set stonith-enabled=true', shell=True)
subprocess.call('sudo pcs property set start-failure-is-fatal=true', shell=True)
subprocess.call('sudo pcs property set cluster-recheck-interval=75s', shell=True)