# aws-keys-security

Command line to list and protective working AWS credentials
on workstations and servers (use IAM roles for any compute, though!)


❌  **IF YOUR IP IS NOT STATIC AND YOU DON'T USE -b OPTION YOU CAN EASILY LOCK 
YOURSELF OUT** 

## Why? 

AWS long lived static credentials is still number 1 initial access vector
for 2021 security breaches, according to many security researches. 
See [here](https://blog.christophetd.fr/cloud-security-breaches-and-vulnerabilities-2021-in-review/#Static_Credentials_Remain_the_Major_Initial_Access_Vector)

## What

Code within the repo allows you to 
- list all of the working profiles from `~/.aws/credentials`, including those based on session tokens
- optionally protect yourself from AWS keys usage by simply whitelistening only current IP address for
  API calls. This, however, does come with a few caveats:
  
  - This works only if credentials allow `iam:PutUserPolicy` on the user    credentials itself. 

  - in order not to lock yourself out when changing IPs, [iam:PutUserPolicy] is    left out of the full protection when using `-b` option, however
    it is conditioned using `aws:UserAgent` condition and expecting hash of the 
    user's arn for it's value. So, in credential leak scenario user is still protected if malicous actor is not aware the keys are protected using this utility
  
  - everytime client IP address is changed, script needs to be executed again to align the policy with the new IP address. 

[See it in action on asciinema](https://asciinema.org/a/481461)

## Requirements

- `python3` 
- `boto3` 

If you are using AWS CLI, chances are good that these are already present on the system. 

## How

Simply, clone the repo and run the scripts

1 - build and install package

```
git clone https://github.com:toshke/aws-keys-sectool.git && \
  cd aws-keys-sectool && \
  python3 setup.py install 

### or install from PyPi
pip3 install aws-keys-sectool
aws-keys-sectool -h
```

### Key listing

```
### default behaviour prints results in human readable format to stdout
aws-keys-sectool list-all-keys

### optionally to write output to json file use (aws_keys_report.json)
aws-keys-sectool list-all-keys -j
```

### Key protection

```shell 
### 
### Options explained
###   -b Add backdoor access. User will only be able to perform 
###        iam:PutUserPolicy action from different IP address, and
###        with UA string set to hash of user ARN. Not added 
###        by default, assuming that user is on a static IP
###        and there is admin account that can restore user's access in 
###        case of different IP
###                      
###   --profile PROFILE : Target specific AWS profile. All profiles 
###        are protected by default with a user prompt
###
###   --ip IP_ADDRESS: If you're whitelisting IP address (or range using CIDR format)
###         other than your current public IP, use this option. 
###         Default value is your current IP address obtained via ipinfo.io  
###
aws-keys-sectool protect-keys  [-b] [-p PROFILE] [-i] ip_address_or_cidr
```

## FAQ

*Q*: Can I do it manually? 

*A*: Yes, see policy below for policy without backdoor access
```
{
    "Sid": "DenyIpBased",
    "Effect": "Deny",
    "NotAction": "iam:PutUserPolicy",
    "Resource": "*",
    "Condition": {
        "NotIpAddress": {
            "aws:SourceIp": <YOUR_IP_GOES_HERE>
        }
    }
}
```



*Q*: What if I use backdoor option and my creds are leaked

*A*: Obviously backdoor implies there is vulnerability by design. 
Ideal scenario is avoid using backdoor option, and an admin profile
to update ip when changed. 
