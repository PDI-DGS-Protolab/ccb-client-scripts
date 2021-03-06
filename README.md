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
$ python ./firstPayment.py 100 EUR tester@tid.es >first_payment.html
```

The payment id wil be self generated, you can get check it on the generated html. 

On the following example the payment id is TST_796281.

```
$ grep reference first_payment.html
    <input type="hidden" type="text" name="reference" value="TST_796281">
```

Please note that the email provided will be shopper identifier for recurring payments.   

### Recurring payment

Creates a recurring payment for an existing customer.

```
$ python ./recurringPayment.py 100 EUR tester@tid.es

REQUEST : POST https://www.ccb-pre.telefonica.com/payments
{"currency": "EUR", "amount": "100", "customerId": "tester@tid.es", "reference": "TST_423766", "merchantTimestamp": "2014/06/09 17:10:55"}

RESPONSE : 201
{"resultCode":"Authorised","reference":"TST_423766"}
```

### Get payment

Gets information about existing payment.

```
$ python ./getPayment.py TST_423766

REQUEST : GET https://www.ccb-pre.telefonica.com/payments/TST_423766

RESPONSE : 200
{"_id":"TST_423766","amount":100,"currency":"EUR","customerId":"538729107515b24afc4573d4","merchantId":"52e7cd3c9e29efe120c6ca63","merchantTimestamp":"2009-06-20T17:10:55.000Z","paymentMethod":"","status":"Authorised","statusHistory":[{"status":"Authorised","timestamp":"2014-06-09T15:09:41.062Z"},{"status":"Initiated","timestamp":"2014-06-09T15:09:40.250Z"}],"timestamp":"2014-06-09T15:09:40.249Z"}
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

### Create invoice

Creates a new simple invoice with one item and no taxes

```
$ python ./createInvoice.py 150000 EUR tester@tid.es

REQUEST : POST https://www.ccb-pre.telefonica.com/customers/joser@tid.es/invoices
{"totalGross": "15000", "toDate": "2014/06/23 10:42:29", "totalTaxes": 0, "fromDate": "2014/06/23 10:42:29", "taxDetails": [{"rate": 0, "taxName": "IVA", "subtotalNet": 0}], "totalNet": "15000", "issueDate": "2014/06/23 10:42:29", "currency": "EUR", "type": "purchase", "items": [{"amountNet": "15000", "name": "product #1", "rate": 0, "units": 1, "amountGross": "15000", "unitPrice": "15000", "taxName": "IVA"}]}

RESPONSE : 201
{"number":"TST-P-23-0000000008","customerId":"tester@tid.es","totalGross":15000,"toDate":"2023-06-20T10:42:29.000Z","totalTaxes":0,"fromDate":"2023-06-20T10:42:29.000Z","totalNet":15000,"currency":"EUR","type":"purchase","merchantBillingInfo":{"countryCode":"UK","zipCode":"38383","state":"unknown","city":"Slough,  SL1 4DX","address":"260 Bath Road","vatNumber":"dummy","name":"Telefรณnica Digital UK"},"customerBillingInfo":{"countryCode":"ES","zipCode":"28001","state":"Madrid","city":"Madrid","address":"Calle Mayor, 22","vatNumber":"235456-AV","name":"John Smith"},"taxDetails":[{"rate":0,"taxName":"IVA","subtotalNet":0,"id":"53a7e875ded829582b3fecb6"}],"items":[{"amountNet":15000,"name":"product #1","rate":0,"units":1,"amountGross":15000,"unitPrice":15000,"taxName":"IVA","id":"53a7e875ded829582b3fecb5"}],"sent":false,"status":"Pending","issueDate":"2023-06-20T10:42:29.000Z","id":"53a7e875ded829582b3fecb4"}
```

You can also create a more complex invoice with several items with same item price and taxes.

On the following example the invoice will have 3 items, each item will be 3 EUR and a 21% of VAT:

```
python ./createComplexInvoice.py 3 300 EUR joser@tid.es 2100

REQUEST : POST http://localhost:8080/customers/joser@tid.es/invoices
{"totalGross": 1089, "toDate": "2014/06/24 11:51:58", "totalTaxes": 189, "fromDate": "2014/06/24 11:51:58", "taxDetails": [{"rate": 2100, "taxName": "IVA", "subtotalNet": 900}], "totalNet": 900, "issueDate": "2014/06/24 11:51:58", "currency": "EUR", "type": "purchase", "items": [{"amountNet": 300, "name": "product #0", "rate": 2100, "units": 1, "amountGross": 363, "unitPrice": 300, "taxName": "IVA"}, {"amountNet": 300, "name": "product #1", "rate": 2100, "units": 1, "amountGross": 363, "unitPrice": 300, "taxName": "IVA"}, {"amountNet": 300, "name": "product #2", "rate": 2100, "units": 1, "amountGross": 363, "unitPrice": 300, "taxName": "IVA"}]}

RESPONSE : 201
{"number":"TST-P-24-0000000022","customerId":"joser@tid.es","totalGross":1089,"toDate":"2024-06-20T11:51:58.000Z","totalTaxes":189,"fromDate":"2024-06-20T11:51:58.000Z","totalNet":900,"currency":"EUR","type":"purchase","merchantBillingInfo":{"countryCode":"UK","zipCode":"38383","state":"unknown","city":"Slough,  SL1 4DX","address":"260 Bath Road","vatNumber":"dummy","name":"Telefรณnica Digital UK"},"customerBillingInfo":{"countryCode":"ES","zipCode":"28001","state":"Madrid","city":"Madrid","address":"Calle Mayor, 22","vatNumber":"235456-AV","name":"John Smith"},"taxDetails":[{"rate":2100,"taxName":"IVA","subtotalNet":900,"id":"53a94a3eded829582b3fecfa"}],"items":[{"amountNet":300,"name":"product #0","rate":2100,"units":1,"amountGross":363,"unitPrice":300,"taxName":"IVA","id":"53a94a3eded829582b3fecf9"},{"amountNet":300,"name":"product #1","rate":2100,"units":1,"amountGross":363,"unitPrice":300,"taxName":"IVA","id":"53a94a3eded829582b3fecf8"},{"amountNet":300,"name":"product #2","rate":2100,"units":1,"amountGross":363,"unitPrice":300,"taxName":"IVA","id":"53a94a3eded829582b3fecf7"}],"sent":false,"status":"Pending","issueDate":"2024-06-20T11:51:58.000Z","id":"53a94a3eded829582b3fecf6"}
```