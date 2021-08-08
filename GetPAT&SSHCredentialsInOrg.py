#!/usr/bin/python
import os
import json
import requests
import sys
headers = {"Authorization": "Bearer XXXXXXXx"}

def check_key_exists(loaddict,loadkey):
    if loaddict.get(loadkey) is not None:
        return True
    else:
        return False

sys.stdout = open("getpatsssh.csv", "w")
#Print the headers
print("{0},{1},{2},{3},{4},{5},{6}".format("login", "token_last_eight", "credential_id",
                                           "credential_type", "credential_authorized_at", "credential_accessed_at",
                                           "scopes"))
org="mygithuborg" #Enter your GitHub organization
next = True
i = 1
while next == True:
    api_url = 'https://api.github.com' + "/orgs/" + org + "/credential-authorizations" + '?page={}&per_page=100'.format(i)
    response = requests.get(api_url, headers=headers, verify=False)
    json_data = response.json()
    for item in json_data:
        r = json.dumps(item)
        loaded_r = json.loads(r)
        try:
            login=loaded_r['login']
            token_last_eight=""
            if check_key_exists(loaded_r, 'token_last_eight'):
                token_last_eight=loaded_r['token_last_eight']
            credential_id=loaded_r['credential_id']
            credential_type=loaded_r['credential_type']
            credential_authorized_at=loaded_r['credential_authorized_at']
            credential_accessed_at=loaded_r['credential_accessed_at']
            scopes=""
            if check_key_exists(loaded_r, 'scopes'):
                scopes = '|'.join(loaded_r['scopes'])
            #Print the values
            print("{0},{1},{2},{3},{4},{5},{6}".format(login,token_last_eight,credential_id,credential_type,
                                                   credential_authorized_at,credential_accessed_at,scopes))
        except Exception as err:
            raise err
    if 'Link' in response.headers:
        if 'rel="next"' not in response.headers['Link']:
            next = False
    i = i + 1
sys.stdout.close()
