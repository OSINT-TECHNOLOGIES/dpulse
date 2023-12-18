"""
Program start point

You can call this script from yours system terminal: python main.py -u "url" -ra "number"

"""

import report_creation as rc
import argparse

attributes_parser = argparse.ArgumentParser(description='OSINT methodology tool')

attributes_parser.add_argument('-sd',
                       '--url',
                       action='store',
                       type=str,
                       required=True,
                       help='Attribute which contains website to research and investigate. Should be shorted: google.com, github.com')

attributes_parser.add_argument('-ra',
                       '--ra',
                       action='store',
                       type=int,
                       required=True,
                       help='Attribute which specify output amount of Google Dorking.')

args = attributes_parser.parse_args()

print(f"Processing scan of {args.url}")

url = "http://" + str(args.url) + "/"

rc.create_report(str(args.url), url, args.ra)