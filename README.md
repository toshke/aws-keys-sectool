# aws-keys-security

Command line to list and protective working AWS credentials
on workstations and servers (use IAM roles for any compute, though!)


## Why? 

AWS long lived static credentials is still number 1 initial access vector
for 2021 security breaches, according to many security researches. 
See [here](https://blog.christophetd.fr/cloud-security-breaches-and-vulnerabilities-2021-in-review/#Static_Credentials_Remain_the_Major_Initial_Access_Vector)

## What

Code within the repo allows you to 
- list all of the working profiles from `~/.aws/credentials`, including those based on session tokens
- optionally protect yourself from AWS keys usage by simply whitelistening only current IP address for
  API calls. This does come with few caveats:
  
  - credentials need to allow `iam:PutUserPolicy` on the user credentials itself. Optionally, you can provide
    admin credentials to perform this operation using `--admin-profile` option
  
  - in order not to lock yourself out when changing IPs, [iam:PutUserPolicy] is left out of the protection, however
    it does have UserAgent string protection that would prevent it's usage by any process that are unaware of this
    script/method existance. 
  
  - everytime client IP address is changed, script needs be executed again to align the policy with the new IP        address 

## Requirements

`python3` and it's `boto3` 

If you are using AWS CLI, chances are good that these are already present on the system. 

## How

Simply, clone the repo and run the scripts

1 - clone the repo

```
git clone https://github.com:toshke/aws-keys-security.git
```

### Key listing

```
### default behaviour prints results in human readable format to stdout
python3 list_keys.py

### optionally to write output to json file use (aws_keys_report.json)
python3 list_keys.py machine-readable
```

### Key protection

```shell 
### default behaviour will leave a backdoor access for PutUserPolicy 
python3 protect_keys.py 

### which can be short-circuited with additional option
python3 protect_keys.py no-ua-backdoor
```