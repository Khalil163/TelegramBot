from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


from create__bot import dp, bot
from data import sql
from keyboards import kb_admin



cb = kb_admin.cb


class FSMAdmin(StatesGroup):
    name = State()
    price = State()
    item = State()
    stoplist = State()


class FSMItem(StatesGroup):
    name = State()
    photo = State()


flag = False


# @dp.register_message_handler(Text(equals='moderator', ignore_case=True))
async def user_upp(message: types.Message):
    global flag
    flag = True
    await message.answer('Введите пароль: ')


# @dp.register_message_handler()
async def inp_key(message: types.Message):
    global flag
    if flag:
        if message.text == 'LazzatMod163':
            if await sql.is_moder(message.from_user.id) is False:
                await sql.add_user(message.from_user.first_name, message.from_user.id, 'admin')
                await message.answer('Здравствуй, модератор!!!', reply_markup=kb_admin.admin_case)
            elif await sql.is_moder(message.from_user.id) == 'client':
                await sql.upp_level(message.from_user.id, 'admin')
                await message.answer('Здравствуй, модератор!!!', reply_markup=kb_admin.admin_case)


# @dp.register_message_handler()Text('ModerMode')
async def kb_adm(message: types.Message):
    if await sql.is_moder(message.from_user.id) == 'admin':
        await message.answer('Здравствуй, модератор!!!', reply_markup=kb_admin.admin_case)


# @dp.message_handler(state=None)
async def edit_menu(message: types.Message):
    if await sql.is_moder(message.from_user.id) == 'admin':
        if message.text == "Добавить блюдо":
            await FSMAdmin.name.set()
            await message.answer('Введите название: ', reply_markup=kb_admin.kb_canc)


# dp.register_message_handler(state="*", commands='Отмена')
# dp.register_message_handler(Text(equals='отмена', ignore_case=True),state="*" )
async def cancel_hand(message: types.Message, state: FSMContext):
    if await sql.is_moder(message.from_user.id) == 'admin':
        to_state = await state.get_state()
        if to_state is None:
            return
        await state.finish()
        await message.answer('ОК', reply_markup=kb_admin.admin_case)


# @dp.message_handler(state=FSMAdmin.name)
async def set_name(message: types.Message, state: FSMContext):
    if await sql.is_moder(message.from_user.id) == 'admin':
        if await sql.is_name_food(message.text):
            async with state.proxy() as data:
                data['name'] = message.text
            await FSMAdmin.next()
            await message.answer("Введите цену: ")
        else:
            return await message.answer('Такое блюдо уже есть!\nВведите название: ')


# @dp.message_handler(lambda message: not message.text.isdigit(), state=FSMAdmin.price)
async def set_price_invalid(message: types.Message):
    return await message.answer("Введите цену: (цифры)")


# @dp.message_handler(state=FSMAdmin.price)
async def set_price(message: types.Message, state: FSMContext):
    if await sql.is_moder(message.from_user.id) == 'admin':
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Раздел блюда: ", reply_markup=await kb_admin.items_in())


# ['Супы', 'Второе', 'Мангал', 'Гарниры', 'Салаты', 'Соусы', 'Напитки', 'Десерты']


# @dp.callback_query_handler(lambda call: call.data in items_menu, FSMAdmin.item)
async def set_item(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if await sql.is_moder(call.from_user.id) == 'admin':
        async with state.proxy() as data:
            data['item'] = callback_data.get('category')
        await FSMAdmin.next()
        await call.message.edit_reply_markup()
        await bot.send_message(call.from_user.id, f'<b>Ваш выбор:</b> {callback_data.get("category")}',
                               parse_mode='html')
        await bot.send_message(call.from_user.id, "Наличие в меню: ", reply_markup=kb_admin.stop_case)
        await call.answer()


# @dp.callback_query_handler(lambda call: call.data in ['start', 'stop'], FSMAdmin.stoplist)
async def set_stop_list(call: types.CallbackQuery, state: FSMContext):
    if await sql.is_moder(call.from_user.id) == 'admin':
        async with state.proxy() as data:
            data['stoplist'] = str(call.data)
        await call.message.edit_reply_markup()
        await bot.send_message(call.from_user.id, f'<b>Ваш выбор:</b> {call.data}', parse_mode='html')
        print(data)
        await sql.add_menu(state)
        await bot.send_message(call.from_user.id, 'Данные загружены, ОК!', reply_markup=kb_admin.admin_case)
        await call.answer()
        await state.finish()


# @dp.message_handler(Text(equals='Удалить'))
async def fun_del(message: types.Message):
    if await sql.is_moder(message.from_user.id) == 'admin':
        wait = await sql.sql_read_menu()
        if len(wait) > 0:
            await message.answer('Что хотите удалить ?', reply_markup=kb_admin.del_in_kb)
        else:
            await message.answer('Вам нечего удалять')


# @dp.callback_query_handler(cb.filter(type='delete'))
async def choice_del(call: types.CallbackQuery, callback_data: dict):
    if callback_data.get('category') == 'food':
        await call.message.edit_reply_markup(reply_markup=await kb_admin.items_i_del())
    else:
        await call.message.edit_reply_markup(reply_markup=await kb_admin.items_i_d())


# @dp.callback_query_handler(cb.filter(type='del_item'))
async def del_item(call: types.CallbackQuery, callback_data: dict):
    await sql.del_item(callback_data.get('category'))
    await call.message.edit_reply_markup(reply_markup=await kb_admin.items_i_d())
    await call.answer(text=f'Раздел - {callback_data.get("category")}, удален.')


# @dp.callback_query_handler(lambda x: x.data.split(' ')[1] == 'del')
async def show_del_menu(call: types.CallbackQuery, callback_data: dict):
    if await sql.is_moder(call.from_user.id) == 'admin':
        wait = await sql.sql_read_menu()
        await call.message.edit_reply_markup(reply_markup=await kb_admin.in_del_m(callback_data.get('category'), wait))
        await call.answer()


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_call(call: types.CallbackQuery, callback_data: dict):
    if await sql.is_moder(call.from_user.id) == 'admin':
        if callback_data.get('product') == 'Назад':
            await call.message.edit_reply_markup(reply_markup=await kb_admin.items_i_del())
        else:
            await sql.del_food(callback_data.get('product'))
            wait = await sql.sql_read_menu()
            await call.message.edit_reply_markup(
                reply_markup=await kb_admin.in_del_m(callback_data.get('category'), wait))
            await call.answer(text=f'Блюдо - {callback_data.get("product")}, удалено.')


# @dp.message_handler(Text(equals='Стоп лист'))
async def set_stop(message: types.Message):
    if await sql.is_moder(message.from_user.id) == 'admin':
        await message.answer('Стоп лист:', reply_markup=await kb_admin.items_in_stop())
        await message.delete()


# @dp.callback_query_handler(lambda call: call.data in kb_admin.items_menu)
async def start_menu(call: types.CallbackQuery, callback_data: dict):
    if await sql.is_moder(call.from_user.id) == 'admin':
        wait = await sql.sql_read_menu()
        await call.message.edit_reply_markup(reply_markup=kb_admin.in_stop(callback_data.get('category'), wait))
        await call.answer()


# @dp.callback_query_handler(lambda call: call.data in wait or call.data == 'Назад')
async def upd_stop(call: types.CallbackQuery, callback_data: dict):
    if await sql.is_moder(call.from_user.id) == 'admin':
        wait = await sql.sql_read_menu()
        if callback_data.get('product') == 'Назад':
            await call.message.edit_reply_markup(reply_markup=await kb_admin.items_in_stop())
            await call.answer()
        elif callback_data.get('state') == "ЕСТЬ":
            await sql.edit_stop('НЕТ', callback_data.get('product'))
            wait = await sql.sql_read_menu()
            await call.message.edit_reply_markup(reply_markup=kb_admin.in_stop(callback_data.get('category'), wait))
            await call.answer('ОК')
        else:
            await sql.edit_stop('ЕСТЬ', callback_data.get('product'))
            wait = await sql.sql_read_menu()
            await call.message.edit_reply_markup(reply_markup=kb_admin.in_stop(callback_data.get('category'), wait))
            await call.answer('ОК')


#@dp.message_handler(Text('Добавить раздел'), state=None)
async def start_edit_item(message: types.Message):
    if await sql.is_moder(message.from_user.id) == 'admin':
        await message.answer('Название раздела:', reply_markup=kb_admin.kb_canc)
        await FSMItem.name.set()


#@dp.message_handler(state=FSMItem.name)
async def set_name_item(message: types.Message, state: FSMContext):
    if await sql.is_moder(message.from_user.id) == 'admin':
        if await sql.is_name_item(message.text):
            await sql.add_item(message.text)
            await message.answer('Данные успешно загружены', reply_markup=kb_admin.admin_case)
            await state.finish()
        else:
            return await message.answer('Такой раздел уже есть\nНазвание раздела:', reply_markup=kb_admin.kb_canc)





def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(user_upp, Text(equals='moderator', ignore_case=True))
    dp.register_message_handler(kb_adm, Text(equals='ModerMod'))
    dp.register_message_handler(inp_key, Text('LazzatMod163'))
    dp.register_message_handler(set_stop, Text(equals='Стоп лист'))
    dp.register_callback_query_handler(upd_stop, cb.filter(type='edit_stop'))
    dp.register_message_handler(edit_menu, Text('Добавить блюдо'), state=None)
    dp.register_message_handler(cancel_hand, state="*", commands='Отмена')
    dp.register_message_handler(cancel_hand, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(set_name, state=FSMAdmin.name)
    # dp.register_message_handler(set_description, state=FSMAdmin.description)
    dp.register_message_handler(set_price_invalid, lambda message: not message.text.isdigit(), state=FSMAdmin.price)
    dp.register_message_handler(set_price, lambda message: message.text.isdigit(), state=FSMAdmin.price)
    dp.register_callback_query_handler(set_item, cb.filter(type='set_item'), state=FSMAdmin.item)
    dp.register_callback_query_handler(set_stop_list, lambda call: call.data in ['ЕСТЬ', 'НЕТ'],
                                       state=FSMAdmin.stoplist)
    dp.register_callback_query_handler(start_menu, cb.filter(type='items_stop'))
    dp.register_message_handler(fun_del, Text(equals='Удалить'))
    dp.register_callback_query_handler(choice_del, cb.filter(type='delete'))
    dp.register_callback_query_handler(del_item, cb.filter(type='del_item'))
    dp.register_callback_query_handler(show_del_menu, cb.filter(type='show_items_del'))
    dp.register_callback_query_handler(del_call, cb.filter(type='del_food'))
    dp.register_message_handler(start_edit_item, Text('Добавить раздел'), state=None)
    dp.register_message_handler(set_name_item, state=FSMItem.name)

# mas = []
# data = {
#     'name':
# }