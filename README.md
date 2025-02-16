# NGINX Proxy Manager (NPM) Automation

## Purpose
Automate the ability to create proxy hosts within NPM using the built-in API and a static Cloudflare certificate

## Prerequisites
0. Register a domain, if you want this externally accessible, or setup DDNS/manual port-forwarding, etc. 
1. NGINX Proxy Manager running/installed on a machine, accessible at a domain (or local URL)
    - I am using Cloudflare Tunnels, but this could be tested locally before deploying
    - I am also using NPM via Docker, with 80, 81 and 443 exposed
2. Admin user account created in NPM
3. API key created against the user account in #2 - if not already generated, guidance is provided below
4. The python-dotenv library. After [installing pip](https://pip.pypa.io/en/stable/installation/), issue the following:
   `python# -m pip install python-dotenv`, substituting `#` with your Python version

## Usage
1. Clone this repository and create a .env file in the same folder
2. Generate an API token - this can be using Postman, cURL, or another RESTful API tool of your choice (I recommend the [ThunderClient](https://www.thunderclient.com/) VSCode extension). An example request is shown in the screenshot below:

#### **Headers:**
![headers](<Screenshot 2025-02-15 at 3.48.07 AM.png>)

#### **Request body:**
![request body](<Screenshot 2025-02-15 at 3.46.49 AM.png>)

**Note**: If no expiry value is specified, NPM appears to use a default value of 30 hours

3. The generated response will contain a Bearer token in JWT format that can be used for subsequent authenticated actions:

![alt text](<Screenshot 2025-02-15 at 3.53.52 AM.png>)

4. Fill out the following fields in the .env file:
    - API_KEY - token generated above
    - BASE_URL - base URL where NPM is accessed with no trailing / at the end (i.e. https://npm.domain.com)
    - CERTIFICATE - optional - this is the certificate ID if a single certificate (i.e. Cloudflare Origin Server cert for CF Tunnels) is used
        - sample cURL command to url/nginx/certs to retrieve this value as shown:
        ```
        curl --location 'https://yournpmurl.domain.com/api/nginx/certificates' \
        --header 'Authorization: Bearer <BEARER_AUTH_TOKEN_HERE>'
        ```
        - Optionally, pipe the output through `jq` to parse just the certificate ID:
        ```
        curl --location 'https://yournpmurl.domain.com/api/nginx/certificates' \
        --header 'Authorization: Bearer <BEARER_AUTH_TOKEN_HERE>' | jq '.[] | {id}'
        ```
        - This can be ommitted if Let's Encrypt is used instead
    - DOMAIN_NAME - your registered domain name, i.e. example.com
    - Before moving forward, set the permissions for this .env file to 600 - this is for security and will prevent anyone other than the user from read/writing it.
        - `chmod 600 .env` from within the directory with the .env file
5. Create a `proxy_hosts.csv` file containing the following:
    ```
    subdomain,schema,container_name,port
    ```
    - Example:
        ```
        port,https,portainer,9443
        ```
    - In the above example, a proxy host will be created for Portainer, reachable at port.domain.com - the port number is automatically handled and doesn't need to be appended at the end of the URL.
6. Once completed, run npm_api.py. It will automatically read through the CSV and, for each host listed, formulate the appropriate request to the NPM API

## Debugging
In case of issues, edit `npm_api.py` and un-comment the debug lines to get more granularity on what payload is being sent. In my testing, I discovered that the '400' status code seems to be used the most, but isn't terribly verbose - this can indicate an issue in the formatting of the .CSV, or (more problematically) that the host already exists. A good practice would be to do a GET to /api/nginx/proxy-hosts and validate the host doesn't already exist before creating it.

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
- [X] re-write README to flow better
- [ ] add in varying verbosity of debug levels
- [ ] related to debugs, add in logic that checks if a proxy host already exists before attempting to re-create it, as the 400 error code doesn't provide an indication of this.
- [ ] organize a Postman API collection that is actually updated

## References
- Portions of this code were generated using ChatGPT

All credits go to the original author of NPM. No copyright or trademark infringement is intended.
