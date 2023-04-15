import requests
import json

import create__bot
from data import sql
from create__bot import API_TAXI, client_id, bot
import uuid
from keyboards import client_kb
from data import hms

# info = await sql.get_info(id)
async def draft_order(id):
    info = await sql.get_info(id)
    res = {
        "client_requirements": {
            "taxi_class": 'express'
        },
        "emergency_contact": {
            "name": 'Неизвестно',
            "phone": '+79649687004',
        },
        'items': [
            {
                "cost_currency": 'RUB',
                "cost_value": '200',
                "droppof_point": 2,
                "fiscalization": {
                    "mark": {
                        "code": 'groceries',
                        "kind": "- 444D00000000003741"
                    },
                },
                "pickup_point": 1,
                "quantity": 1,
                "size": {
                    "height": 0.5,
                    "length": 0.5,
                    "width": 0.5
                },
                "title": "Пакет",
            },
        ],
        "route_points": [
            {
                "address": {
                    'coordinates': [
                        49.408787,
                        53.518245
                    ],
                    "fullname": "Россия, Тольятти, улица Комсомольская, 62с5"
                },

                "contact": {
                    "email": "alimzhanov.2005@list.ru",
                    "name": "Unknown",
                    "phone": "+79649687004",
                },

                "external_order_cost": {
                    "currency": "RUB",
                    "currency_sign": "₽",
                    "value": "200.0"
                },


                "point_id": 1,
                "skip_confirmation": True,
                'type': 'source',
                "visit_order": 1
            },

            {
                "address": {
                    'coordinates': [
                        info[4],
                        info[5]
                    ],
                    "fullname": info[11],
                },

                "contact": {
                    "email": "example@gmail.com",
                    "name": "Неизвестно",
                    "phone": str(info[3]),
                },

                "external_order_cost": {
                    "currency": "RUB",
                    "currency_sign": "₽",
                    "value": "200.0"
                },

                "point_id": 2,
                "skip_confirmation": True,
                'type': 'destination',
                "visit_order": 2
            },
        ],
        "skip_client_notify": True,
        "skip_door_to_door": True,
        "skip_emergency_notify": True
    }

    par = uuid.uuid4()
    req = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/create?request_id={par}',
                        headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'}, json=res)
    #print('order: ', req.text)
    try:
        if str(req) == '<Response [200]>':
            obj = json.loads(req.text)
            a = str(obj['id'])
            await sql.add_offer(id, a)
    except Exception:
        await bot.send_message(create__bot.admin_id,
                               f'Сбой вызова такси:\nВам придется заказать такси самому: \nТел: {await sql.get_num(id)}')


async def proc_order(id):
    offer = await sql.get_offer(id)

    req = {
        "version": 1
    }

    rq = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/accept?claim_id={offer}',
                       headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'}, json=req)
    #print("proc: ", rq, rq.text)
    try:
        obj = json.loads(rq.text)
        if str(rq) == '<Response [409]>':
            await proc_order(id)
        elif str(rq) == '<Response [200]>':
            pass
    except Exception as e:
        await bot.send_message(create__bot.admin_id,
                               f'Сбой вызова такси:\nВам придется заказать такси самому: \nТел: {await sql.get_num(id)}')

#
async def cancel_order(id):

    offer = await sql.get_offer(id)
    rq = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/cancel-info?claim_id={offer}',
                       headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'})
    obj = json.loads(rq.text)
    a = str(obj['cancel_state'])
    #print(a)

    res = {
            "cancel_state": a,
            "version": 1
    }

    rq = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/cancel?claim_id={offer}',
                       headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'}, json=res)

    if str(rq) == '<Response [200]>':
        #print(rq, rq.text)
        pass
    else:
        return await bot.send_message(id, 'Не удалось отменить заказ\nОтмените  сами!!!')

async def state_order(id):

    offer = await sql.get_offer(id)


    rq = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/info?claim_id={offer}',
                       headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'})
    #print('status: ',rq, rq.text)
    try:
        obj = json.loads(rq.text)
        a = str(obj['route_points'][0]['visit_status'])

        if a == 'skipped':
            a = await hms.diff_lang(id, 'skipped')
        elif a == 'pending':
            a = await hms.diff_lang(id, 'pending')
        elif a in ['arrived', 'visited']:
            a = await hms.diff_lang(id, 'visited')
        return a
    except Exception:
        return '...'


# async def sharing_link(id):
#     offer = await sql.get_offer(id)
#     rq = requests.get(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/claims/tracking-links?claim_id={offer}',
#                        headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'})
#
#     print(rq.text, rq)
#     obj = json.loads(rq.text)
#     a = str(obj['route_points'][0]['sharing_link'])
#
#     return a




