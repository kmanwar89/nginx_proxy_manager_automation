# Archived 19 MAY 2024 in favor of new code

## Automation for NPM reverse proxy manager

## Background
I discovered the Reddit "self hosted" community and quickly went down a rabbit hole of self-hosting, reverse proxies and Docker (oh my!). I discovered Nginx Proxy Manager (NPM) as an easy-to-use GUI with the ability to quickly add proxy hosts behind a reverse proxy, and secure them automatically using Let's Encrypt. While this is much easier than editing cryptic nginx config files, it became tedious each time I added, changed, or removed a host, so I wanted to automate it.

Unfortunately, there is no API or CLI, though an issue is already open on the NPM github. I leveraged tools I've used in the past, such as Selenium and Python, to accomplish this task.  The code isn't the prettiest, but I think for <75 sloc, it's not as bad as it could be. There are probably many improvements that can consolidate it even further, and those will be a future endeavour.

## Purpose
Automate the ability to create proxy hosts within NPM. Base (default) values that never change, at least in my setup, are:

- Base domain name
- Server IP address
- Block common exploits
- Cache assets
- Use a new Let's Encrypt certificate
- All options under the "SSL" tab

This means all of these values are selected by default in this script. I have included extensive comments, so it'd be trivial to identify where in the script each element is selected, and make appropriate selections accordingly should these defaults not work for you.

## Usage
- This program depends on the [Selenium](https://www.selenium.dev/) browser automation suite. Refer to their documentation to install the appropriate drivers. *pip* will likely need to be installed in order to install the drivers.

- I am using Brave, which is based on Chrome. In addition to the Selenium driver, download the specific driver for Chrome, which can be found [here](https://chromedriver.storage.googleapis.com/index.html). The version of Brave should match the Chrome version numbering, so download the appropriate driver and place it in the same folder as the Python script. NOTE: You should obviously modify these instructions based on your browser - there are drivers for Safari, Firefox, etc. Adjust accordingly.

- Modify the script to point to the path where the Chromedriver is located - I chose to copy mine to /usr/local/bin, but it can work just as well from within the same folder. Use absolute paths when specifying.

- This was written on MacOS, but there's no reason it shouldn't work on Windows or Linux. Testing on those is TBD.

## To-Do:
- [ ] accept a list of domains & ports in CSV format to pass through, to quickly allow the creation of multiple entries

- [ ] automatically look for Selenium webdriver files and, if not found, offer to automatically download them

- [ ] refactor, better organize and clean-up the code; maybe some loops or logic can be used to click through multiple elements?

- [ ] prompt for a server ID (statically and/or dynamically)

- [ ] further investigate the API located at /api/schema, and submit a PR for documentation of it.

## References:
https://stackoverflow.com/questions/47158434/how-to-run-selenium-tests-on-the-brave-web-browser

All credits go to the original author of NPM. No copyright or trademark infringement is intended.
