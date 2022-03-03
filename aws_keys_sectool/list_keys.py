import sys
import json

from .common import get_accessibility_data


def list_keys(options):
    dump_json = options.dump_json
    data = get_accessibility_data(not dump_json)
    accessible_profiles = [profile for profile in data if data[profile].get('accessible',False)]
    
    if dump_json:
        with open('aws_keys_report.json','w') as f:
            f.write(json.dumps(
                {
                'accessible_profiles': accessible_profiles, 
                 'profile_data': 
                    dict(map(lambda x:[x, {'accessible':data[x]['accessible'],'identity':data[x].get('identity','')}], data))
                }, indent=2))
        print(f'Machine readable info written to aws_keys_report.json')
    else:
        print(f'\nAccessible profiles are:\n')
        print('✅ ' + '\n✅ '.join(accessible_profiles))
