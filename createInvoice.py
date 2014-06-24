import sys
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


# generate html page containing payment form
def generate_request(totalNet, currency, customerId, timestamp):
    endpoint = base_endpoint + "/customers/" + customerId + "/invoices"
    headers = {'Content-type': 'application/json', 'apikey': apikey}
    data = {'type': 'purchase', 
            'fromDate': timestamp, 
            'toDate': timestamp, 
            'totalNet':totalNet, 
            'totalGross':totalNet,
            'totalTaxes':0,
            'currency':currency,
            'issueDate':timestamp,
            'taxDetails':[{
                'subtotalNet':0,
                'rate':0,
                'taxName':'IVA'}],
            'items':[{
                'name':'product #1',
                'unitPrice':totalNet,
                'amountNet':totalNet,
                'amountGross':totalNet,
                'units':1,
                'taxName':'IVA',
                'rate':0}]
            }

    r = requests.post(endpoint, data=json.dumps(data), headers=headers, verify=False)
    
    print "REQUEST : POST " + endpoint
    print str(json.dumps(data))
    print "RESPONSE : "+ str(r.status_code)
    print r.text

def main():   

    if len(sys.argv) != 4:
         print 'usage: ./createInvoice.py amount_minorunits currency_code customer_email'
         sys.exit(1)

    totalNet = sys.argv[1]
    currency = sys.argv[2]
    customerId = sys.argv[3]
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    data = generate_request(totalNet, currency, customerId, timestamp) 


if __name__ == '__main__':
    main()
    
 