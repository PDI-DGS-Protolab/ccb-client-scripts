import sys
import ConfigParser

import requests



# merchant and environment configuration
config = ConfigParser.ConfigParser()
config.read('merchant.cfg')
apikey = config.get('merchant','apikey')
base_endpoint =  config.get('environment','base_endpoint') 


# generate GET request to get transaction info
def generate_request(id):
    endpoint = base_endpoint + "/payments/" + id
    headers = {'Content-type': 'application/json', 'apikey': apikey}
    params = {'apikey' : apikey}

    r = requests.get(endpoint, headers=headers, params=params, verify=False)
    
    print "REQUEST : GET " + endpoint
    print "RESPONSE : "+ str(r.status_code)
    print r.text


def main():   

    if len(sys.argv) != 2:
        print 'usage: ./getPayments.py id'
        sys.exit(1)

    id = sys.argv[1] 
     
    generate_request(id) 


if __name__ == '__main__':
    main()