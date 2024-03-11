import paypalrestsdk
import os
from dotenv import load_dotenv


load_dotenv()


class Paypal:
    def __init__(self, config):
        self.sdk = paypalrestsdk
        self.sdk.configure(config)

    def get_payment_link(self):
        
        payment = self.sdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:5000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "5.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print("Payment created successfully")

        else:
            return False

        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine Unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                approval_url = str(link.href)
                # print("Redirect for approval: %s" % (approval_url))
                return approval_url
            
        return False
    

    def execute_payment(self, payment_id, payer_id):
        payment = self.sdk.Payment.find(payment_id)
        return payment.execute({"payer_id": payer_id})
           