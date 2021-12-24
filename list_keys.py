#!/usr/bin/env python3

import sys
import json

from aws_keys_security_common import get_accessibility_data


def main():
    machine_readable = len(sys.argv) > 1 and sys.argv[1] == "machine-readable"
    data = get_accessibility_data(not machine_readable)
    accessible_profiles = [profile for profile in data if data[profile].get('accessible',False)]
    
    if machine_readable:
        with open('aws_keys_report.json','w') as f:
            f.write(json.dumps(
                {
                'accessible_profiles': accessible_profiles, 
                 'profile_data': 
                    dict(map(lambda x:[x, {'accessible':data[x]['accessible'],'identity':data[x].get('identity','')}], data))
                }, indent=2))
        print(f'Machine readable info written to aws_keys_report.json')
    else:
        print(f'Accessible profiles:')
        print('\n'.join(accessible_profiles))
    
if __name__ == '__main__':
    main()