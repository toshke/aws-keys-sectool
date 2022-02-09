
from optparse import OptionParser
from .list_keys import list_keys
from .protect_keys import protect_keys

import sys

parser = OptionParser('aws-key-sectool (list-keys|protect-keys) ')
parser.add_option("-p", "--profile", dest="target_profile", default="",
                  help="select single profile", metavar="PROFILE")
parser.add_option("-n", "--no-ua-backdor",
                  dest="no_ua_backdoor", default=False,
                  help="don't create UA string based backdoor")
parser.add_option("-a", "--admin-profile",
                  dest="admin_profile", default=None,
                  help="admin profile to perform iam:PutUserPolicy")


def main():

    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_usage()
        sys.exit(1)
    if args[1] == "list-keys":
        list_keys()
    elif args[1] == "protect-keys":
        protect_keys()