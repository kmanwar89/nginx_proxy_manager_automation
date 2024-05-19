# Purpose: Leverage NPM API and Python requests library to
# programmatically create new hosts in NPM
# Programmer: Kadar Anwar
# Language: Python 3.10.12
# Filename: npm_api_automation.py
# Date: 19 MAY 2024

import csv
import requests
import os
from dotenv import load_dotenv

# Securely read in environment variables using .env files;
# this allows for flexibility in configuration while not exposing any
# sensitive information
load_dotenv()

api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL')
certificate_id = os.getenv('CERTIFICATE')
domain_name = os.getenv('DOMAIN_NAME')

def create_host():
    # Read CSV file
    with open('proxy_hosts.csv', 'r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            print (row)
            
            # Extracting values from CSV
            sub = row[0]
            scheme = row[1]
            container_name = row[2]
            port = row[3]
            
            # Constructing URL for proxy host creation
            url = f"{base_url}/api/nginx/proxy-hosts"
            
            # Data for the API call - not all values are used, un-comment accordingly
            data = {
                "domain_names": [sub+'.'+domain_name],
                "forward_scheme": scheme,
                "forward_host": container_name,
                "forward_port": port,
                "certificate_id": certificate_id,
                # "meta": {
                #     "letsencrpyt_agree": false,
                #     "dns_challenge": false
                # },
                # "advanced_config": "",
                # "locations": [],
                "block_exploits": "true",
                "caching_enabled": "true",
                # "allow_websocket_upgrade": "false",
                "http2_support": "true",
                # "hsts_enabled": "false",
                # "hsts_subdomains": "false",
                #"ssl_forced": "true",
                #"access_list_id": 0,
                "enabled": "true"
            }   
                
            headers = {
            "Authorization": f"Bearer" + api_key,
            "Content-Type": "application/json"
            }
            
            # Debugs can be un-commented for troubleshooting
            #print("Payload to be sent is:")
            #print(url)
            #print(data)
            
            # #Make API call to create proxy host
            response = requests.post(url, json=data, headers={"Authorization":f"Bearer {api_key}"})
            # response = requests.post(url, json=data, headers=headers)
            
            if response.status_code in (200,201):
                print(f"Proxy host for {sub}.kadaranwar.com created successfully")
            else:
                print(f"Error creating proxy host for {sub}.kadaranwar.com. Status code: {response.status_code}")
                        
def main():
    create_host()

main()