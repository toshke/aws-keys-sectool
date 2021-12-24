#!/usr/bin/env python3

import sys
import json
import hashlib
import copy

import urllib.request

import boto3
import botocore.config

from aws_keys_security_common import get_accessibility_data

DENY_NOT_IP_POLICY = {
            "Sid": "DenyIpBased",
            "Effect": "Deny",
            "NotAction": "iam:PutUserPolicy",
            "Resource": "*",
            "Condition": {
                "NotIpAddress": {
                    "aws:SourceIp": ""
                }
            }
        }

DENY_NOT_UA_POLICY  = {
            "Sid": "DenyUABased",
            "Effect": "Deny",
            "Action": "iam:PutUserPolicy",
            "Resource": "*",
            "Condition": {
                "StringNotEquals": {
                    "aws:UserAgent": ""
                }
            }
        }

def main():
    no_ua_backdoor = len(sys.argv) > 1 and sys.argv[1] == "no-ua-backdoor"
    data = get_accessibility_data(False)
    accessible_profiles = [profile for profile in data if data[profile].get('accessible',False)]
    response = urllib.request.urlopen("http://ipinfo.io").read()
    ip = json.loads(response)['ip']
    for profile in accessible_profiles:
        arn = data[profile]['identity']
        if ':user' not in arn:
            print(f'Not applying protection for non-user identity {arn}')
            continue
        arn_digest = hashlib.sha256(arn.encode('utf-8')).hexdigest()
        policy = {  
            "Version": "2012-10-17",
            "Statement": [ copy.copy(DENY_NOT_IP_POLICY), copy.copy(DENY_NOT_UA_POLICY) ]
        }
        policy['Statement'][0]['Condition']['NotIpAddress']['aws:SourceIp'] = ip
        if no_ua_backdoor:
            del policy['Statement'][1]
            del policy['Statement'][0]['NotAction']
            policy['Statement'][0]['Action'] = '*'
        else:
            policy['Statement'][1]['Condition']['StringNotEquals']['aws:UserAgent'] = arn_digest

        iam = boto3.Session(profile_name=profile).client('iam', config=botocore.config.Config(
            user_agent=arn_digest
        ))
        print(f'Processing profile {profile}: {arn}')
        user = arn.split('/')[1]
        print(f'Set IP based protection ({ip}) on user {user}')
        iam.put_user_policy(
                UserName=user, 
                PolicyName='IpBasedProtection',
                PolicyDocument=json.dumps(policy)
        )

if __name__ == '__main__':
    main()