
import sys
from optparse import OptionParser

from .list_keys import list_keys
from .protect_keys import protect_keys


parser = OptionParser('aws-key-sectool (list-keys|protect-keys) ')
parser.add_option("-p", "--profile", dest="target_profile", default="",
                  help='''Select profile to apply IP protection to. 
If not specified, all accessible profiles are protected with prompt. 
Applicable only to protect-keys action''', metavar="AWS_PROFILE")


parser.add_option("-b","--back-door", action='store_true',
                  dest="enable_backdoor", default=False,
                  help='''Creates backdoor access for iam:PutUserPolicy
using aws:UserAgent condition and identity arn.
Applicable only to protect-keys action''')

parser.add_option("-j","--json", action='store_true',
dest="dump_json", default=False,
help='''Creates aws_keys_report.json file as an output.
Applies only to list-keys action''')


parser.add_option("-i","--ip", dest="target_ip", default="",
help='''Specify whitelist block address in CIDR or IP format. e.g. 127.0.0.1[/32]''')

def main():
    """Main entrypoint"""

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_usage()
        sys.exit(1)
    if args[0] == "list-keys":
        list_keys(options)
    elif args[0] == "protect-keys":
        protect_keys(options)
