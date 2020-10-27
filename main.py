import json

def generateCaptureRefunded(transaction_guid, net_amount):
	refund_payload = {
		"id": "WH-3MA894552E613690H-017341661D6772928",
		"event_version": "1.0",
		"create_time": "2020-10-27T07:45:33.973Z",
		"resource_type": "refund",
		"resource_version": "2.0",
		"event_type": "PAYMENT.CAPTURE.REFUNDED",
		"summary": f"A $ {net_amount} USD capture payment was refunded",
		"resource": {
		  "seller_payable_breakdown": {
			"total_refunded_amount": {
			  "value": "12.00",
			  "currency_code": "USD"
			},
			"paypal_fee": {
			  "value": "0.35",
			  "currency_code": "USD"
			},
			"gross_amount": {
			  "value": "12.00",
			  "currency_code": "USD"
			},
			"net_amount": {
			  "value": "11.65",
			  "currency_code": "USD"
			}
		  },
		  "amount": {
			"value": "12.00",
			"currency_code": "USD"
		  },
		  "update_time": "2020-10-27T00:44:36-07:00",
		  "create_time": "2020-10-27T00:44:36-07:00",
		  "custom_id": transaction_guid,
		  "invoice_id": transaction_guid,
		  "id": "97D452256N657123D",
		  "status": "COMPLETED"
		}
	}

	return json.dumps(refund_payload)
