import sys
import operator
import time
import random
import datetime
import requests
import json
import ConfigParser

# merchant and environment configuration
config = ConfigParser.ConfigParser()
config.read('merchant.cfg')
apikey = config.get('merchant','apikey')
merchant_account = config.get('merchant','merchant_account')
merchant_code = config.get('merchant','merchant_code') 
base_endpoint =  config.get('environment','base_endpoint') 

# generate html page containing payment form
def generate_request(operation, id):
    headers = {'Content-type': 'application/json', 'apikey': apikey}
    params = {'apikey' : apikey}
    data = {'status': operation}
    endpoint = base_endpoint+"/payments/"+id

    r = requests.post(endpoint, data=json.dumps(data), headers=headers, params=params, verify=False)
    
    print "REQUEST : POST " + endpoint
    print str(json.dumps(data))
    print "RESPONSE : "+ str(r.status_code)
    print r.text

def main():   

    if len(sys.argv) != 3:
         print 'usage: ./modifyPayment.py {refund|capture} id'
         sys.exit(1)

    operation = sys.argv[1]
    id = sys.argv[2]
    
    if operation == "refund" : 
         generate_request("Refunded", id) 
         sys.exit(0)
    if operation == "capture" : 
         generate_request("Captured", id) 
         sys.exit(0)
    else :
         print 'usage: ./modifyPayment.py {refund|capture} id'
         print "opeation: " + operation
         sys.exit(1)       
             

if __name__ == '__main__':
    main()