ccb-client-scripts
==================

## Dependencies

The scripts have the following dependencies [Jinja2](http://jinja.pocoo.org/docs/) for templating on first payment and [Requests](http://docs.python-requests.org/en/latest/) to perform the API calls.

You can install them as follows using [pip](https://pip.pypa.io):

```
pip install jinja2
pip install requests
```

## Configuration

You can set up your credentials (apikey & salt) and endpoint environment editing the [merchant.cfg](https://github.com/PDI-DGS-Protolab/ccb-client-scripts/blob/master/merchant.cfg) file.

You do not need to add any additional setting to the scripts.


## Usage 

### First payment

Creates a first payment html page including the signature.  

In order to complete the first payment, is required to use the resulting html in a browser.


```
$ python ./firstPayment.py 100 EUR tester@tid.es >prueba.html
```

### Recurring payment

Creates a recurring payment for an existing customer.

```
$ python ./recurringPayment.py 100 EUR tester@tid.es

REQUEST : POST https://www.ccb-pre.telefonica.com/payments
{"currency": "EUR", "amount": "100", "customerId": "tester@tid.es", "reference": "TST_423766", "merchantTimestamp": "2014/06/09 17:10:55"}

RESPONSE : 201
{"resultCode":"Authorised","reference":"TST_423766"}
```

### Modify payment

Captures or refunds an existing payment.

```
$ python ./modifyPayment.py refund TST_423766

REQUEST : POST https://www.ccb-pre.telefonica.com/payments/TST_423766
{"status": "Refunded"}

RESPONSE : 200
{"_id":"TST_423766","amount":100,"currency":"EUR","customerId":"538729107515b24afc4573d4","description":"","merchantId":"52e7cd3c9e29efe120c6ca63","merchantTimestamp":"2009-06-20T17:06:37.000Z","status":"Cancelling","statusHistory":[{"status":"Cancelling","timestamp":"2014-06-09T15:08:32.451Z"},{"status":"Capturing","timestamp":"2014-06-09T15:08:18.090Z"},{"status":"Authorised","timestamp":"2014-06-09T15:07:32.204Z"},{"status":"Initiated","timestamp":"2014-06-09T15:05:34.736Z"}],"timestamp":"2014-06-09T15:05:34.735Z"}
```
