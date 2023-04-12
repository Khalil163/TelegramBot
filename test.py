import requests
import json

login = 'p632401387435-api'
password = 'Lazzat163.'

url = 'https://securepayments.sberbank.ru/payment/rest/register.do'

data = {
    'userName': login,
    'password': password,
    'amount': 1000,
    'language': 'ru',
    'returnUrl': 'https://t.me/lazzat_163_Bot',
    'orderNumber': '1222331*abc',
    'currency': 643,

}

rq = requests.post(url, data=data,  verify=False)
print(rq.text)

obj = json.loads(rq.text)
order_id = str(obj['orderId'])


# data2 = {
#     'userName': login,
#     'password': password,
#     'orderId': '4233285d-363d-716d-85cf-5c0b02d43fea',
#     'amount': 0,
# }
#
# rq = requests.post('https://securepayments.sberbank.ru/payment/rest/deposit.do', data=data2, verify=False)
#
# obj = json.loads(rq.text)
# order_id = str(obj['errorCode'])
# print(order_id)
#
# data3 = {
#     'userName': login,
#     'password': password,
#     'orderId': '4233285d-363d-716d-85cf-5c0b02d43fea',
# }
#
# rq = requests.post('https://securepayments.sberbank.ru/payment/rest/getOrderStatusExtended.do', data=data3, verify=False)
# obj = json.loads(rq.text)
# order_id = str(obj['orderStatus'])
# print(order_id)