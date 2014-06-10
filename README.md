ccb-client-scripts
==================

## Dependencies

The scripts have the following dependencies jinja 2 for templating on first payment and request to perform the API calls.

You can install them as follows using pip:

pip install jinja2

pip install requests


## Configuration

You can set up your credencials (apikey & salt) and endpoint environment.


## Usage 

Simple python scripts to invoke CCB API

### First payment

$ python ./firstPayment.py 100 EUR tester@tid.es >prueba.html

### Recurring payment

$ python ./recurringPayment.py 100 EUR tester@tid.es

REQUEST : POST https://www.ccb-pre.telefonica.com/payments
{"currency": "EUR", "amount": "100", "customerId": "tester@tid.es", "reference": "TST_423766", "merchantTimestamp": "2014/06/09 17:10:55"}

RESPONSE : 201
{"resultCode":"Authorised","reference":"TST_423766"}

### Modifying a payment

$ python ./modifyPayment.py refund TST_423766

REQUEST : POST https://www.ccb-pre.telefonica.com/payments/TST_423766
{"status": "Refunded"}

RESPONSE : 200
{"_id":"TST_423766","amount":100,"currency":"EUR","customerId":"538729107515b24afc4573d4","description":"","merchantId":"52e7cd3c9e29efe120c6ca63","merchantTimestamp":"2009-06-20T17:06:37.000Z","status":"Cancelling","statusHistory":[{"status":"Cancelling","timestamp":"2014-06-09T15:08:32.451Z"},{"status":"Capturing","timestamp":"2014-06-09T15:08:18.090Z"},{"status":"Authorised","timestamp":"2014-06-09T15:07:32.204Z"},{"status":"Initiated","timestamp":"2014-06-09T15:05:34.736Z"}],"timestamp":"2014-06-09T15:05:34.735Z"}

