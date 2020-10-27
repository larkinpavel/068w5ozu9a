import json
import string
import random

def generate_capture_refunded(transaction_guid, net_amount):
    pay_pal_fee = 0.03 * net_amount
    refund_payload = {
        "id": get_random_webhook_id(),
        "event_version": "1.0",
        "create_time": "2020-10-27T07:45:33.973Z",
        "resource_type": "refund",
        "resource_version": "2.0",
        "event_type": "PAYMENT.CAPTURE.REFUNDED",
        "summary": f"A $ {net_amount} USD capture payment was refunded",
        "resource": {
          "seller_payable_breakdown": {
            "total_refunded_amount": {
              "value": net_amount,
              "currency_code": "USD"
            },
            "paypal_fee": {
              "value": pay_pal_fee,
              "currency_code": "USD"
            },
            "gross_amount": {
              "value": net_amount,
              "currency_code": "USD"
            },
            "net_amount": {
              "value": net_amount - pay_pal_fee,
              "currency_code": "USD"
            }
          },
          "amount": {
            "value": net_amount,
            "currency_code": "USD"
          },
          "update_time": "2020-10-27T00:44:36-07:00",
          "create_time": "2020-10-27T00:44:36-07:00",
          "custom_id": transaction_guid,
          "invoice_id": transaction_guid,
          "id": get_random_upper_letter_digit_string(17),
          "status": "COMPLETED"
        }
    }

    return json.dumps(refund_payload)

def generate_dispute_cancelled_by_buyer(transaction_guid, seller_transaction_id, paypal_merchant_id, net_amount):
    dispute_payload = {
        "id": get_random_webhook_id(),
        "event_version": "1.0",
        "create_time": "2020-10-26T16:20:56.886Z",
        "resource_type": "dispute",
        "event_type": "CUSTOMER.DISPUTE.RESOLVED",
        "summary": "A dispute was resolved with case # PP-D-29539",
        "resource": {
            "reason": "MERCHANDISE_OR_SERVICE_NOT_RECEIVED",
            "dispute_channel": "INTERNAL",
            "create_time": "2020-10-26T15:55:46.000Z",
            "dispute_id": get_random_dispute_id(),
            "dispute_life_cycle_stage": "INQUIRY",
            "refund_details": {
                "allowed_refund_amount": {
                    "value": net_amount,
                    "currency_code": "USD"
                }
            },
            "disputed_transactions": [{
                    "seller": {
                        "name": "Test Store",
                        "merchant_id": paypal_merchant_id
                    },
                    "seller_transaction_id": seller_transaction_id,
                    "custom": transaction_guid,
                    "invoice_number": transaction_guid,
                    "items": [],
                    "seller_protection_eligible": True
                }
            ],
            "update_time": "2020-10-26T16:20:29.000Z",
            "messages": [
            ],
            "links": [
            ],
            "dispute_amount": {
                "value": net_amount,
                "currency_code": "USD"
            },
            "dispute_outcome": {
                "outcome_code": "CANCELED_BY_BUYER"
            },
            "status": "RESOLVED"
        },
        "links": [
        ]
    }
    
    return json.dumps(dispute_payload)

def get_random_webhook_id():
    return 'WH-' + get_random_upper_letter_digit_string(17) + '-' + get_random_upper_letter_digit_string(17)

def get_random_dispute_id():
    return f"PP-D-{get_random_digit_string(10)}"
    
def get_random_upper_letter_digit_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_random_digit_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))

def generate_insert_statement(body):
    return upsert('PayPalWebhookRequests', DateTimeCreated = SqlParameter('GETDATE()'), Body = SqlParameter(body, SqlParameterFormat.quotate), Headers = 'NULL', IsValid = '1', ValidationMessage = 'NULL', ProcessingStatus = '1201', ProcessingMessage = 'NULL', Path = 'NULL')

def upsert(table, **kwargs):
    keys = ["%s" % key for key in kwargs]
    values = [str(v) for v in kwargs.values()]
    sql = list()
    sql.append("INSERT INTO %s \n(\n" % table)
    sql.append(",\n".join('\t{0}'.format(key) for key in keys))
    sql.append("\n)\nVALUES\n(")
    sql.append(",\n".join('\t{0}'.format(value) for value in values))
    sql.append("\n);")
    return "".join(sql)

from enum import Enum

SqlParameterFormat = Enum('SqlParameterFormat', 'quotate donothing')

class SqlParameter:
    def __init__(self, value, format = SqlParameterFormat.donothing):
        self.value = value
        self.format = format
        
    def __str__(self):
        if self.format == SqlParameterFormat.donothing:
            return str(self.value)
        elif self.format == SqlParameterFormat.quotate:
            return f"'{self.value}'"
        else:
            return f"'{self.value}'"