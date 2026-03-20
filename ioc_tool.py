import argparse
import requests
import json

def argument_parse():
    pars = argparse.ArgumentParser(
        prog='IOC tool with different API connections',
        description='A simple tool to background check several types of Indicators',
        usage='ioc_tool.py -t [TYPE] -i [INDICATORS]',
        epilog='Example: ioc_tool.py -t ip -i 8.8.8.8'
        )

    pars.add_argument(
        "-t", "--type",
        required=True,
        choices=["ip","domain","hash"],
        help="Choose a type of Indicator"
        )

    pars.add_argument(
        "-i", "--indicator",
        required=True,
        help="Input your indicator: domain, ip-address or hash"
        )
    
    return pars.parse_args()

def hash_api(hash):
    pass

def domain_api(domain):
    pass

def ip_api(ip_addr):
    pass

if __name__ == "__main__":
    args = argument_parse()
    if args.type == "hash":
        hash_api(args.indicator)
    elif args.type == "domain":
        domain_api(args.indicator)
    elif args.type == "ip":
        ip_api(args.indicator)

