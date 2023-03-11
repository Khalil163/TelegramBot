from aiogram import types, Dispatcher
import string, json
from keyboards import client_kb


#@dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.delete()
        await message.answer(f'{message.from_user.first_name}, Сквернословие - это плохо!!')
    else:
        await message.answer('Рад, что вы с нами!', reply_markup=client_kb.kb_client)



def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)