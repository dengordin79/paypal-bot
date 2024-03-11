""" создаем сервер в нашем случае это локальный хост формируем два юрл адреса
и связываем их декораторм с функциями пэйпал для формирования линка на оплату
и линка на подтверждение самого платежа и проведение последнего"""


import os
from flask import Flask, request
from dotenv import load_dotenv
from paypalsdk import Paypal


load_dotenv()
MY_CONFIG = {
    "mode": "sandbox", # sandbox or live
    "client_id": os.getenv("PAYPAL-CLIENT-ID"),
    "client_secret": os.getenv("PAYPAL-CLIENT-SECRET")
}

paypal = Paypal(MY_CONFIG)
app = Flask(__name__)


@app.get('/payment/get')
def get_payment():
    """
    Получение ссылки для проведения платежа
    """
    link = paypal.get_payment_link()
    return link if link else ("Error", 400)

@app.get('/payment/execute')
def do_payment():
    """
    Проведение платежа (перенаправление с платежной ссылки)
    """
    payer_id = request.args.get('PayerID')
    payment_id = request.args.get('paymentId')
    print(payer_id, payment_id)
    
    if paypal.execute_payment(payment_id, payer_id):
        return "Payment success"
    return "Error", 404
    
if __name__ == '__main__':
    app.run(debug=True)