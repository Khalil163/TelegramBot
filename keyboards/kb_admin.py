from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import sql


cb = CallbackData('adm', 'type', 'category', 'product', 'state')

b_edit_menu = KeyboardButton('Добавить блюдо')
b_edit_item = KeyboardButton('Добавить раздел')
b_del = KeyboardButton('Удалить')
b_stop = KeyboardButton('Стоп лист')
admin_case = ReplyKeyboardMarkup(resize_keyboard=True).add(b_edit_menu, b_edit_item).add(b_del, b_stop).add(KeyboardButton('Режим клиента'))

b_canc = KeyboardButton('Отмена')
kb_canc = ReplyKeyboardMarkup(resize_keyboard=True).add(b_canc)

b_st = InlineKeyboardButton('ЕСТЬ', callback_data='ЕСТЬ')
b_sp = InlineKeyboardButton('НЕТ', callback_data='НЕТ')
stop_case = InlineKeyboardMarkup(row_width=1).add(b_st, b_sp)


in_del_item = InlineKeyboardButton('Раздел', callback_data='adm:delete:item:-:-')
in_del_food = InlineKeyboardButton('Блюдо', callback_data='adm:delete:food:-:-')
del_in_kb = InlineKeyboardMarkup(row_width=1).insert(in_del_item).insert(in_del_food)


async def items_in():
    items_case = InlineKeyboardMarkup(row_width=2)
    items_menu = await sql.get_items()
    for i in items_menu:
        items_case.insert(InlineKeyboardButton(f'{i[0]}', callback_data=f'adm:set_item:{i[0]}:-:-'))
    return items_case


async def items_in_stop():
    items_case = InlineKeyboardMarkup(row_width=2)
    items_menu = await sql.get_items()
    for i in items_menu:
        items_case.insert(InlineKeyboardButton(f'{i[0]}', callback_data=f'adm:items_stop:{i[0]}:-:-'))
    return items_case


async def items_i_del():
    items_case = InlineKeyboardMarkup(row_width=2)
    items_menu = await sql.get_items()
    for i in items_menu:
        items_case.insert(InlineKeyboardButton(f'{i[0]}', callback_data=f'adm:show_items_del:{i[0]}:-:-'))
    return items_case


async def items_i_d():
    items_case = InlineKeyboardMarkup(row_width=2)
    items_menu = await sql.get_items()
    for i in items_menu:
        items_case.insert(InlineKeyboardButton(f'{i[0]}', callback_data=f'adm:del_item:{i[0]}:-:-'))
    return items_case


def in_stop(filt, data):
    kb_i_menu = InlineKeyboardMarkup(row_width=2)
    for i in data:
        if i[2] == filt:
            kb_i_menu.add(InlineKeyboardButton(f'{i[0]} - {i[3]}', callback_data=f'adm:edit_stop:{i[2]}:{i[0]}:{i[3]}'))
    return kb_i_menu.insert(InlineKeyboardButton('Назад', callback_data='adm:edit_stop:-:Назад:-'))


async def in_del_m(filt, data):
    kb_i_menu = InlineKeyboardMarkup(row_width=2)
    for i in data:
        if i[2] == filt:
            kb_i_menu.add(InlineKeyboardButton(f'{i[0]} - {i[1]}р', callback_data=f'adm:del_food:{i[2]}:{i[0]}:{i[3]}'))
    return kb_i_menu.insert(InlineKeyboardButton('Назад', callback_data='adm:del_food:-:Назад:-'))
