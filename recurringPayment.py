import sys
import random
import datetime
import json
import ConfigParser

import requests



# merchant and environment configuration
config = ConfigParser.ConfigParser()
config.read('merchant.cfg')
apikey = config.get('merchant','apikey')
merchant_account = config.get('merchant','merchant_account')
merchant_code = config.get('merchant','merchant_code') 
base_endpoint =  config.get('environment','base_endpoint') 


# generate request
def generate_request(amount, currency, reference, customer_id, timestamp):
    endpoint = base_endpoint + "/payments"
    headers = {'Content-type': 'application/json', 'apikey': apikey}
    params = {'apikey' : apikey}
    data = {'amount': amount, 
            'currency': currency, 
            'reference': reference, 
            'customerId':customer_id, 
            'merchantTimestamp':timestamp}

    r = requests.post(endpoint, data=json.dumps(data), headers=headers, params=params, verify=False)
    
    print "REQUEST : POST " + endpoint
    print str(json.dumps(data))
    print "RESPONSE : "+ str(r.status_code)
    print r.text

def main():   

    if len(sys.argv) != 4:
         print 'usage: ./recurringPayment.py amount_minorunits currency_code customer_email'
         sys.exit(1)

    amount = sys.argv[1]
    currency = sys.argv[2]
    customer_id = sys.argv[3]
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    reference = merchant_code+"_"+str(random.randrange(0,1000000))
    
    data = generate_request(amount, currency, reference, customer_id, timestamp) 


if __name__ == '__main__':
    main()