import pytz
from aiogram import types, Dispatcher
import create__bot
from data import sql, menu
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import client_kb
from create__bot import bot
from datetime import datetime, time
from geopy import Yandex
from create__bot import api_geo, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from geopy.distance import geodesic as GD
from data import sber, hms

tz_tlt = pytz.timezone('Europe/Samara')
lim1 = time(9, 15)
lim2 = time(23, 50)
sber_photo = 'AgACAgIAAxkDAAIHV2Q5iS1yosadm_pOkBr0HoFmpNmZAAKJyTEbIK3JSbbsIO2UZs_AAQADAgADcwADLwQ'


async def work_time():
    time_tlt = datetime.now(tz_tlt).time()
    if lim1 <= time_tlt <= lim2:
        return True
    else:
        return False


class orderState(StatesGroup):
    lang = State()
    format_order = State()
    choice_delivery = State()
    choice_pickup = State()
    set_loc = State()
    num = State()
    set_nm = State()
    menu = State()
    ask_order = State()
    get_order = State()
    wait = State()


cb = client_kb.cb



# @dp.message_handler(commands=['start', 'help'])
async def hi_send(message: types.Message, state: FSMContext):
    # await menu.write_menu()
    if await sql.is_moder(message.from_user.id) is False:
        await sql.add_user(message.from_user.first_name, message.from_user.id, 'client')

    await del_twice_message(message.from_user.id)
    text = await hms.diff_lang(message.from_user.id, 'hi')
    await message.answer(text.format(message.from_user.first_name),
                         reply_markup=await client_kb.start_kb(message.from_user.id))
    msg = await message.answer('Выберите язык:', reply_markup=client_kb.locales)
    await sql.add_msg(message.from_user.id, msg.message_id)


# @dp.callback_query_handler(Text(startswith='loc')) #FSM - lang
async def set_lang(call: types.CallbackQuery):
    lang = call.data.split('_')[1]

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    if lang == 'ru':
        await sql.add_lang(call.from_user.id, 'ru')
        await call.message.answer('Хорошо, я постараюсь разговаривать на русском языке.',
                                  reply_markup=await client_kb.start_kb(call.from_user.id))
    elif lang == 'uz':
        await sql.add_lang(call.from_user.id, 'uz')
        await call.message.answer('OK, men o\'zbek tilida gaplashishga harakat qilaman',
                                  reply_markup=await client_kb.start_kb(call.from_user.id))
    elif lang == 'tz':
        await sql.add_lang(call.from_user.id, 'tz')
        await call.message.answer('Хуб, ман кӯшиш мекунам, ки бо забони тоҷикӣ сӯҳбат кунам.',
                                  reply_markup=await client_kb.start_kb(call.from_user.id))




async def del_twice_message(id):
    try:
        msg = await sql.get_msg(id)
        msg1 = str(msg).split('x')[0]
        msg2 = str(msg).split('x')[1]
        await bot.delete_message(chat_id=id, message_id=msg1)
        await bot.delete_message(chat_id=id, message_id=msg2)
    except Exception as e:
        try:
            msg = await sql.get_msg(id)
            await bot.delete_message(chat_id=id, message_id=msg)
        except Exception as e:
            pass


# FSM - format_order
async def ask_buy(message: types.Message, state: FSMContext):
    if not await work_time():
        text = await hms.diff_lang(message.from_user.id, 'time_out')
        return await message.answer(
            text,
            parse_mode='html')

    if await sql.is_moder(message.from_user.id) is False:
        await sql.add_user(message.from_user.first_name, message.from_user.id, 'client')



    await del_twice_message(message.from_user.id)

    text = await hms.diff_lang(message.from_user.id, 'format_order')
    msg = await message.answer(text, reply_markup=await client_kb.in_choice(message.from_user.id))
    await sql.add_msg(message.from_user.id, msg.message_id)
    await orderState.choice_delivery.set()


# FSM - choice_delivery
# @dp.callback_query_handler(text='Доставка')
async def get_loc(call: types.CallbackQuery):
    if not await work_time():
        text = await hms.diff_lang(call.from_user.id, 'time_out')
        return await call.message.answer(
            text,
            parse_mode='html')

    await call.message.edit_reply_markup()
    text = await hms.diff_lang(call.from_user.id, 'choice_deliv')
    text2 = await hms.diff_lang(call.from_user.id, 'get_loc')

    await bot.send_message(call.from_user.id, text)
    await bot.send_message(call.from_user.id, text2,
                           reply_markup=await client_kb.share_kb(call.from_user.id))
    await orderState.set_loc.set()


# FSM - set_loc
# @dp.message_handler(content_types=['location'])
async def set_loc(message: types.Message, state: FSMContext):
    if not await work_time():
        return await message.answer(
            '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
            parse_mode='html')

    point1 = (53.518245, 49.408787)
    loc_out = await hms.diff_lang(message.from_user.id, 'loc_out')
    text = await hms.diff_lang(message.from_user.id, 'set_loc')

    if message.location is not None:
        point2 = (message.location.latitude, message.location.longitude)

        if GD(point1, point2) <= 25:
            locate = Yandex(api_key=api_geo).reverse(
                "%s, %s" % (message.location.latitude, message.location.longitude))

            await message.answer(text.format(locate), reply_markup=await client_kb.kb_right(message.from_user.id))

            await sql.add_loc(message.from_user.id, message.location.longitude, message.location.latitude)
            await sql.add_address(message.from_user.id, f'{locate}')
            delivery = int(await client_kb.get_price(message.from_user.id))
            await sql.add_deliv(message.from_user.id, delivery)

            await orderState.num.set()
        else:
            return await message.answer(loc_out)

    else:
        locate = Yandex(api_key=api_geo).geocode(f'{message.text}, Тольятти, Россия')
        point2 = (locate.latitude, locate.longitude)

        if GD(point1, point2) >= 25 or str(locate.address).split(',')[0] == 'Тольятти':
            return await message.answer(loc_out)

        await message.answer(text.format(locate.address), reply_markup=await client_kb.kb_right(message.from_user.id))
        await sql.add_loc(message.from_user.id, locate.longitude, locate.latitude)
        await sql.add_address(message.from_user.id, f'{locate.address}')
        delivery = int(await client_kb.get_price(message.from_user.id))
        await sql.add_deliv(message.from_user.id, delivery)

        await orderState.num.set()


async def cancel_hand(message: types.Message, state: FSMContext):
    to_state = await state.get_state()
    if to_state is None:
        await del_twice_message(message.from_user.id)
        await sql.add_state(message.from_user.id, 0)
        await sql.empty_cart(message.from_user.id)
        text = await hms.diff_lang(message.from_user.id, 'canc_text')
        return await message.answer(text, reply_markup=await client_kb.start_kb(message.from_user.id))
    if await sql.is_moder(message.from_user.id) == 'admin':
        await message.answer('ОК', reply_markup=await client_kb.start_kb(message.from_user.id))
    else:
        await message.answer('ОК', reply_markup=await client_kb.start_kb(message.from_user.id))
    await state.finish()


async def right_num(call: types.CallbackQuery, state: FSMContext):
    if not await work_time():
        text = await hms.diff_lang(call.from_user.id, 'time_out')
        return await call.message.answer(text,
                                         parse_mode='html')

    if call.data == 'loc_right':
        await call.answer()
        await call.message.edit_reply_markup()
        loc_yes = await hms.diff_lang(call.from_user.id, 'loc_yes')
        get_num = await hms.diff_lang(call.from_user.id, 'get_num')
        await bot.send_message(call.from_user.id, loc_yes)
        await bot.send_message(call.from_user.id, get_num,
                               reply_markup=await client_kb.share_num(call.from_user.id))
        await orderState.set_nm.set()
    else:
        await call.answer()
        await call.message.edit_reply_markup()
        loc_no = await hms.diff_lang(call.from_user.id, 'loc_no')
        get_loc = await hms.diff_lang(call.from_user.id, 'get_loc')
        await bot.send_message(call.from_user.id, loc_no)
        await bot.send_message(call.from_user.id, get_loc, reply_markup=await client_kb.share_kb(call.from_user.id))
        await orderState.set_loc.set()


async def set_num(message: types.Message, state: FSMContext):
    if not await work_time():
        text = await hms.diff_lang(message.from_user.id, 'time_out')
        return await message.answer(text,
                                    parse_mode='html')

    get_foods = await hms.diff_lang(message.from_user.id, 'get_foods')
    try:
        if (message.text.startswith('+79') and len(message.text) == 12) or (message.text.startswith('89') and
                                                                            len(message.text) == 11):
            try:
                await sql.add_num(message.from_user.id, f'{message.contact.phone_number}')
            except AttributeError:
                await sql.add_num(message.from_user.id, message.text)

            await message.answer(get_foods,
                                 reply_markup=await client_kb.kb_order(message.from_user.id))
            msg_cart = await message.answer('Меню: ', reply_markup=await client_kb.items_ikb_clt())
            await sql.add_msg(message.from_user.id, msg_cart.message_id)

            await orderState.menu.set()

        else:
            num_err = await hms.diff_lang(message.from_user.id, 'num_err')
            return await message.answer(num_err)

    except AttributeError:
        await sql.add_num(message.from_user.id, message.contact.phone_number)
        await message.answer(get_foods,
                             reply_markup=await client_kb.kb_order(message.from_user.id))

        msg_cart = await message.answer('Меню: ', reply_markup=await client_kb.items_ikb_clt())
        await sql.add_msg(message.from_user.id, msg_cart.message_id)
        await orderState.menu.set()


# @dp.register_callback_query_handler(lambda call: call.data.startswith('client'))
async def show_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if not await work_time():
        text = await hms.diff_lang(call.from_user.id, 'time_out')
        return await call.message.answer(text,
                                         parse_mode='html')
    wait = await sql.sql_read_menu()
    category = callback_data.get('category')
    await sql.add_cat(call.from_user.id, category)
    await call.message.edit_reply_markup(
        reply_markup=await client_kb.in_plus_menu(category, wait, call.from_user.id))


async def show_plus_minus(call: types.CallbackQuery, callback_data: dict):
    if callback_data.get('category') == 'Назад':
        await call.message.edit_reply_markup(reply_markup=await client_kb.items_ikb_clt())
        await call.answer()

    elif callback_data.get('category') == 'minus_menu':
        wait = await sql.sql_read_menu()
        category = await sql.get_info(call.from_user.id)
        category = str(category[8])
        await call.message.edit_reply_markup(
            reply_markup=await client_kb.in_minus_menu(category, wait, call.from_user.id))
        await call.answer()

    elif callback_data.get('category') == 'plus_menu':
        wait = await sql.sql_read_menu()
        category = await sql.get_info(call.from_user.id)
        category = category[8]
        await call.message.edit_reply_markup(
            reply_markup=await client_kb.in_plus_menu(category, wait, call.from_user.id))
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
    cart_text = await hms.diff_lang(call.from_user.id, 'cart')
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_cart,
                                text=f'<b>{cart_text}</b> \n{old}\n<b>Меню:</b>', parse_mode='html',
                                reply_markup=await client_kb.in_plus_menu(callback_data.get('category'), wait,
                                                                          call.from_user.id))


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
        cart_text = await hms.diff_lang(call.from_user.id, 'cart')
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_cart,
                                    text=f'{cart_text} \n{old}\n<b>Меню:</b>', parse_mode='html',
                                    reply_markup=await client_kb.in_minus_menu(callback_data.get('category'), wait,
                                                                               call.from_user.id))
    else:
        await call.answer()


async def empty_cart(message: types.Message):
    await del_twice_message(message.from_user.id)
    text = await hms.diff_lang(message.from_user.id, 'empty_cart')
    await message.answer(text, reply_markup=await client_kb.kb_order(message.from_user.id))
    msg_cart = await message.answer('Меню', reply_markup=await client_kb.items_ikb_clt())
    await sql.add_msg(message.from_user.id, msg_cart.message_id)
    await sql.add_state(message.from_user.id, 0)
    await sql.add_state_pay(message.from_user.id, 0)
    await sql.empty_cart(message.from_user.id)


async def deliv_self(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await sql.add_deliv(call.from_user.id, 0)
    text = await hms.diff_lang(call.from_user.id, 'get_num')
    await bot.send_message(call.from_user.id, text, reply_markup=await client_kb.share_num(call.from_user.id))
    await call.answer()
    await orderState.set_nm.set()


async def draft_buy(message: types.Message):
    if not await work_time():
        text = await hms.diff_lang(message.from_user.id, 'time_out')
        return await message.answer(text,
                                    parse_mode='html')

    data = await sql.get_info(message.from_user.id)
    msg = data[7]
    await del_twice_message(message.from_user.id)

    if not await sql.get_cart(message.from_user.id):
        await del_twice_message(message.chat.id)
        choice_empty = await hms.diff_lang(message.from_user.id, 'choice_empty')
        await message.answer(choice_empty)
        msg_cart = await message.answer('Меню: ', reply_markup=await client_kb.items_ikb_clt())
        return await sql.add_msg(message.from_user.id, msg_cart.message_id)

    delivery = data[6]
    old = await client_kb.check(delivery, message.from_user.id)

    order_txt = await hms.diff_lang(message.from_user.id, 'order_txt')

    if delivery > 0:
        msg1 = await bot.send_message(message.from_user.id, f'<b>{order_txt}</b>\n\n{old}', parse_mode='html',
                                      )
    else:
        msg1 = await bot.send_message(message.from_user.id, f'<b>{order_txt}</b>\n\n{old}', parse_mode='html',
                                      )
    ask_order = await hms.diff_lang(message.from_user.id, 'ask_order')
    msg = await bot.send_message(message.from_user.id, ask_order,
                                 reply_markup=await client_kb.draft_kb(message.from_user.id))
    total = f'{msg.message_id}x{msg1.message_id}'
    await sql.add_msg(message.from_user.id, total)
    await orderState.ask_order.set()


# @dp.callback_query_handler(Text(startswith='order'), state=None)
async def ask_pay(call: types.CallbackQuery, state: FSMContext):
    if not await work_time():
        text = await hms.diff_lang(call.from_user.id, 'time_out')
        return await call.message.answer(text,
                                         parse_mode='html')

    sum = await client_kb.total_price(call.from_user.id)

    if call.data == 'order_right':

        url = await sber.url_pay(call.from_user.id, 2)

        pay_txt = await hms.diff_lang(call.from_user.id, 'pay_txt')
        check_pay = await hms.diff_lang(call.from_user.id, 'check_pay')
        canc_pay = await hms.diff_lang(call.from_user.id, 'canc_pay')

        claim_keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])
        claim_keyboard.add(InlineKeyboardButton(text=pay_txt,
                                                url=url))
        claim_keyboard.add(InlineKeyboardButton(text=check_pay,
                                                callback_data='clt:claim:-:-:-'))
        claim_keyboard.add(InlineKeyboardButton(text=canc_pay, callback_data='cancel_pay'))

        await call.message.delete()

        buy_txt = await hms.diff_lang(call.from_user.id, 'buy')
        msg = await bot.send_photo(call.from_user.id, photo=sber_photo,
                                   caption=buy_txt,
                                   reply_markup=claim_keyboard, parse_mode='html')
        await call.answer()
        await sql.add_msg(call.from_user.id, msg.message_id)
        await orderState.get_order.set()

    else:
        await state.finish()
        text = await hms.diff_lang(call.from_user.id, 'order_canc')
        await call.message.delete()
        await bot.send_message(call.from_user.id, text,
                               reply_markup=await client_kb.start_kb(call.from_user.id))
        await call.answer()
        await sql.empty_cart(call.from_user.id)
        await del_twice_message(call.from_user.id)


# @dp.callback_query_handler(text='cancel_pay')
async def cancel_pay(call: types.CallbackQuery, state: FSMContext):
    await del_twice_message(call.from_user.id)
    text = await hms.diff_lang(call.from_user.id, 'order_canc')
    await call.message.answer(text, reply_markup=await client_kb.start_kb(call.from_user.id))
    await sql.add_state(call.from_user.id, 0)
    await sql.add_state_pay(call.from_user.id, 0)
    await sql.empty_cart(call.from_user.id)
    await state.finish()


# @dp.message_handler(state=FSMPickup.bill)
async def answer_q3(call: types.CallbackQuery, state: FSMContext):
    data = await sql.get_info(call.message.chat.id)

    old = await client_kb.check(int(data[6]), call.from_user.id)
    num = str(data[3])

    if num[0] == '7':
        num = '+' + num

    if int(data[6]) > 0:
        text = f'Доставка:\n{old}<b>Тел:</b> {num}\n\n<b>Статус:</b> Оплачен!'
    else:
        text = f'Cамовывоз:\n{old}\nТел: {num}\n\nСтатус: Оплачен!'

    await call.answer('...')

    state_pay = await sber.get_pay_status(call.from_user.id)

    if int(state_pay) == 2:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        scs_txt = await hms.diff_lang(call.from_user.id, 'scs_txt')
        await bot.send_message(call.message.chat.id,
                               scs_txt, reply_markup=await client_kb.kb_state(call.from_user.id))
        msg = await bot.send_message(chat_id=create__bot.admin_id, text=text,
                                     reply_markup=await client_kb.acs_butt(call.from_user.id), parse_mode='html')
        await sql.add_msg(call.from_user.id, msg.message_id)
        ord_scs = await hms.diff_lang(call.from_user.id, 'order_success')
        await sql.add_state(call.from_user.id, ord_scs)
        await orderState.wait.set()
    else:
        text = await hms.diff_lang(call.from_user.id, 'wait_pay')
        return await bot.send_message(call.message.chat.id,
                                      text, reply_markup=await client_kb.kb_state(call.from_user.id))


# @dp.message_handler(text='Информация')
async def info_lazzat(message: types.Message):
    await message.answer(
        '<b>Кафе Лаззат:</b>\n\n<b>Адрес:</b> ул. Жигулевская 11 г. Тольятти\n<b>Режим работы:</b> 09:30 - '
        '21:30\n<b>Тел:</b> +79649687004 '
        '\n\nЭтот бот создан для заказа еды, если есть сомнения позвоните по официальному номеру на сайте и уточните '
        'id бота.\n\n<b>Создатель бота:</b> @ZeRo_163',
        reply_markup=client_kb.kb_info, parse_mode='html')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cancel_hand, state="*", commands='Отмена')
    dp.register_message_handler(cancel_hand, Text(equals=['отмена', "To'xtatish", "Бас кунед"], ignore_case=True),
                                state="*")

    dp.register_message_handler(hi_send,
                                lambda message: message.text in ['/start', '/help', 'Режим клиента', 'Привет', 'Hi',
                                                                 'Здравствуйте', 'Назад'], state=None)
    dp.register_callback_query_handler(set_lang, Text(startswith='loc'), state=None)
    dp.register_message_handler(ask_buy, text=['Заказать', 'Фармоиш', 'Buyurtma'], state=None)
    dp.register_callback_query_handler(get_loc, text='Доставка', state=orderState.choice_delivery)
    dp.register_callback_query_handler(deliv_self, text='Самовывоз', state=orderState.choice_delivery)
    dp.register_message_handler(set_loc, content_types=['location', 'text'], state=orderState.set_loc)
    dp.register_callback_query_handler(right_num, text=['loc_err', 'loc_right'], state=orderState.num)
    dp.register_message_handler(set_num, content_types=['contact', 'text'], state=orderState.set_nm)
    dp.register_callback_query_handler(show_menu, cb.filter(type='show_clt_item'), state=orderState.menu)
    dp.register_callback_query_handler(show_plus_minus, cb.filter(type='buy'), state=orderState.menu)
    dp.register_callback_query_handler(add_cart, cb.filter(type='plus'), state=orderState.menu)
    dp.register_callback_query_handler(minus_cart, cb.filter(type='minus'), state=orderState.menu)
    dp.register_message_handler(draft_buy, text=['Купить', 'Харид', "Sotib olish"], state=orderState.menu)
    dp.register_message_handler(empty_cart, text=['Очистить корзину', "Фармоишро тоза кунед", "Buyurtmani tozalash"],
                                state=orderState.menu)
    dp.register_callback_query_handler(ask_pay, Text(startswith='order'), state=orderState.ask_order)
    dp.register_callback_query_handler(answer_q3, cb.filter(type='claim'), state=orderState.get_order)
    dp.register_callback_query_handler(cancel_pay, text='cancel_pay', state=orderState.get_order)
    dp.register_message_handler(info_lazzat, text=['Информация', "Ma'lumot", 'Маълумот'], state='*')

