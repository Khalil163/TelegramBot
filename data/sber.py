import requests
import json
import string
import random

import create__bot
from data import sql
from create__bot import bot

login = 'p632401387435-api'
password = 'Lazzat163.'


async def url_pay(id, sum):
    url = 'https://securepayments.sberbank.ru/payment/rest/register.do'

    letters_and_digits = string.ascii_lowercase + string.digits
    orderNumber = ''.join(random.sample(letters_and_digits, 10))
    data = {
        'userName': login,
        'password': password,
        'amount': sum * 100,
        'language': 'ru',
        'returnUrl': 'https://t.me/lazzat_163_Bot',
        'orderNumber': orderNumber,
        'currency': 643,
    }
    rq = requests.post(url, data=data, verify=False)

    try:
        obj = json.loads(rq.text)
        url = str(obj['formUrl'])
        orderId = str(obj['orderId'])
        await sql.add_state_pay(id, orderId)
        return url
    except Exception as e:
        await url_pay(id, sum)



async def get_pay_status(id):
    orderId = await sql.get_state_pay(id)

    data = {
        'userName': login,
        'password': password,
        'orderId': orderId,
    }

    rq = requests.post('https://securepayments.sberbank.ru/payment/rest/getOrderStatusExtended.do', data=data,
                       verify=False)
    obj = json.loads(rq.text)
    orderStatus = str(obj['orderStatus'])
    return orderStatus


async def reverse_money(id, amount):
    orderId = await sql.get_state_pay(id)

    data = {
        'userName': login,
        'password': password,
        'orderId': orderId,
        'amount': amount*100
    }

    rq = requests.post('https://securepayments.sberbank.ru/payment/rest/refund.do', data=data,
                       verify=False)

    obj = json.loads(rq.text)
    print(rq.text)
    if int(error_code) == 0:
        pass
    else:
        await bot.send_message(create__bot.admin_id, 'Вернуть деньги не удалось!')