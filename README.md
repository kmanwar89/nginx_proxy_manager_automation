# NGINX Proxy Manager (NPM) Automation

## Purpose
Automate the ability to create proxy hosts within NPM using the built-in API and a static Cloudflare certificate

## Prerequisites
0. Register a domain, if you want this externally accessible, or setup DDNS/manual port-forwarding, etc. 
1. NGINX Proxy Manager running/installed on a machine, accessible at a domain (or local URL)
    - I am using Cloudflare Tunnels, but this could be tested locally before deploying
    - I am also using NPM via Docker, with 80, 81 and 443 exposed
2. User account created in NPM
3. API key created against the user account in #2 - if not already generated, guidance is provided below
4. The python-dotenv library (can be installed using *pip*)

## Usage
1. Clone this repository and create a .env file in the same folder
2. Fill out the following fields in the .env file:
    - API_KEY - API key used with NPM
        - sample cURL command to generate a 10 year token; adjust accordingly for 1d, 3m, 1y, etc.:
        ```
        curl --location 'https://yournpmurl.domain.com/api/tokens' \
            --form 'identity="YOUR_EMAIL_HERE"' \
            --form 'secret="YOUR_PASSWORD_HERE"'\
            --form 'expiry="10y"'
        ```
    - BASE_URL - base URL where NPM is accessed with no trailing / at the end
    - CERTIFICATE - optional - this is the certificate ID if a single certificate (i.e. Cloudflare Origin Server cert for CF Tunnels) is used
        - sample cURL command to url/nginx/certs to retrieve this value as shown:
        ```
        curl --location 'https://yournpmurl.domain.com/api/nginx/certificates' \
        --header 'Authorization: Bearer <BEARER_AUTH_TOKEN_HERE>'
        ```
        - Optionally, pipe the output through `jq` to parse just the certificate ID:
        ```
        curl --location 'https://npm.kadaranwar.com/api/nginx/certificates' \
        --header 'Authorization: Bearer <BEARER_AUTH_TOKEN_HERE>' | jq '.[] | {id}'
        ```
        - This can be ommitted if Let'sEncrypt is used instead
    - DOMAIN_NAME - your registered domain name, i.e. example.com
    - Before moving forward, set the permissions for this .env file to 600 - this is for security and will prevent anyone other than the user from read/writing it.
        - `chmod 600 .env` from within the directory with the .env file
3. Create a `proxy_hosts.csv` file containing the following:
    ```
    subdomain,schema,container_name,port
    ```
    - Example:
        ```
        port,https,portainer,9443
        ```
4. Once completed, run npm_api.py. It will automatically read through the CSV and, for each host listed, formulate the appropriate request to the NPM API

## To-Do
- [X] accept a list of domains & ports in CSV format to pass through, to quickly allow the creation of multiple entries

- [ ] refactor, better organize and clean-up the code
    - Add in functions for create, delete & list hosts
    - Programmatically/semi-automatically generate a token
    - More dynamic menus, prompting for base domain URL, dynamic CSV filename and other options
        - Store these as values in the .env file
- [X] further investigate the API located at /api/schema, and submit a PR for documentation of it
    - [Issue raised](https://github.com/NginxProxyManager/nginx-proxy-manager/issues/3749#issuecomment-2107483394)
- [ ] adjust code to perform more than one operation (i.e. CRUD on more than one host)

## References
- Portions of this code were generated using ChatGPT

All credits go to the original author of NPM. No copyright or trademark infringement is intended.
