import sys
import random
import datetime
import base64
import hmac
import hashlib
import ConfigParser

from jinja2 import Environment, FileSystemLoader



# merchant and environment configuration
config = ConfigParser.ConfigParser()
config.read('merchant.cfg')
salt = config.get('merchant','salt')
merchant_account = config.get('merchant','merchant_account')
merchant_code = config.get('merchant','merchant_code') 
base_endpoint =  config.get('environment','base_endpoint') 

# calculate signature based on merchant salt
def calculate_hash(amount, currency, reference, customer_id, timestamp):
    string_to_hash = amount+currency+reference+customer_id+merchant_account+timestamp
    hm = hmac.new(salt, string_to_hash, hashlib.sha256)
    signature = base64.encodestring(hm.digest()).strip()
    return signature

# generate html page containing payment form
def generate_form(base_endpoint, amount, currency, reference, customer_id, timestamp, signature):
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template('payment_template.html')
    form =  template.render(
                   base_endpoint=base_endpoint,
                   amount=amount,
                   currency=currency,
                   reference=reference,
                   customer_id=customer_id,
                   timestamp=timestamp,
                   signature=signature,
                   merchant_account=merchant_account)
    return form


def main():   

    if len(sys.argv) != 4:
         print 'usage: ./firstPayment.py amount_minorunits currency_code customer_email'
         sys.exit(1)

    amount = sys.argv[1]
    currency = sys.argv[2]
    customer_id = sys.argv[3]
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    reference = merchant_code+"_"+str(random.randrange(0,1000000))
    
    signature = calculate_hash(amount, currency, reference, customer_id, timestamp)
    form = generate_form(base_endpoint, amount, currency, reference, customer_id, timestamp, signature) 
    print form


if __name__ == '__main__':
    main()