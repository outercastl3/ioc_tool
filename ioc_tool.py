import argparse
import requests
import json
import os
import sys
from datetime import datetime

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

def hash_api(filehash):
    api_url_virus = f"https://www.virustotal.com/api/v3/files/{filehash}"
    api_key_virus = os.environ.get("VIRUSTOTAL_KEY")
    
    try:
        response = requests.get(api_url_virus, headers={"x-apikey": api_key_virus, "accept": "application/json"}, timeout=10)
        if response.status_code == 200:
            response_data = response.json()["data"]["attributes"]
            last_date = datetime.utcfromtimestamp(response_data['last_analysis_date']).strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f"File Name: {response_data['meaningful_name']}") # add more data in the future
            print(f"Analysis Stats from {last_date}: {response_data['last_analysis_stats']}")
            print(f"File Type: {response_data['type_description']}")

        elif response.status_code == 400:
            print("BadRequestError")

        else:
             print(f"Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("Error, connection could not be established")

    except requests.exceptions.Timeout:
        print("Error: request timed out")

def domain_api(domain):
    api_url_virus_domain = f"https://www.virustotal.com/api/v3/domains/{domain}"
    api_key_virus = os.environ.get("VIRUSTOTAL_KEY")
    try:
        response = requests.get(api_url_virus_domain, headers={"x-apikey": api_key_virus, "accept": "application/json"}, timeout=10)
        if response.status_code == 200:
            response_data = response.json()["data"]["attributes"]
            print(f"Domain Name: {domain}")
            print(f"Results of last Analysis: {response_data['last_analysis_stats']}")


        elif response.status_code == 400:
            print("BadRequestError")

        else:
            print(f"Error: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("Error, connection could not be established")
    
    except requests.exceptions.Timeout:
        print("Error: request timed out")


def ip_api(ip_addr):
    api_url = "https://api.abuseipdb.com/api/v2/check"
    api_key = os.environ.get("ABUSEIPDB_KEY")
    try:
        response = requests.get(api_url, headers={"Key": api_key, "Accept": "application/json"}, params={"ipAddress": ip_addr, "maxAgeInDays":90}, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()["data"]
            print(f"IP: {response_data['ipAddress']}")
            print(f"Abuse Score: {response_data['abuseConfidenceScore']}")
            print(f"Country: {response_data['countryCode']}")
            print(f"ISP: {response_data['isp']}")
            print(f"Total Reports: {response_data['totalReports']}")
        elif response.status_code == 401:
            print("Error: Invalid API key")
            sys.exit(1)
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: Connection to AbuseIPDB could not be established")
    
    except requests.exceptions.Timeout:
        print("Error: Requests timed out")

if __name__ == "__main__":
    args = argument_parse()
    if args.type == "hash":
        hash_api(args.indicator)
    elif args.type == "domain":
        domain_api(args.indicator)
    elif args.type == "ip":
        ip_api(args.indicator)

