#!/usr/bin/python
import os
import json
import requests
import sys
import urllib3

# To disable InsecureRequestWarnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Enter your PAT token here
headers = {"Authorization": "Bearer enteryourPATtokenNumberhere"}
#Enter your GitHub organization name here
org = "mygithuborg"

sys.stdout = open("getpublicfacingrepos.csv", "w")
#Print the headers
print("{0},{1},{2},{3},{4},{5}".format("login","reponame","repourl","privatestatus","userurl","permissions"))

next = True
i = 1
while next == True:
    api_url = 'https://api.github.com' + "/orgs/" + org + "/members" + '?page={}&per_page=30'.format(i)
    response = requests.get(api_url, headers=headers, verify=False)
    json_data = response.json()
    for item in json_data:
        r = json.dumps(item)
        loaded_r = json.loads(r)
        try:
            login=loaded_r['login']
            publicrepoapi_url = 'https://api.github.com/users/' + login + '/repos'
            publicresponse= requests.get(publicrepoapi_url, headers=headers, verify=False)
            publicjson_data = publicresponse.json()
            for m in publicjson_data:
                n= json.dumps(m)
                loaded_n=json.loads(n)
                reponame = loaded_n['name']
                repourl = loaded_n['html_url']
                privatestatus = loaded_n['private']
                userurl = loaded_n['owner']['html_url']
                permissions = loaded_n['permissions']
                print("{0},{1},{2},{3},{4},{5}".format(login,reponame,repourl,privatestatus,userurl,permissions))#Print the values
        except Exception as err:
            raise err
    if 'Link' in response.headers:
        if 'rel="next"' not in response.headers['Link']:
            next = False
    i = i + 1
sys.stdout.close()
