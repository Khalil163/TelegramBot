from aiogram import types, Dispatcher
from create__bot import dp, bot
from keyboards import req_api, client_kb
from data import sql, sber, hms
from aiogram.dispatcher import FSMContext
from handlers import orderState

cb = client_kb.cb


# @dp.callback_query_handler(cb.filter(type='pay_a'))
async def access(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get('product'))
    delivery = await sql.get_info(id)
    msg = delivery[7]
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])
    price = int(callback_data.get('price'))
    locate = await sql.get_address(id)

    if num[0] == '7':
        num = '+' + num

    if callback_data.get('category') == 'true':
        if price > 0:
            text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ ' \
                   f'готовится '
            acc_txt = await hms.diff_lang(id, 'acc_txt')
            await bot.send_message(id, acc_txt, reply_markup= await client_kb.kb_state(id), parse_mode='html')
            await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                        reply_markup=await client_kb.express(id), parse_mode='html')

        else:
            text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ готовится'
            await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                        reply_markup=await client_kb.fd_ready(id), parse_mode='html')
            await bot.send_message(id, '<b>Мы стараемся, чтобы ваш заказ был приготовлен как можно быстрее!</b>\n\nМы '
                                       'сообщим как будет всё готово.',
                                   reply_markup=await client_kb.kb_state(id), parse_mode='html')
    else:
        sum = await client_kb.total_price(id)

        if price > 0:
            text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ ' \
                   f'отменен'
            await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                        parse_mode='html')
        else:
            text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ отменен'
            await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                        parse_mode='html')
        srr_txt = await hms.diff_lang(id, 'srr_txt')
        await bot.send_message(id, srr_txt,
                               reply_markup=await client_kb.start_kb(call.from_user.id))

        await sber.reverse_money(id, sum)

        await sql.add_state(id, 0)
        await sql.add_state_pay(id, 0)
        await sql.empty_cart(id)
        await state.finish()


# @dp.callback_query_handler(cb.filter(type='taxi_o'))
async def order_taxi(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])

    if num[0] == '7':
        num = '+' + num

    await req_api.draft_order(id)
    await req_api.proc_order(id)

    state = await req_api.state_order(id)

    await sql.add_state(id, state)

    await call.answer('Вы заказали такси')
    locate = await sql.get_address(id)
    text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> {state}'

    await bot.edit_message_text(text, call.from_user.id, message_id=msg, reply_markup=await client_kb.kb_finish(id),
                                parse_mode='html')

    await call.message.edit_reply_markup(reply_markup=await client_kb.canc_express(id))


# @dp.callback_query_handler(cb.filter(type='taxi_canc'))
async def canc_taxi(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])

    state = await req_api.state_order(id)

    await sql.add_state(id, state)
    await sql.add_state_pay(id, 0)

    if num[0] == '7':
        num = '+' + num

    await req_api.cancel_order(id)

    await call.answer('Отмена такси')

    locate = await sql.get_address(id)
    text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Отменено такси'
    await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                reply_markup=await client_kb.kb_finish(id), parse_mode='html')


# @dp.callback_query_handler(cb.filter(type='fd_ready'))
async def ready(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])

    state = await hms.diff_lang(id, 'await_pickup')

    await sql.add_state(id, state)
    await sql.add_state_pay(id, 0)

    if num[0] == '7':
        num = '+' + num

    text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Ожидает выдачи...'

    await bot.send_message(id, f'<b>Заказ: {state}</b>', parse_mode='html')
    await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                reply_markup=await client_kb.kb_pkp(id), parse_mode='html')


# @dp.callback_query_handler(cb.filter(type='dv_finish'))
async def ready_dv(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])

    await sql.add_state(id, 0)

    if num[0] == '7':
        num = '+' + num

    locate = await sql.get_address(id)

    text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ завершен'

    await bot.edit_message_text(text, call.from_user.id, message_id=msg, parse_mode='html')
    await call.answer('Заказ завершен')
    thank_txt = await hms.diff_lang(id, 'thank_txt')
    await bot.send_message(id, thank_txt, reply_markup=await client_kb.start_kb(call.from_user.id))
    await sql.empty_cart(id)
    await sql.add_state(id, 0)
    await sql.add_deliv(id, 0)
    await state.finish()


# @dp.callback_query_handler(cb.filter(type='pkp_finish'))
async def ready_pkp(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])

    if num[0] == '7':
        num = '+' + num

    text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ завершен'
    thank_txt = await hms.diff_lang(id, 'thank_txt')
    await bot.send_message(id, thank_txt, reply_markup=await client_kb.start_kb(call.from_user.id))
    await bot.edit_message_text(text, call.from_user.id, message_id=msg, parse_mode='html')
    await call.answer('Заказ завершен')
    await sql.empty_cart(id)
    await sql.add_state(id, 0)
    await sql.add_state_pay(id, 0)
    await state.finish()


# @dp.message_handler(text='Статус заказа')
async def state_order(message: types.Message):
    if message.text == 'Статус заказа' or message.text == 'Buyurtma holati' or message.text == 'Статуси фармоиш':
        if await sql.get_delivery(message.from_user.id) > 0:
            state = await sql.get_state(message.from_user.id)
        else:
            state = await req_api.state_order(message.from_user.id)
        sts_txt = await hms.diff_lang(message.from_user.id, 'st_kb')
        await message.answer(f'<b>{sts_txt}:</b> {state}', parse_mode='html')
    else:
        text = await hms.diff_lang(message.from_user.id, 'sorry')
        await message.answer(text, parse_mode='html')


async def error_handler(message: types.Message):
    msg = await message.answer('Пожалуйста нажимайте кнопки или вводите данные:')


def register_handlers_order(dp: Dispatcher):
    dp.register_callback_query_handler(access, cb.filter(type='pay_a'), state="*")
    dp.register_callback_query_handler(order_taxi, cb.filter(type='taxi_o'), state="*")
    dp.register_callback_query_handler(canc_taxi, cb.filter(type='taxi_canc'), state="*")
    dp.register_callback_query_handler(ready, cb.filter(type='fd_ready'), state="*")
    dp.register_callback_query_handler(ready_dv, cb.filter(type='dv_finish'), state="*")
    dp.register_callback_query_handler(ready_pkp, cb.filter(type='pkp_finish'), state="*")
    dp.register_message_handler(state_order, state=orderState.wait)
    dp.register_message_handler(error_handler, state="*")
