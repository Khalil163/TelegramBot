from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import sql
from aiogram.utils.callback_data import CallbackData
import requests
from create__bot import API_TAXI
import json


cb = CallbackData('clt', 'type', 'category', 'product', 'price')


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


site = InlineKeyboardButton('Сайт', url='https://yandex.ru/maps/org/lazzat/36507547565/?ll=49.408934%2C53.518607&z=12')
Zero = InlineKeyboardButton('Меню', url='https://sabyget.ru/shop/lazzat/catalog')
kb_info = InlineKeyboardMarkup(row_width=1).add(site).add(Zero)


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

kb_client.add(b_order).add(b_loc).insert(b_time)
kb_adm.add(b_order).add(b_loc, b_time).add(KeyboardButton('ModerMod'))

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


async def items_ikb_clt():  # inline menu for client
    items_menu = await sql.get_items()
    items_case = InlineKeyboardMarkup(row_width=2)
    for i in items_menu:
        items_case.insert(InlineKeyboardButton(f'{i[0]}', callback_data=f'clt:show_clt_item:{i[0]}:-:-'))
    return items_case


async def in_plus_menu(filt, data):  # buy
    kb_i_menu = InlineKeyboardMarkup(row_width=2)
    for i in data:
        if i[2] == filt and i[3] == 'ЕСТЬ':
            kb_i_menu.insert(InlineKeyboardButton(f'{i[0]} - {i[1]}р 🔼', callback_data=f'clt:plus:{i[2]}:{i[0]}:{i[1]}'))
    return kb_i_menu.add(InlineKeyboardButton('Уменьшить', callback_data=f'clt:buy:minus_menu:-:-')).\
        insert(InlineKeyboardButton('Назад', callback_data='clt:buy:Назад:-:-'))


async def in_minus_menu(filt, data):  # buy
    kb_i_menu = InlineKeyboardMarkup(row_width=2)
    for i in data:
        if i[2] == filt and i[3] == 'ЕСТЬ':
            kb_i_menu.insert(InlineKeyboardButton(f'{i[0]} - {i[1]}р 🔽', callback_data=f'clt:minus:{i[2]}:{i[0]}:{i[1]}'))
    return kb_i_menu.add(InlineKeyboardButton('Увеличить', callback_data='clt:buy:plus_menu:-:-')).\
        insert(InlineKeyboardButton('Назад', callback_data='clt:buy:Назад:-:-'))


async def get_price(user_id):
    mas = await sql.get_info(user_id)
    long = mas[4]
    lat = mas[5]
    number = mas[0][3]

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
                    long,
                    lat
                ],
                "fullname": f'{mas[11]}'
            }
        ],
        "skip_door_to_door": False 
    }

    res = requests.post(f'https://b2b.taxi.yandex.net/b2b/cargo/integration/v2/check-price',
                        headers={"Authorization": f'Bearer {API_TAXI}', 'Accept-Language': 'ru'}, json=res)

    print(long, lat, mas[11])
    print(res.text)
    obj = json.loads(res.text)
    a = str(obj['price'])
    print(a)
    return a


async def check(delivery, id):
    load = await sql.get_cart(id)
    old = ''
    sum = 0

    for i in load:
        old += '<u>{0:<1}</u>  {1:^1} * {2:^1} {3:^1} {4:>1}\n'.format(i[1], i[2], i[3], '=', i[2] * i[3])
        sum += int(i[2]) * int(i[3])
    if int(delivery) == 0:
        old += '\n<b>Итого:</b>{:5}\n'.format(sum)
    else:
        sum += int(delivery)
        old += '\n<b>Доставка:</b>{:5}\n<b>Итого:</b>{:5}\n'.format(int(delivery), sum)
    return old