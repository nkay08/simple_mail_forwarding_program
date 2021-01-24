# simple_mail_forwarding_program (SMFP)
Python program to fetch and forward mails based on rules.

When switching the email provider you often run into the problem, that you cannot instantly update all records of your old email to you new one.
Some mail providers have a free forwarding option (big G corporation), but others (big Y corporation) do not.  
Some people believe that automatic forwarding is an security risk (some company administators), but the e-mail protocol is inherently unsafe (unless encrypted).

This tool provides an automatic way to fetch and forward unread mails of one account to another.
Due to technical limitations and security measures of mail providers the original `FROM` e-mail header is replaced by your old e-mail address.  
The original sender is instead added to the `REPLY-TO` header and as text/html to the mail body.



## Requirements
- `python3`
    - `pipenv`
        - Install required packages from `Pipfile` with [pipenv](https://pypi.org/project/pipenv/), OR manually

## Usage
- Create a forwarding rule as `json` file in `./rules`
    - Sample is available in folder and won't be loaded
- Run `main.py`



## Settings  
- Set environment variable `SMFP_RULES_DIR` to change the rules folder
 
### Possible future extensions
- Unit tests
- Allow fetching via SSL or not based on rule
- Allow sending via SSL or not based on rule
- Allow fetching via POP3 or IMAP based on rule
- Allow only fetching without forwarding
- Allow automatic encryption
- Allow fetching new, but read mails, instead of only unread



I am always open for improvements, as I often just "hack" things together.