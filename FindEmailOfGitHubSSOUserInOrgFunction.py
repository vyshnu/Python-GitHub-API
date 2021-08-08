  
#!/usr/bin/python
import os
import json
import requests
import sys
import urllib3
import csv
import pandas as pd
import config
from datetime import datetime
# To disable InsecureRequestWarnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# To run SSO USers Email python script
os.system('SSOEnabledGitUsers.py')
#Finding Email Of Login
def FindEmail(userlogin):
     data = pd.read_csv (r"sso_output.csv")   
     df = pd.DataFrame(data, columns= ['email','login'])
     newdf=(df.loc[df['login'] == userlogin])
     useremail= newdf.values[0][0]
     return useremail
