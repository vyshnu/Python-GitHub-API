import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
def get_spn():
    TENANT_ID = os.environ.get("AZURE_TENANT_ID")
    CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    KEYVAULT_NAME = os.environ.get("AZURE_KEYVAULT_NAME")
    KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net/"
    _credential = ClientSecretCredential(tenant_id=TENANT_ID,client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
    _sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)
    clientid = CLIENT_ID
    secret = _sc.get_secret("<enterurkeyvaultsecretname>").value
    return clientid, secret

def getpattoken():
    TENANT_ID = os.environ.get("AZURE_TENANT_ID")
    CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
    KEYVAULT_NAME = os.environ.get("AZURE_KEYVAULT_NAME")
    KEYVAULT_URI = f"https://{KEYVAULT_NAME}.vault.azure.net/"
    _credential = ClientSecretCredential(tenant_id=TENANT_ID,client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
    _sc = SecretClient(vault_url=KEYVAULT_URI, credential=_credential)
    pattoken = _sc.get_secret("<enterurkeyvaultpatname>").value
    return pattoken
