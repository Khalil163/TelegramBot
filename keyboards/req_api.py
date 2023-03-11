import requests
import json
from data import sql
from create__bot import API_TAXI, client_id, bot
from keyboards import client_kb


async def draft_order(id):
    info = await sql.get_info(id)
    res = {
        "comment": "Кафе Лаззат. Зеленые ворота",
        "source": {
            "country": "Россия",
            "short_text_to": "Тольятти, Комсомольская 62с5",
            "geopoint": [
                49.408787,
                53.518245
            ],
            "extra_data": {
                "contact_phone": "+79649687004",
            }
        },
        'offer': f'{info[9]}',
        "class": "express",
        "requirements": {"door_to_door": False},
        "destination": {
            "country": "Россия",
            "geopoint": [
                int(info[4]),
                int(info[5])
            ],
            "extra_data": {
                "contact_phone": f"{info[3]}",
            },
        }
    }

    rq = requests.post(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/',  headers={"Authorization": API_TAXI}, json=res)
    print(rq.text)
    if rq == 200:
        obj = json.loads(rq.text)
        a = str(obj['id'])
        await sql.add_offer(id,a)
    # else:
    #     await bot.send_message(1176527696, f'Сбой такси:\nВам придется заказать такси самому: \nТел: {await sql.get_num(id)}')


async def proc_order(id):
    offer = await sql.get_offer(id)
    rq = requests.post(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/{offer}/processing',
                       headers={"Authorization": API_TAXI})
    if rq == 200:
        obj = json.loads(rq.text)
        a = str(obj['status']['description'])
        return a
    elif rq == 406:
        await client_kb.get_price(id)
        await draft_order(id)
        await proc_order(id)
    # else:
    #     await bot.send_message(1176527696, f'Сбой вызова такси:\nВам придется заказать такси самому: \nТел: {await sql.get_num(id)}')



async def cancel_order(id):
    pass
    # offer = await sql.get_offer(id)
    # rq = requests.get(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/{offer}?show_cancel_text=true',
    #                    headers={"Authorization": API_TAXI})
    # obj = json.loads(rq.text)
    # state = str(obj['cancel_rules']['state'])
    # js = {
    #     'state': str(state)
    # }
    #
    # rq = requests.get(f'https://business.taxi.yandex.ru/api/1.0/client/{client_id}/order/{offer}/cancel',
    #                   headers={"Authorization": API_TAXI}, json=js)
    # if rq == 200:
    #     pass
    # else:
    #     await bot.send_message(1176527696,
    #                            f'Сбой отмены такси!\nОтмените в приложении! \nТел: {await sql.get_num(id)}')


# req = requests.get('https://business.taxi.yandex.ru/api/auth', headers={"Authorization": API_TAXI})
# print(req.text)
