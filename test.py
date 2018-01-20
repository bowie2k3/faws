#!/usr/bin/python

import boto3    

ec2client = boto3.client('ec2')

tagkey = "Name"
tagvalue = "awsr53"

response = ec2client.describe_instances(
    Filters = [
        {
            'Name':'tag:'+tagkey, 
            'Values':[tagvalue]
        }
    ]
    )

instancelist = []

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        # This will print will output the value of the Dictionary key 'InstanceId'
        print(instance["InstanceId"])

     #   for instance in reservation["Instances"]:
     #       instancelist.append(instance["InstanceId"])
      #  return instancelist 