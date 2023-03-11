import pytz
from aiogram import types, Dispatcher
from create__bot import dp
from data import sql
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from keyboards import client_kb
from create__bot import bot
from datetime import datetime, time
from geopy import Yandex
from create__bot import api_geo
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

tz_tlt = pytz.timezone('Europe/Samara')
lim1 = time(9, 30)
lim2 = time(22, 0)


async def work_time():
    time_tlt = datetime.now(tz_tlt).time()
    if lim1 <= time_tlt <= lim2:
        return True
    else:
        return False


class FSMUsers(StatesGroup):
    load = State()
    start = State()
    loc = State()
    number = State()


class FSMPickup(StatesGroup):
    start = State()
    bill = State()


cb = client_kb.cb


# @dp.message_handler(commands=['start', 'help'])
async def hi_send(message: types.Message):
    if await sql.is_moder(message.from_user.id) == 'admin':
        await message.answer(f"Привет, {message.from_user.first_name}! 👋", reply_markup=client_kb.kb_adm)
    else:
        await message.answer(f"Привет, {message.from_user.first_name}! 👋",
                             reply_markup=client_kb.kb_client)


async def ask_buy(message: types.Message):
    if await work_time():
        if await sql.is_moder(message.from_user.id) is False:
            await sql.add_user(message.from_user.first_name, message.from_user.id, 'client')
        try:
            if int(await sql.get_state(message.from_user.id)) == 0:
                await message.answer('Формат заказа:', reply_markup=client_kb.in_choice)
        except ValueError:
            await message.answer('Извините, у вас уже есть открытый заказ.\nПо вопросам звонить: +79649687004')
    else:
        await message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


# @dp.callback_query_handler(text='Доставка')
async def get_loc(call: types.CallbackQuery):
    if await work_time():
        await call.message.edit_reply_markup()
        await bot.send_message(call.from_user.id, 'Ваш выбор: Доставка')
        await bot.send_message(call.from_user.id, 'Поделитесь местоположением или напишите адрес',
                               reply_markup=client_kb.share_loc)
        await FSMUsers.load.set()
    else:
        await call.message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


# @dp.message_handler(content_types=['location'])
async def set_loc(message: types.Message, state: FSMContext):
    if await work_time():
        if message.location is not None:
            locate = Yandex(api_key=api_geo).reverse("%s, %s" % (message.location.latitude, message.location.longitude))
            await message.answer(f'Это ваш адрес?\n{locate}', reply_markup=client_kb.kb_right)
            await sql.add_loc(message.from_user.id, message.location.longitude, message.location.latitude)
            delivery = int(await client_kb.get_price(message.from_user.id))
            await sql.add_deliv(message.from_user.id, delivery)
            await sql.add_address(message.from_user.id, f'{locate}')
            await FSMUsers.start.set()
        else:
            locate = Yandex(api_key=api_geo).geocode(f'{message.text}, Тольятти, Россия')
            if str(locate.address).split(',')[0] == 'Тольятти':
                return await message.answer('Указан неверный адрес\nВведите адрес:')
            await sql.add_loc(message.from_user.id, locate.longitude, locate.latitude)
            delivery = int(await client_kb.get_price(message.from_user.id))
            await sql.add_deliv(message.from_user.id, delivery)
            await message.answer(f'Это ваш адрес?\n{locate.address}', reply_markup=client_kb.kb_right)
            await sql.add_address(message.from_user.id, f'{locate.address}')
            await FSMUsers.start.set()
    else:
        await message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


async def cancel_hand(message: types.Message, state: FSMContext):
    to_state = await state.get_state()
    if to_state is None:
        return
    if await sql.is_moder(message.from_user.id) == 'admin':
        await message.answer('ОК', reply_markup=client_kb.kb_adm)
    else:
        await message.answer('ОК', reply_markup=client_kb.kb_client)
    await state.finish()


async def right_num(call: types.CallbackQuery, state: FSMContext):
    if await work_time():
        if call.data == 'loc_right':
            await call.answer()
            await call.message.edit_reply_markup()
            await bot.send_message(call.from_user.id, 'Ваш выбор: Да')
            await bot.send_message(call.from_user.id, 'Отлично, теперь мне нужен ваш номер:',
                                   reply_markup=client_kb.share_num)
            await FSMUsers.number.set()
        else:
            await call.answer()
            await call.message.edit_reply_markup()
            await bot.send_message(call.from_user.id, 'Ваш выбор: Нет')
            await bot.send_message(call.from_user.id, 'Хорошо. Введите адрес:\nПример: Жигулевская 11')
            await FSMUsers.load.set()
    else:
        await call.message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


async def set_num(message: types.Message, state: FSMContext):
    if await work_time():
        try:
            if (message.text.startswith('+79') and len(message.text) == 12) or (message.text.startswith('89') and
                                                                                len(message.text) == 11):
                try:
                    await sql.add_num(message.from_user.id, f'{message.contact.phone_number}')
                except AttributeError:
                    await sql.add_num(message.from_user.id, message.text)
                await message.answer('Теперь выберите блюда', reply_markup=client_kb.kb_order)

                msg_cart = await message.answer('Меню: ', reply_markup=await client_kb.items_ikb_clt())
                await sql.add_msg(message.from_user.id, msg_cart.message_id)

                await state.finish()

            else:
                return await message.answer('Некорректный формат:\nВведите ваш номер')

        except AttributeError:
            await sql.add_num(message.from_user.id, message.contact.phone_number)
            await message.answer('Теперь выберите блюда', reply_markup=client_kb.kb_order)

            msg_cart = await message.answer('Меню: ', reply_markup=await client_kb.items_ikb_clt())
            await sql.add_msg(message.from_user.id, msg_cart.message_id)
            # delivery = await client_kb.get_price(message.from_user.id)
            #
            # await sql.add_deliv(message.from_user.id, delivery)
            await state.finish()
    else:
        await message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


# @dp.register_callback_query_handler(lambda call: call.data.startswith('client'))
async def show_menu(call: types.CallbackQuery, callback_data: dict):
    if await work_time():
        wait = await sql.sql_read_menu()
        category = callback_data.get('category')
        await sql.add_cat(call.from_user.id, category)
        await call.message.edit_reply_markup(
            reply_markup=await client_kb.in_plus_menu(callback_data.get('category'), wait))
    else:
        await call.message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


async def show_plus_minus(call: types.CallbackQuery, callback_data: dict):
    if callback_data.get('category') == 'Назад':
        await call.message.edit_reply_markup(reply_markup=await client_kb.items_ikb_clt())
        await call.answer()

    elif callback_data.get('category') == 'minus_menu':
        wait = await sql.sql_read_menu()
        category = await sql.get_info(call.from_user.id)
        category = str(category[8])
        await call.message.edit_reply_markup(reply_markup=await client_kb.in_minus_menu(category, wait))
        await call.answer()

    elif callback_data.get('category') == 'plus_menu':
        wait = await sql.sql_read_menu()
        category = await sql.get_info(call.from_user.id)
        category = category[8]
        await call.message.edit_reply_markup(reply_markup=await client_kb.in_plus_menu(category, wait))
        await call.answer()


async def add_cart(call: types.CallbackQuery, callback_data: dict):
    count = await sql.get_count_cart(call.from_user.id, callback_data.get('product'))
    if count:
        cnt = count[0][0] + 1
        await sql.change_count(call.from_user.id, callback_data.get('product'), cnt)
    else:
        await sql.add_cart(call.from_user.id, callback_data.get('product'), callback_data.get('price'))
    wait = await sql.sql_read_menu()
    delivery = await sql.get_info(call.from_user.id)
    delivery = delivery[6]
    old = await client_kb.check(delivery, call.from_user.id)
    msg_cart = await sql.get_info(call.from_user.id)
    msg_cart = msg_cart[7]
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_cart,
                                text=f'<b>Корзина:</b> \n{old}\n<b>Меню:</b>', parse_mode='html',
                                reply_markup=await client_kb.in_plus_menu(callback_data.get('category'), wait))


async def minus_cart(call: types.CallbackQuery, callback_data: dict):
    count = await sql.get_count_cart(call.from_user.id, callback_data.get('product'))
    if count:
        cnt = count[0][0] - 1
        if cnt <= 0:
            await sql.remove_one_item(call.from_user.id, callback_data.get('product'))
        else:
            await sql.change_count(call.from_user.id, callback_data.get('product'), cnt)

        wait = await sql.sql_read_menu()
        delivery = await sql.get_info(call.from_user.id)
        delivery = delivery[6]
        msg_cart = await sql.get_info(call.from_user.id)
        msg_cart = msg_cart[7]
        old = await client_kb.check(delivery, call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_cart,
                                    text=f'<b>Корзина:</b> \n{old}\n<b>Меню:</b>', parse_mode='html',
                                    reply_markup=await client_kb.in_minus_menu(callback_data.get('category'), wait))
    else:
        await call.answer('Нельзя уменьшить')


async def empty_cart(message: types.Message):
    msg_cart = await sql.get_info(message.from_user.id)
    msg_cart = msg_cart[7]
    await sql.empty_cart(message.from_user.id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=msg_cart)
    await message.answer('Корзина очищена')
    msg_cart = await message.answer('Меню', reply_markup=await client_kb.items_ikb_clt())
    await sql.add_msg(message.from_user.id, msg_cart.message_id)


async def deliv_self(call: types.CallbackQuery):
    await sql.add_deliv(call.from_user.id, 0)
    await bot.send_message(call.from_user.id, 'Отлично, теперь мне нужен ваш номер:', reply_markup=client_kb.share_num)
    await call.answer()
    await FSMUsers.number.set()


async def draft_buy(message: types.Message):
    if await work_time():
        delivery = (await sql.get_info(message.from_user.id))[6]
        old = await client_kb.check(delivery, message.from_user.id)
        await bot.send_message(message.from_user.id, f'<b>Ваш заказ:</b>\n\n{old}', parse_mode='html')
        await bot.send_message(message.from_user.id, 'Оформляем заказ?', reply_markup=client_kb.draft_kb)
    else:
        await message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


# @dp.callback_query_handler(Text(startswith='order'), state=None)
async def ask_pay(call: types.CallbackQuery):
    if await work_time():
        if call.data == 'order_right':
            await call.message.delete()
            await bot.send_message(call.from_user.id,
                                   'Реквизиты для оплаты (Сбербанк):\n\nТел: *+79879459755*\nКарта: `2202 2061 9330 '
                                   '0691`\nФИО: ХАЛИЛИЛЛОХ МАНАПЖАНОВИЧ A.\n\nНажмите на номер для '
                                   'копирования!\n\nЖду чек перевода ...',
                                   reply_markup=ReplyKeyboardRemove(), parse_mode='MarkDown')
            await call.answer()
            await FSMPickup.bill.set()
        else:
            await call.message.delete()
            await bot.send_message(call.from_user.id, 'Заказ отменен.\nБудем ждать вашего заказа!',
                                   reply_markup=client_kb.kb_client)
            await call.answer()
            await sql.empty_cart(call.from_user.id)
    else:
        await call.message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


# @dp.message_handler(state=FSMPickup.bill)
async def answer_q3(message: types.Message, state: FSMContext):
    if await work_time():
        delivery = (await sql.get_info(message.from_user.id))
        old = await client_kb.check(int(delivery[6]), message.from_user.id)
        num = str(delivery[3])
        if num[0] == '7':
            num = '+' + num

        if int(delivery[6]) > 0:
            locate = await sql.get_address(message.from_user.id)
            text = f'Доставка:\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Не подтвержден'
        else:
            text = f'Cамовывоз:\n{old}\nТел: {num}\n\nСтатус: Не подтвержден'

        if message.text is not None:
            return await bot.send_message(message.from_user.id, 'Отправьте чек!')

        elif message.photo is not None:
            try:
                msg = await bot.send_photo(chat_id=5412070881, photo=message.photo[-1].file_id,
                                           caption=text, parse_mode='html',
                                           reply_markup=await client_kb.acs_butt(message.from_user.id))
                await sql.add_msg(message.from_user.id, msg.message_id)
            except IndexError:
                msg = await bot.send_document(chat_id=5412070881, document=message.document.file_id,
                                              caption=text, parse_mode='html',
                                              reply_markup=await client_kb.acs_butt(message.from_user.id))
                await sql.add_msg(message.from_user.id, msg.message_id)

        await bot.send_message(message.from_user.id, 'Проверяем оплату\nПару минут...')
        await state.finish()

    else:
        await message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')


# @dp.message_handler(text='Информация')
async def info_lazzat(message: types.Message):
    await message.answer(
        '<b>Кафе Лаззат:</b>\n\n<b>Адрес:</b> ул. Жигулевская 11 г. Тольятти\n<b>Режим работы:</b> 09:30 - '
        '22:00\n<b>Тел:</b> +79649687004 '
        '\n\nЭтот бот создан для заказа еды, если есть сомнения позвоните по официальному номеру на сайте и уточните '
        'id бота.\n\nМеню с опсианием и картинками ниже по ссылке\n\n<b>Создатель бота:</b> @ZeRo_163',
        reply_markup=client_kb.kb_info, parse_mode='html')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(hi_send,
                                lambda message: message.text in ['/start', '/help', 'Режим клиента', 'Привет', 'Hi',
                                                                 'Здравствуйте', 'Назад'])
    dp.register_callback_query_handler(get_loc, text='Доставка', state=None)
    dp.register_callback_query_handler(deliv_self, text='Самовывоз', state=None)
    dp.register_message_handler(cancel_hand, state="*", commands='Отмена')
    dp.register_message_handler(cancel_hand, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(set_loc, content_types=['location', 'text'], state=FSMUsers.load)
    dp.register_callback_query_handler(right_num, text=['loc_err', 'loc_right'], state=FSMUsers.start)
    dp.register_message_handler(set_num, content_types=['contact', 'text'], state=FSMUsers.number)
    dp.register_callback_query_handler(show_menu, cb.filter(type='show_clt_item'))
    dp.register_callback_query_handler(show_plus_minus, cb.filter(type='buy'))
    dp.register_callback_query_handler(add_cart, cb.filter(type='plus'))
    dp.register_callback_query_handler(minus_cart, cb.filter(type='minus'))
    dp.register_message_handler(answer_q3, content_types=['photo', 'text', 'document'], state=FSMPickup.bill)
    dp.register_callback_query_handler(ask_pay, Text(startswith='order'), state=None)
    dp.register_message_handler(empty_cart, Text('Очистить корзину'))
    dp.register_message_handler(ask_buy, Text('Заказать'))
    dp.register_message_handler(draft_buy, Text('Купить'))
    dp.register_message_handler(info_lazzat, text='Информация')
