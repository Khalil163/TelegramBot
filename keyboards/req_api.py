import requests
import json
from data import sql
from create__bot import API_TAXI, client_id, bot
import uuid
from keyboards import client_kb

# info = await sql.get_info(id)
# async def draft_order(id):
#     info = await sql.get_info(id)
#     res = {
#         "comment": "some comment",
#         "fullname": "Имя Фамилия",
#         "phone": "+71112223344",
#         "due": "2013-04-01T14:00:00+0400",
#         "source": {
#             "country": "Россия",
#             "fullname": "Россия, Москва, Новосущевская, 1",
#             "geopoint": [
#                 33.6,
#                 55.1
#             ],
#             "locality": "Москва",
#             "porchnumber": "1",
#             "premisenumber": "1",
#             "thoroughfare": "Новосущевская"
#         },
#         "interim_destinations": [{
#             "country": "Россия",
#             "fullname": "Россия, Москва, Троицкая, 15с1",
#             "geopoint": [
#                 37.6,
#                 55.7
#             ],
#             "locality": "Москва",
#             "porchnumber": "",
#             "premisenumber": "15с1",
#             "thoroughfare": "Троицкая"
#         }],
#         "destination": {
#             "country": "Россия",
#             "fullname": "Россия, Москва, 8 Марта, 4",
#             "geopoint": [
#                 33.1,
#                 52.1
#             ],
#             "locality": "Москва",
#             "porchnumber": "",
#             "premisenumber": "4",
#             "thoroughfare": "8 Марта"
#         },
#         "class": "econom",
#         "requirements": {
#             "nosmoking": True
#         },
#     }
#     # {
#     #     "comment": "",
#     #     "source": {
#     #         "country": "Россия",
#     #         "fullname": "Россия, Тольятти, улица Комсомольская, 62с5",
#     #         "short_text": "улица Комсомольская, 62с5",
#     #         "short_text_from": "улица Комсомольская, 62с5",
#     #         "short_text_to": "улица Комсомольская, 62с5",
#     #         "geopoint": [
#     #             49.408787,
#     #             53.518245
#     #         ],
#     #         "locality": "Тольятти",
#     #         "premisenumber": "62с5",
#     #         "thoroughfare": "улица Комсомольская",
#     #         "type": "address",
#     #         "object_type": "другое",
#     #         "extra_data": {
#     #             "contact_phone": "+79649687004",
#     #             "floor": "1",
#     #             "apartment": "1",
#     #             "comment": "my comment"
#     #         }
#     #     },
#     #     "class": "express",
#     #     "requirements": {"door_to_door": True},
#     #     "phone": "+79811234567",
#     #     "destination": {
#     #         "country": "Россия",
#     #         "fullname": str(info[11]),
#     #         "short_text": str(info[11]),
#     #         "short_text_from": str(info[11]),
#     #         "short_text_to": str(info[11]),
#     #         "geopoint": [
#     #             int(info[4]),
#     #             int(info[5])
#     #         ],
#     #         "locality": "Тольятти",
#     #         "premisenumber": str(info[11]).split(',')[1],
#     #         "thoroughfare": str(info[11]).split(',')[0],
#     #         "type": "address",
#     #         "object_type": "другое",
#     #         "extra_data": {
#     #             "contact_phone": f"{info[3]}",
#     #             "floor": "0",
#     #             "apartment": "0",
#     #             "comment": "0"
#     #         },
#     #         "cost_center": "some cost center"
#     #     },
#     #     'offer': str(info[9])
#     # }
#
#     # {
#     #     "comment": "",
#     #     "source": {
#     #         "country": "Россия",
#     #         "fullname": "Россия, Тольятти, улица Комсомольская, 62c5",
#     #         "short_text": "улица Комсомольская, 62с5",
#     #         "short_text_to": "Тольятти, Комсомольская 62с5",
#     #         "geopoint": [
#     #             49.408787,
#     #             53.518245
#     #         ],
#     #         "locality": 'Тольятти',
#     #         "premisenumber": "62c5",
#     #         "thoroughfare": "улица Комсомольская, 62с5",
#     #         "type": "address",
#     #         "object_type": "другое",
#     #         "extra_data": {
#     #             "contact_phone": "+79649687004",
#     #             "floor": "1",
#     #             "apartment": "1",
#     #             "comment": "Кафе Лаззат. Зеленые ворота"
#     #         }
#     #     },
#     #
#     #     "class": "express",
#     #     "requirements": {"door_to_door": True},
#     #     "phone": "+79649687004",
#     #     "destination": {
#     #         "country": "Россия",
#     #         "fullname": str(info[11]),
#     #         "geopoint": [
#     #             int(info[4]),
#     #             int(info[5])
#     #         ],
#     #         "extra_data": {
#     #             "contact_phone": f"{info[3]}",
#     #         },
#     #     }
#     # }
#
#     rq = requests.post(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/',
#                        headers={"Authorization": API_TAXI}, json=res)
#     print(rq.text)
#     print(rq)
#
#     if str(rq) == '<Response [200]>':
#         obj = json.loads(rq.text)
#         a = str(obj['_id'])
#         await sql.add_offer(id, a)
#     else:
#         await bot.send_message(1176527696,
#                                f'Сбой такси:\nВам придется заказать такси самому: \nТел: {await sql.get_num(id)}')
#
#
# async def proc_order(id):
#     offer = await sql.get_offer(id)
#     rq = requests.post(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/{offer}/processing',
#                        headers={"Authorization": API_TAXI})
#     print("proc: ", rq, rq.text)
#     if rq == 200:
#         obj = json.loads(rq.text)
#         a = str(obj['status']['description'])
#         return a
#     elif str(rq) == '<Response [406]>':
#         await client_kb.get_price(id)
#         await draft_order(id)
#         await proc_order(id)
#     else:
#         await bot.send_message(1176527696,
#                                f'Сбой вызова такси:\nВам придется заказать такси самому: \nТел: {await sql.get_num(id)}')
#
#
# async def cancel_order(id):
#     offer = await sql.get_offer(id)
#     rq = requests.get(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/{offer}?show_cancel_text=true',
#                       headers={"Authorization": API_TAXI})
#     obj = json.loads(rq.text)
#     state = str(obj['cancel_rules']['state'])
#     js = {
#         'state': str(state)
#     }
#
#     rq = requests.get(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/{offer}/cancel',
#                       headers={"Authorization": API_TAXI}, json=js)
#     if rq == 200:
#         pass
#     else:
#         await bot.send_message(1176527696,
#                                f'Сбой отмены такси!\nОтмените в приложении! \nТел: {await sql.get_num(id)}')
#
# # req = requests.get('https://business.taxi.yandex.ru/api/auth', headers={"Authorization": API_TAXI})
# # print(req.text)

res = {
    "items": [
        {
            "quantity": 1,
            'height ': 0.5,
            'length': 0.5,
            'width ': 0.5,
        }
    ],
    "requirements": {
        "taxi_class": 'express'
    },
    "route_points": [
        {
            "coordinates": [
                49.408787,
                53.518245
            ],
            "fullname": 'Россия, Тольятти, улица Комсомольская, 62c5'
        },
        {
            "coordinates": [
                49.390407,
                53.539377
            ],
            "fullname": 'Автозаводское шоссе, 10, Тольятти, Самарская область, Россия'
        }
    ],
    "skip_door_to_door": False
}


req = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price',
                    headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'}, json=res)
print(req.text)
