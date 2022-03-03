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
  
  - This works only if credentials allow `iam:PutUserPolicy` on the user    credentials itself. Optionally, you can provide
    admin credentials to perform this operation using `--admin-profile` option
  
  - in order not to lock yourself out when changing IPs, [iam:PutUserPolicy] is left out of the protection, however
    it does have UserAgent string protection that would prevent it's usage by any process that are unaware of this
    script/method existance. 
  
  - everytime client IP address is changed, script needs be executed again to align the policy with the new IP           address, consider scheduling 'update' command per examples below

## Requirements

`python3` and it's `boto3` 

If you are using AWS CLI, chances are good that these are already present on the system. 

## How

Simply, clone the repo and run the scripts

1 - build and install package

```
git clone https://github.com:toshke/aws-keys-sectool.git && \
  cd aws-keys-sectool && \
  python3 setup.py install 

### or simply install from PyPi
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
aws-keys-sectool protect-keys  [-b] [-p PROFILE]
```