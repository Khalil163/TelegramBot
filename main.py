from create__bot import dp
from aiogram.utils import executor
from handlers import client, admin, other, order
from data import sql


async def start_on(_):
    print("Bot is working")
    sql.start_basa()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
order.register_handlers_order(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=False, on_startup=start_on)