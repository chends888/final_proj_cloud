import boto3
from botocore.exceptions import ClientError

# Key pair and security group to be created names
print('Insira o nome da sua key pair (sem .pem):')
keypair_name = str(input())
print('Insira o nome do seu security group:')
security_group_name = str(input())
print('Insira o nome para ser registrado nas instâncias:')
owner_name = str(input())

# Configure AWS access keys before running 'aws configure'
ec2 = boto3.client('ec2')

# def del_and_create_keypair():
#     '''
#     Deletes possible key pairs with the provided name,
#     and creates a new one from the imported
#     '''

#     try:
#         ec2.delete_key_pair(KeyName=keypair_name)
#         print('Key pair:', keypair_name, 'deleted')
#     except ClientError as e:
#         print(e)

    # res_keypair = ec2.import_key_pair(
    #     KeyName=keypair_name,
    #     PublicKeyMaterial=b''
    # )
    # print(res_keypair)


def del_and_create_secgroup():
    '''
    Get vpc id and create security group
    '''
    try:
        response = ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        response = ec2.delete_security_group(GroupName=security_group_name)
        print('Security group:', security_group_name, 'deleted')
    except ClientError as e:
        print(e)

    try:
        # response = ec2.describe_security_groups()

        # Create security group
        response = ec2.create_security_group(GroupName=security_group_name,
                                            Description='Group for final project',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 5000,
                'ToPort': 5000,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

def del_and_create_instance():
    '''
    Delete current instances with tags provided,
    and create a new one
    '''

    res_inst_ids = ec2.describe_instances(
        Filters= [
            {
                'Name':'tag:Owner:',
                'Values':[owner_name]
            }
        ]
    )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrationec2.html
    instanceids = []
    for reservation in (res_inst_ids["Reservations"]):
        for instance in reservation["Instances"]:
            instanceids.append(instance["InstanceId"])
    try:
        ec2.terminate_instances(InstanceIds=instanceids)
        print('Instances:', instanceids, 'terminated')
    except ClientError as e:
        print(e)

    try:
        instances = ec2.run_instances(
            ImageId='ami-0ac019f4fcb7cb7e6', # Ubuntu 18 image
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
    except ClientError as e:
        print(e)


del_and_create_secgroup()
del_and_create_instance()