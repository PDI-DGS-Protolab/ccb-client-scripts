import sys
import datetime
import requests
import json
import ConfigParser


# merchant and environment configuration
config = ConfigParser.ConfigParser()
config.read('merchant.cfg')
apikey = config.get('merchant', 'apikey')
merchant_account = config.get('merchant', 'merchant_account')
merchant_code = config.get('merchant', 'merchant_code')
base_endpoint = config.get('environment', 'base_endpoint')


# generate html page containing payment form
def generate_request(items_number, items_amount_minorunits, currency, customer_id, vat_rate, timestamp):
    endpoint = base_endpoint + "/customers/" + customer_id + "/invoices"
    headers = {'Content-type': 'application/json', 'apikey': apikey}
    items = []

    for i in range(0,items_number):
        items.append(
            {'name': 'product #' + str(i),
             'unitPrice': items_amount_minorunits,
             'amountNet': items_amount_minorunits,
             'amountGross': items_amount_minorunits * (100 + vat_rate / 100) / 100,
             'units': 1,
             'taxName': 'IVA',
             'rate': vat_rate}
        )

    data = {'type': 'purchase',
            'fromDate': timestamp,
            'toDate': timestamp,
            'totalNet': items_amount_minorunits * items_number,
            'totalGross': items_amount_minorunits * items_number * (100 + vat_rate / 100) / 100,
            'totalTaxes': items_amount_minorunits * items_number * vat_rate / 10000,
            'currency': currency,
            'issueDate': timestamp,
            'taxDetails': [{
                               'subtotalNet': items_amount_minorunits * items_number,
                               'rate': vat_rate,
                               'taxName': 'IVA'}],
            'items': items
    }

    r = requests.post(endpoint, data=json.dumps(data), headers=headers, verify=False)

    print "REQUEST : POST " + endpoint
    print str(json.dumps(data))
    print "RESPONSE : " + str(r.status_code)
    print r.text


def main():
    if len(sys.argv) != 6:
        print 'usage: ./createInvoice.py items_number items_amount_minorunits currency_code customer_email vat_rate'
        sys.exit(1)

    items_number = int(sys.argv[1])
    items_amount_minorunits = int(sys.argv[2])
    currency = sys.argv[3]
    customer_id = sys.argv[4]
    vat_rate = int(sys.argv[5])
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    generate_request(items_number, items_amount_minorunits, currency, customer_id, vat_rate, timestamp)


if __name__ == '__main__':
    main()