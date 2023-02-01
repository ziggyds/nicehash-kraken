import urllib.parse
import hashlib
import hmac
import base64
import time
import requests
import time
import os

# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
api_key = os.environ['API_KEY_KRAKEN']
api_sec = os.environ['API_SEC_KRAKEN']

# Retrieve API-Sign which must be unique for each api call
def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    print(sigdigest.decode())
    return sigdigest.decode()

# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)    
         
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    print(data)
    return req

# Construct the request and print the result
deposit_methods = kraken_request('/0/private/DepositMethods', {
    "nonce": str(int(1000*time.time())),
    "asset": "XBT"
}, api_key, api_sec)

print(deposit_methods.json())

resp = kraken_request('/0/private/DepositAddresses', {
    "nonce": str(int(1000*time.time())),
    "asset": "XBT",
    "method": "Bitcoin Lightning", # even tho it's listed as a method it seems not supported via api atm {'error': ['EService:Busy']}
    "new": True
}, api_key, api_sec)

print(resp.json())