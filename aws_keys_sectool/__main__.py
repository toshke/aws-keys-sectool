
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--profile", dest="target_profile", default="",
                  help="select single profile", metavar="PROFILE")
parser.add_option("-n", "--no-ua-backdor",
                  dest="no_ua_backdoor", default=False,
                  help="don't create UA string based backdoor")
parser.add_option("-a", "--admin-profile",
                  , dest="admin_profile", default=None,
                  help="admin profile to perform iam:PutUserPolicy")

(options, args) = parser.parse_args()

def main():
    