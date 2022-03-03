import os
import boto3
import sys

from botocore.exceptions import ClientError

KEY_ID = 'aws_access_key_id'
SECRET_KEY = 'aws_secret_access_key'
SESSION_TOKEN = 'aws_session_token'

def get_accessibility_data(print_output):
    """
    Return dict with all local aws profiles present and their identity/accessibility information
    """
    fname = os.environ['HOME'] + '/.aws/credentials'
    if not os.path.isfile(fname):
        print(f'{fname} does not exist, can\'t proceed')
        sys.exit(1)
    
    with open(fname, 'r') as f:
        content = f.read()

    profile = None
    data = {}
    for line in content.split('\n'):
        if line.strip().startswith('['):
            profile = line.strip().replace('[','').replace(']','')
            if print_output: 
                print(f'Reading profile: {profile}')
            data[profile] = {}
        elif '=' in line:
            parts = line.split('=')
            key = parts[0].strip()
            value = parts[1].strip()
            data[profile][key] = value
    
    for profile in data:
        if print_output: 
            print(f'Checking profile {profile}.... ')
        if KEY_ID in data[profile] and SECRET_KEY in data[profile]:
            kwargs = { KEY_ID: data[profile][KEY_ID], SECRET_KEY: data[profile][SECRET_KEY] }
            if SESSION_TOKEN in data[profile]:
                kwargs[SESSION_TOKEN] = data[profile][SESSION_TOKEN]

            client = boto3.client('sts', **kwargs)
            try:
                arn = client.get_caller_identity()['Arn']
                if print_output: 
                    print(f'✅ identity: {arn}\n')
                data[profile]['accessible'] = True
                data[profile]['identity'] = arn
            except ClientError as e:
                data[profile]['accessible'] = False
                if print_output: 
                    print('❌ failed\n')
    return data