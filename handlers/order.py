from aiogram import types, Dispatcher
from create__bot import dp, bot
from keyboards import req_api, client_kb
from data import sql

cb = client_kb.cb


#@dp.callback_query_handler(cb.filter(type='pay_a'))
async def access(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('product'))
    delivery = await sql.get_info(id)
    msg = delivery[7]
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])
    state = 'Заказ готовится'


    if num[0] == '7':
        num = '+' + num

    if callback_data.get('category') == 'true':
        if float(callback_data.get('price')) > 0:
            locate = await sql.get_address(id)
            text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ готовится'
            await bot.send_message(id, '<b>Мы стараемся, чтобы ваш заказ был приготовлен как можно быстрее!</b>\n\nДоставка заказа займет от 15 мин', reply_markup= client_kb.kb_state, parse_mode='html')
            await bot.edit_message_text(text, call.from_user.id, message_id=msg, reply_markup=await client_kb.express(id), parse_mode='html')

        else:
            text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ готовится'
            await bot.edit_message_text(text, call.from_user.id, message_id=msg, reply_markup=await client_kb.fd_ready(id), parse_mode='html')
            await bot.send_message(id, '<b>Мы стараемся, чтобы ваш заказ был приготовлен как можно быстрее!</b>\n\nМы сообщим как будет всё готово.',
                                   reply_markup=client_kb.kb_state, parse_mode='html')



#@dp.callback_query_handler(cb.filter(type='taxi_o'))
async def order_taxi(call: types.CallbackQuery, callback_data: dict):

    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])
    #state = 'Ожидаем курьера...'


    if num[0] == '7':
        num = '+' + num

    await req_api.draft_order(id)
    await req_api.proc_order(id)

    state = await req_api.state_order(id)

    await sql.add_state(id, state)


    await call.answer('Вы заказали такси')
    locate = await sql.get_address(id)
    text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> {state}'

    await bot.edit_message_text(text, call.from_user.id, message_id=msg, reply_markup=await client_kb.kb_finish(id), parse_mode='html')


    await call.message.edit_reply_markup(reply_markup=await client_kb.canc_express(id))


#@dp.callback_query_handler(cb.filter(type='taxi_canc'))
async def canc_taxi(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])
    state = await req_api.state_order(id)

    await sql.add_state(id, state)
    await sql.add_state(id,state)

    if num[0] == '7':
        num = '+' + num

    await req_api.cancel_order(id)

    await call.answer('Отмена такси')

    locate = await sql.get_address(id)
    text = f'<b>Доставка:</b>\n{old}\n<b>Адрес:</b> {locate}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> {state}'
    await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                   reply_markup=await client_kb.kb_finish(id), parse_mode='html')



#@dp.callback_query_handler(cb.filter(type='fd_ready'))
async def ready(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])
    state = 'Ожидает выдачи'
    await sql.add_state(id,state)
    if num[0] == '7':
        num = '+' + num

    text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Ожидает выдачи...'

    await bot.send_message(id, '<b>Ваш заказ готов!</b>', parse_mode='html')
    await bot.edit_message_text(text, call.from_user.id, message_id=msg,
                                reply_markup=await client_kb.kb_pkp(id), parse_mode='html')


#@dp.callback_query_handler(cb.filter(type='dv_finish'))
async def ready_dv(call: types.CallbackQuery, callback_data: dict):
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

    await bot.edit_message_text(text, call.from_user.id, message_id=msg,  parse_mode='html')
    await call.answer('Заказ завершен')
    await bot.send_message(id, 'Благодарим за заказ.\nПриятного аппетита!', reply_markup=client_kb.kb_client)
    await sql.empty_cart(id)



#@dp.callback_query_handler(cb.filter(type='pkp_finish'))
async def ready_pkp(call: types.CallbackQuery, callback_data: dict):
    id = int(callback_data.get('category'))
    delivery = (await sql.get_info(id))
    msg = int(delivery[7])
    old = await client_kb.check(int(delivery[6]), id)
    num = str(delivery[3])

    await sql.add_state(id, 0)

    if num[0] == '7':
        num = '+' + num

    text = f'<b>Cамовывоз:</b>\n{old}\n<b>Тел:</b> {num}\n\n<b>Статус:</b> Заказ завершен'
    await bot.send_message(id, 'Спасибо за заказ!\nБудем ждать новых заказов!', reply_markup=client_kb.kb_client)
    await bot.edit_message_text(text, call.from_user.id, message_id=msg,  parse_mode='html')
    await call.answer('Заказ завершен')
    await sql.empty_cart(id)


#@dp.message_handler(text='Статус заказа')
async def state_order(message: types.Message):
    state = str(await sql.get_state(message.from_user.id))
    await message.answer(f'<b>Статус заказа:</b> {state}', parse_mode='html')


def register_handlers_order(dp: Dispatcher):
    dp.register_callback_query_handler(access, cb.filter(type='pay_a'))
    dp.register_callback_query_handler(order_taxi, cb.filter(type='taxi_o'))
    dp.register_callback_query_handler(canc_taxi, cb.filter(type='taxi_canc'))
    dp.register_callback_query_handler(ready, cb.filter(type='fd_ready'))
    dp.register_callback_query_handler(ready_dv, cb.filter(type='dv_finish'))
    dp.register_callback_query_handler(ready_pkp, cb.filter(type='pkp_finish'))
    dp.register_message_handler(state_order, text='Статус заказа')