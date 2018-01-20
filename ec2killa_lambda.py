#! env python
from __future__ import print_function
from datetime import datetime
import boto3, os

# All variables required to configure job, passed via Lambda envs

region = os.environ["region"]
tagkey = os.environ["tagkey"]
tagvalue = os.environ["tagvalue"]
batchsize = int(os.environ["batchsize"])

# boombox terminates 'running' EC2 instances identified by a given tag/tag-key 
# in a configurable batch size.

def printClock():
    now = datetime.now()
    clock = "%02d:%02d" % (now.hour,now.minute)
    # print(clock)
    return clock

def lambda_handler(event, context):

    start = printClock()
    print("Start time: %s" % start)
    ec2 = boto3.resource('ec2',region_name=region)

    instances = ec2.instances.filter(
        Filters=[
            {'Name': 'tag-key', 'Values': [tagkey]},
            {'Name': 'tag-value', 'Values': [tagvalue]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    fullist = []

    for instance in instances:
        fullist.append(instance.id)

# Nice to have, add rolling status (i.e. instances remaining) 
# Along with estimation based on time to complete last iteration

    if len(fullist) >= 1:
        print("Total instances to terminate: %s" % len(fullist))
        for i in xrange(0, len(fullist), batchsize):
            batch = fullist[i:i+batchsize]
            print("Terminating %s instances." % len(batch))
            ec2.instances.filter(InstanceIds=batch).terminate()
    elif len(fullist) == 0:
        return "There are no instances to terminate."
    
# change so that it will confirm / count actual # of terminated instances
    return "All instances terminated, completed at %s" % printClock()
