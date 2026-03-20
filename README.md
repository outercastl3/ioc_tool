# An Indicator of Compromise(IOC) tool
A self-written command-line Indicator of Compromise tool, which lookups across multiple thread intelligence sources

## Supported IOC Types
- **IP Addresses** - AbuseIPDB, Shodan
- **DOmains** - VirusTotal
- **File Hashes** - VirusTotal

## API Used
- AbuseIPDB
- Shodan
- VirusTotal

## Usage
ioc_tool.py -t [TYPE] -i [INDICATOR]
Example: ioc_tool.py -t ip -i 8.8.8.8

## Author 
Bogdan Ermakov
