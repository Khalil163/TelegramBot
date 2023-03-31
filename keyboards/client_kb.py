from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import create__bot
from data import sql
from aiogram.utils.callback_data import CallbackData
import requests
from create__bot import API_TAXI
import json
from aiogram.types.web_app_info import WebAppInfo

cb = CallbackData('clt', 'type', 'category', 'product', 'price')



claim_keyboard = InlineKeyboardMarkup()

claim_keyboard.add(InlineKeyboardButton(text='Проверить оплату',
                                                    callback_data='clt:claim:-:-:-'))


async def link(lin):
    link_b = InlineKeyboardButton('Местоположение', url=lin)
    kb = InlineKeyboardMarkup().add(link_b)
    return kb


async def acs_butt(id):
    price = (await sql.get_info(id))[6]
    b_y = InlineKeyboardButton('Подтвердить', callback_data=f'clt:pay_a:true:{id}:{price}')
    b_n = InlineKeyboardButton('Отклонить', callback_data=f'clt:pay_a:false:{id}:{price}')
    kb = InlineKeyboardMarkup(row_width=1).add(b_y).add(b_n)
    return kb


async def express(id):
    b_ord = InlineKeyboardButton('Заказать такси', callback_data=f'clt:taxi_o:{id}:-:-')
    kb = InlineKeyboardMarkup().add(b_ord)
    return kb


async def canc_express(id):
    b_ord = InlineKeyboardButton('Отменить такси', callback_data=f'clt:taxi_canc:{id}:-:-')
    b2_ord = InlineKeyboardButton('Завершить заказ', callback_data=f'clt:dv_finish:{id}:-:-')
    kb = InlineKeyboardMarkup(row_width=1).add(b2_ord).add(b_ord)
    return kb


async def fd_ready(id):
    b_ord = InlineKeyboardButton('Заказ готов', callback_data=f'clt:fd_ready:{id}:-:-')
    kb = InlineKeyboardMarkup().add(b_ord)
    return kb


async def kb_finish(id):
    b_ord = InlineKeyboardButton('Завершить заказ', callback_data=f'clt:dv_finish:{id}:-:-')
    kb = InlineKeyboardMarkup().add(b_ord)
    return kb


async def kb_pkp(id):
    b_ord = InlineKeyboardButton('Завершить заказ', callback_data=f'clt:pkp_finish:{id}:-:-')
    kb = InlineKeyboardMarkup().add(b_ord)
    return kb


site = InlineKeyboardButton('Сайт', url='https://lazzat-zhigulevskaja-ulitsa.clients.site')
site2 = InlineKeyboardButton('Меню',web_app=WebAppInfo(url='https://lazzat-zhigulevskaja-ulitsa.clients.site') )
#Zero = InlineKeyboardButton('Меню', url='https://sabyget.ru/shop/lazzat/catalog')
kb_info = InlineKeyboardMarkup(row_width=1).add(site)

b_state = KeyboardButton('Статус заказа')
kb_state = ReplyKeyboardMarkup(resize_keyboard=True).add(b_state)

b_menu = KeyboardButton('Меню')
b_order = KeyboardButton('Заказать')
b_loc = KeyboardButton('Поделиться 📍', request_location=True)
b_canc = KeyboardButton('Отмена')
b_time = KeyboardButton('Информация')
s_num = KeyboardButton('Поделиться номером', request_contact=True)
s_loc = KeyboardButton('Поделиться местоположением', request_location=True)

share_num = ReplyKeyboardMarkup(resize_keyboard=True).add(s_num).add(b_canc)

in_delivary = InlineKeyboardButton('Доставка', callback_data='Доставка')
in_self = InlineKeyboardButton('Самовывоз', callback_data='Самовывоз')
in_choice = InlineKeyboardMarkup(row_width=1).add(in_delivary).add(in_self)

share_loc = ReplyKeyboardMarkup(resize_keyboard=True).add(b_loc).add(b_canc)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_adm = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b_order).add(site2).insert(b_time)
kb_adm.add(b_order).add(site2, b_time).add(KeyboardButton('ModerMod'))

ib_right = InlineKeyboardButton('Да', callback_data='loc_right')
ib_err = InlineKeyboardButton('Нет', callback_data='loc_err')
kb_right = InlineKeyboardMarkup(row_width=1).row(ib_right, ib_err)

ib_y = InlineKeyboardButton('Да', callback_data='order_right')
ib_n = InlineKeyboardButton('Нет', callback_data='order_err')
draft_kb = InlineKeyboardMarkup(row_width=1).row(ib_y, ib_n)

b_buy = KeyboardButton('Купить')
b_empty_cart = KeyboardButton('Очистить корзину')
b_help = KeyboardButton('Назад')
kb_order = ReplyKeyboardMarkup(resize_keyboard=True).add(b_buy).row(b_empty_cart, b_help)

score = InlineKeyboardButton('Потратить баллы', callback_data='order_score_minus')

kb_order2 = InlineKeyboardMarkup().add(score)
kb_order3 = ReplyKeyboardMarkup(resize_keyboard=True).add(b_empty_cart)


async def items_ikb_clt():  # inline menu for client
    items_menu = await sql.get_items()
    items_case = InlineKeyboardMarkup(row_width=2)
    for i in items_menu:
        items_case.insert(InlineKeyboardButton(f'{i[0]}', callback_data=f'clt:show_clt_item:{i[0]}:-:-'))
    return items_case


async def in_plus_menu(filt, data):  # buy
    kb_i_menu = InlineKeyboardMarkup(row_width=2)

    for i in data:
        if str(i[2]) == str(filt) and i[3] == 'ЕСТЬ':
            kb_i_menu.insert(
                InlineKeyboardButton(f'{i[0]} 🔼', callback_data=f'clt:plus:{i[2]}:{i[0]}:{i[1]}'))
    return kb_i_menu.add(InlineKeyboardButton('Уменьшить', callback_data=f'clt:buy:minus_menu:-:-')). \
        insert(InlineKeyboardButton('Назад', callback_data='clt:buy:Назад:-:-'))


async def in_minus_menu(filt, data):  # buy
    kb_i_menu = InlineKeyboardMarkup(row_width=2)
    for i in data:
        if i[2] == filt and i[3] == 'ЕСТЬ':
            kb_i_menu.insert(
                InlineKeyboardButton(f'{i[0]} 🔽', callback_data=f'clt:minus:{i[2]}:{i[0]}:{i[1]}'))
    return kb_i_menu.add(InlineKeyboardButton('Увеличить', callback_data='clt:buy:plus_menu:-:-')). \
        insert(InlineKeyboardButton('Назад', callback_data='clt:buy:Назад:-:-'))


async def get_price(user_id):
    mas = await sql.get_info(user_id)
    long = mas[4]
    lat = mas[5]

    # data = {
    #     "items": [
    #         {
    #             "quantity": 1,
    #             'height ': 0.5,
    #             'length': 0.5,
    #             'width ': 0.5,
    #         }
    #     ],
    #     "requirements": {
    #         "taxi_class": 'express'
    #     },
    #     "route_points": [
    #         {
    #             "coordinates": [
    #                 49.408787,
    #                 53.518245
    #             ],
    #             "fullname": 'Россия, Тольятти, улица Комсомольская, 62c5'
    #         },
    #         {
    #             "coordinates": [
    #                 long,
    #                 lat
    #             ],
    #             "fullname": f'{mas[11]}'
    #         }
    #     ],
    #     "skip_door_to_door": False
    # }
    #
    # res = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price',
    #                     headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'}, json=data)
    #
    # print(long, lat, mas[11])
    # print(res.text)
    # obj = json.loads(res.text)
    # a = str(obj['distance_meters'])
    # print('distance 1 : ', float(a)/1000, 'merets')

    # print('distance 2 : ', GD(point1,point2) / 1000, 'merets')

    data = {
        "route": [
            [
                49.408787,
                53.518245
            ],
            [
                long,
                lat
            ]
        ],

        "requirements": {
            "nosmoking": False,
            "conditioner": False
        },

        "phone": "+79649687004",
        "selected_class": "express"
    }

    res = requests.post(f'https://business.taxi.yandex.ru/api/1.0/estimate',
                        headers={"Authorization": API_TAXI}, json=data)
    print(res.text)
    obj = json.loads(res.text)
    a = str(obj['service_levels'][0]['price']).replace('руб.', '')
    print('price 2 : ', a)
    a = await round_int(int(a))
    return a


async def check(delivery, id):
    load = await sql.get_cart(id)
    score = await sql.get_score(id)

    old = ''
    sum = 0



    for i in load:
        old += '<u>{0:<1}</u>  {1:^1} * {2:^1}р {3:^1} {4:>1}р\n'.format(i[1], i[2], i[3], '=', i[2] * i[3])
        sum += int(i[2]) * int(i[3])
    if int(delivery) == 0:
        old += '\n<b>Ваши баллы:</b>{:5}\n<b>Итого:</b>{:5}р\n'.format(score, sum)
    else:
        data = await sql.get_info(id)
        address = data[11]
        address = str(address).split(',')
        geo = address[0] + ' ' + address[1]
        sum += int(delivery)
        old += '\n<b>Ваши баллы:</b>{:5}\n<b>Доставка:</b>{:5}р\n<b>Итого:</b>{:5}р\n\n<b>Адрес:</b> {:5}\n'.format(score,delivery, sum, geo)
    return old

async def total_price(id):
    delivery = await sql.get_deliv(id)
    load = await sql.get_cart(id)
    sum = 0

    for i in load:
        sum += int(i[2]) * int(i[3])
    sum += int(delivery)
    return sum



async def round_int(val):
    if val % 10 != 0:
        val = val * 1.2 - ((val * 1.2) % 10) + 10
    return val


async def score_check(id, score):
    load = await sql.get_cart(id)
    old = ''
    delivery = await sql.get_delivery(id)
    sum = 0

    for i in load:
        old += '<u>{0:<1}</u>  {1:^1} * {2:^1}р {3:^1} {4:>1}р\n'.format(i[1], i[2], i[3], '=', i[2] * i[3])
        sum += int(i[2]) * int(i[3])
    if int(delivery) == 0:
        if score > sum:
            score2 = score
            score = sum//2
            old += '\n<b>Итого:</b>{:5}р - {:5}(баллы) = {:5}\n'.format(sum, score,sum-score)
            await sql.add_score(id, score2 - score)
        else:
            old += '\n<b>Итого:</b>{:5}р - {:5}(баллы) = {:5}\n'.format(sum, score,sum-score)
            await sql.add_score(id, 0)
    else:
        sum += int(delivery)
        if score > sum:
            score2 = score
            score = sum//2
            old += '\n<b>Доставка:</b>{:5}р\n<b>Итого:</b>{}р - {}(баллы) = {}р\n'.format(int(delivery), sum, score,sum-score)
            await sql.add_score(id, score2 - score)
        else:
            old += '\n<b>Доставка:</b>{:5}р\n<b>Итого:</b>{:5}р - {:5}(баллы) = {:5}р\n'.format(int(delivery), sum, score,sum-score)
            await sql.add_score(id, 0)



    return old