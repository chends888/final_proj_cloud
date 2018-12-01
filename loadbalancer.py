import boto3
from botocore.exceptions import ClientError
# pip install flask
from flask import Flask, redirect
import random
import requests
import time
import threading

# Configure AWS access keys before running 'aws configure'
ec2 = boto3.client('ec2')
waiter = ec2.get_waiter('instance_running')
# ec2_2 = boto3.resources('ec2', region_name='us-east-1')

def create_instance(keypair_name, security_group_name, owner_name):
    reservation = ec2.run_instances(
        ImageId='ami-0ac019f4fcb7cb7e6', # Ubuntu 18 Server image
        MinCount=1, 
        MaxCount=1,
        KeyName=keypair_name,
        InstanceType="t2.micro",
        SecurityGroups=[security_group_name],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Owner:',
                        'Value': owner_name
                    },
                ]
            },
        ],
        UserData='''#!/bin/bash
        cd /
        git clone https://github.com/chends888/final_proj_cloud.git
        cd final_proj_cloud/
        cd aps1/
        ./requirements.sh
        node server.js
        '''
    )
    print('Created instance successfully')
    return reservation

def get_instance_id():
    res_inst = ec2.describe_instances(
        Filters= [
            {
                'Name':'tag:Owner:',
                'Values':[owner_name]
            }
        ]
    )
    instance_ids_ips = []
    for reservation in (res_inst["Reservations"]):
        for instance in reservation["Instances"]:
            if (instance["State"]["Name"] == 'running'):
                instance_ids_ips.append((instance["InstanceId"],instance["PublicIpAddress"]))
    print(instance_ids_ips)
    return(random.choice(instance_ids_ips))

def healthcheck():
    while(True):
        res_inst = ec2.describe_instances(
            Filters= [
                {
                    'Name':'tag:Owner:',
                    'Values':[owner_name]
                }
            ]
        )
        instance_ids_ips = []
        for reservation in (res_inst["Reservations"]):
            for instance in reservation["Instances"]:
                if (instance["State"]["Name"] == 'running'):
                    instance_ids_ips.append((instance["InstanceId"],instance["PublicIpAddress"]))

        if (len(instance_ids_ips) < 2):
            print('creating missing instances')
            reservation = create_instance(keypair_name, security_group_name, owner_name)
            instance = reservation['Instances'][0]

            waiter.wait(InstanceIds=[instance["InstanceId"]])
        for i in instance_ids_ips:
            try:
                test = requests.get('http://'+i[1]+':5000/healthcheck/', timeout=2)
                if (test.status_code != 200):
                    ('creating missing instances')
                    reservation = create_instance(keypair_name, security_group_name, owner_name)
                    instance = reservation['Instances'][0]
                    print('Waiting for instance to initialize')
                    waiter.wait(InstanceIds=[instance["InstanceId"]])
                else:
                    print(len(instance_ids_ips), 'healthy servers running')
            except:
                print(len(instance_ids_ips), 'healthy servers running')

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect('http://'+get_instance_id()[1]+':5000/'+path)


if __name__ == '__main__':
    # Key pair and security group to be created names
    print('Insira o nome da sua key pair:')
    keypair_name = str(input())
    print('Insira o nome do seu security group:')
    security_group_name = str(input())
    print('Insira o nome para ser registrado nas instâncias:')
    owner_name = str(input())

    t = threading.Thread(target=healthcheck)
    t.start()

    app.run(host='0.0.0.0')