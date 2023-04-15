from data import sql
from create__bot import bot


async def diff_lang(id, text):
    lang = await sql.get_lang(id)

    if lang == 'ru':
        return RU[text]

    elif lang == 'uz':
        return UZ[text]

    elif lang == 'tz':
        return TZ[text]


RU = {
    'hi': "Привет, {}! 👋",
    'sorry': 'Извините, у вас уже есть открытый заказ.\nПо вопросам звонить: +79649687004',
    'time_out': '<b>Режим работы:</b> 09:30 - 22:00\n\nМы не можем сейчас принять заказ.\nНо будем рады в рабочее время!',
    'format_order': 'Формат заказа:',
    'choice_deliv': 'Ваш выбор: Доставка',
    'get_loc': 'Нажмите на кнопку поделиться или напишите адрес доставки:',
    'set_loc': 'Это ваш адрес?\n{}',
    'loc_out': 'Работаем только в городе Тольятти.\nВведите адрес:',
    'canc_text': 'Хорошо. Будем ждать вашего заказа!',
    'loc_yes': 'Ваш выбор: Да',
    'loc_no': "Ваш выбор: Нет",
    'get_num': 'Отлично, теперь мне нужен ваш номер.\n\nНажмите на кнопку поделиться или напишите сами:',
    'get_foods': 'Теперь выберите блюда \n(Для покупки нажмите кнопку "КУПИТЬ")',
    'num_err': 'Некорректный формат:\n\nНажмите на кнопку поделиться или напишите сами:',
    'cart': '<b>Корзина:</b>',
    'empty_cart': 'Корзина очищена.',
    'choice_empty': 'Вы ничего не выбрали',
    'order_txt': 'Ваш заказ:',
    'ask_order': 'Оформляем заказ ?',
    'pay_txt': 'Оплатить',
    'check_pay': "Проверить оплату",
    'canc_pay': 'Отменить оплату',
    'buy':
        '''Нажмите на кнопку оплатить, после этого проверьте платеж.\n\n(Если у вас сбербанк, то на платежной странице можно нажать на <b>зеленую кнопку</b> для оплаты.\nВам не надо будет вводить данные)''',
    'order_canc': "Заказ отменен.\nБудем ждать ваc снова!",
    'order_success': "Заказ принят",
    'wait_pay':
        '''Вы не оплатили заказ или оплата еще в пути!\nПопробуйте проверить снова! ''',
    'order': 'Заказать',
    'share_loc': 'Поделиться 📍',
    'canc_txt': 'Отмена',
    'info': 'Информация',
    'sh_num': 'Поделиться номером',
    'dry': 'Доставка',
    'pickup': 'Самовывоз',
    'yes': 'Да',
    'no': 'Нет',
    'buy_r': 'Купить',
    'cart_empty': "Очистить корзину",
    'minus': "Уменьшить",
    'plus': 'Увеличивать',
    'back': 'Назад',
    'scs_txt': 'Оплата подтверждена!\nВаш заказ принят!',
    'acc_txt': "<b>Мы стараемся, чтобы ваш заказ был приготовлен как можно быстрее!</b>\n\nДоставка заказа займет от 15 мин",
    'srr_txt': 'Извините, ваш заказ был отменен Позвоните: +79649687004',
    'await_pickup': 'Ожидает выдачи',
    'thank_txt': "Благодарим за заказ.\nПриятного аппетита!",
    'st_kb': 'Статус заказа',
    "skipped": 'Курьер отменен',
    'pending': '<b>Ищем курьера</b>',
    'visited': 'Курьер уже в пути'

}

UZ = {
    'hi': 'Salom alaykum, {}! 👋',
    'sorry': "Kechirasiz, sizda allaqachon ochiq buyurtma bor.\nSavollar bo'yicha qo'ng'iroq qiling: +79649687004",
    'time_out': "<b>Ish vaqti:</b> 09:30 - 22:00\n\nBiz hozir buyurtmani qabul qila olmaymiz.\nLekin ish vaqtida xursand bo'lamiz!",
    'format_order': 'Buyurtma formati:',
    'choice_deliv': 'Sizning tanlovingiz: yetkazib berish',
    'get_loc': "Joylashuvni knopkasini bosing yoki etkazib berish manzilini yozing:",
    'set_loc': "Bu sizning manzilingizmi?\n{}",
    'loc_out': "Biz faqat Tolyatti shahrida ishlaymiz.\nManzilni kiriting:",
    'canc_text': "Yaxshi. Buyurtmangizni kutamiz!",
    'loc_yes': 'Sizning tanlovingiz: Ha',
    'loc_no': "Sizning tanlovingiz: yo'q",
    'get_num': "Ajoyib, endi menga sizning raqamingiz kerak.\n\nKnopkani bosing yoki o'zingiz yozing:",
    'get_foods': "Endi ovqatni tanlang\n\n(sotib olish uchun \"sotib olish\" knopkani bosing)",
    'num_err': "Noto'g'ri format:\n\nUlashish tugmasini bosing yoki o'zingiz yozing:",
    'cart': '<b>Buyurtma:</b>',
    'empty_cart': "Buyurtma o'chirildi",
    'choice_empty': "Siz hech narsani tanlamadingiz",
    'order_txt': 'Sizning buyurtmangiz:',
    'ask_order': 'Buyurtma berasizmi ?',
    'pay_txt': "To'lash",
    'check_pay': "To'lovni tekshiring",
    'canc_pay': "To'lovni to'xtating",
    'buy': '''To'lash tugmasini bosing, keyin to'lovni tekshiring.\n\n(Agar sizda Sberbank bo'lsa, unda to'lov sahifasida to'lov uchun <b>yashil knopkani</b> bosishingiz mumkin.\nMa'lumotlarni kiritishingiz shart emas)''',
    'order_canc': "Buyurtma to'xtatildi.\nSizni yana kutamiz!",
    'order_success': "Buyurtma qabul qilindi",
    'wait_pay': '''Siz buyurtmani to'lamadingiz yoki to'lov hali yo'lda!\nYana tekshirib ko'ring!''',
    'order': 'Buyurtma',
    'share_loc': 'Yuborish 📍',
    'canc_txt': "To'xtatish",
    'info': "Ma'lumot",
    'sh_num': 'Raqamni yuboring',
    'dry': "Yetkazib berish",
    'pickup': 'Olib ketish',
    'yes': "Ha",
    'no': "Yo'q",
    'buy_r': "Sotib olish",
    'cart_empty': "Buyurtmani tozalash",
    'minus': "Kamaytirish",
    'plus': "Ko'paytirish",
    'back': "Orqaga",
    'scs_txt': "To'lov tasdiqlandi!\nSizning buyurtmangiz qabul qilindi!",
    'acc_txt': '<b>Biz sizning buyurtmangizni iloji boricha tezroq pishirishga harakat qilamiz!</b>\n\nBuyurtmani etkazib berish 15 daqiqadan boshlanadi',
    'srr_txt': "Kechirasiz, buyurtmangiz bekor qilindi qo'ng'iroq qiling: +79649687004",
    'await_pickup': 'Chiqarishni kutmoqda',
    'thank_txt': "Buyurtma uchun rahmat.\nYoqimli ishtaha!",
    'st_kb': "Buyurtma holati",
    'skipped': "Buyurtma <b>to'xtatildi</b>",
    'pending': "<b>Biz kurerni qidirmoqdamiz</b>",
    'visited': "Kuryer yo'lda"

}

TZ = {
    'hi': 'Салом, {}! 👋',
    'sorry': "Бубахшед, шумо аллакай фармоиши кушод доред.\nОид ба саволҳо занг занед: +79649687004",
    'time_out': '<b>Ҳолати корӣ:</b> 09:30 - 22:00\n\nMо ҳоло фармоишро қабул Карда Наметавонем.\nAммо дар соатҳои корӣ хурсанд мешавем!',
    'format_order': 'Формати фармоиш:',
    'choice_deliv': 'Интихоби шумо: Интиқол',
    'get_loc': 'Тугмаи мубодилаи маконро клик кунед е суроғаи интиқолро нависед:',
    'set_loc': 'Ин суроғаи шумост?\n{}',
    'loc_out': 'Мо танҳо дар Шаҳри Толиятти кор мекунем.\nСуроғаро ворид кунед:',
    'canc_text': 'Хуб. Мо интизори фармоиши шумо ҳастем!',
    'loc_yes': 'Интихоби Шумо: Бале',
    'loc_no': 'Интихоби шумо: Не',
    'get_num': "Бузург, ҳоло ба ман рақами шумо лозим аст.\n\nТугмаи мубодила ро клик кунед е худатон нависед:",
    'get_foods': 'Акнун хӯрокро интихоб кунед\n(барои харидан тугмаи "ХАРИДАН" - ро клик кунед)',
    'num_err': "Формати нодуруст: тугмаи мубодила Ро Клик кунед е худатон нависед:",
    'cart': '<b>Фармоиш:</b>',
    'empty_cart': 'Фармоиш нест карда шуд',
    'choice_empty': 'Шумо чизе интихоб накардед',
    'order_txt': 'Фармоиши шумо:',
    'ask_order': 'Фармоиш додан ?',
    'pay_txt': "Пардохт кунед",
    'check_pay': 'Пардохтро тафтиш кунед',
    'canc_pay': 'Пардохт накардан',
    'buy':
        '''Тугмаи пардохтро клик кунед, пас пардохтро тафтиш кунед.\n\n(Агар шумо сбербанк дошта бошед, пас дар саҳифаи пардохт шумо метавонед \nтугмаи сабзро барои пардохт пахш кунед-ба шумо лозим нест,\nки маълумотро ворид кунед)''',
    'order_canc': "Фармоиш қатъ карда шуд.\nБиеед боз шуморо интизор шавем!",
    'order_success': 'Фармоиш қабул карда шуд',
    'wait_pay': '''Шумо пардохт накардаед фармоиш е пардохт ҳанӯз дар роҳ аст!\nКӯшиш кунед, ки дубора тафтиш кунед!''',
    'order': 'Фармоиш',
    'share_loc': 'Ирсол 📍',
    'canc_txt': "Бас кунед",
    'info': 'Маълумот',
    'sh_num': 'Ирсоли рақам',
    'dry': 'Таҳвил',
    'pickup': 'Гирифтан',
    'yes': 'бале',
    'no': 'не',
    'buy_r': "Харид",
    'cart_empty': "Фармоишро тоза кунед",
    'minus': 'Redusí',
    "plus": "Aumenta",
    'back': 'Atrás',
    'scs_txt': "Пардохт тасдиқ карда шуд!\nФармоиши шумо қабул карда шуд!",
    'acc_txt': "<b>Мо кӯшиш мекунем, ки фармоиши шумо ҳарчи зудтар омода карда шавад!</b>\n\nБарои расонидани фармоиш аз 15 дақиқа вақт лозим аст",
    'srr_txt': "Бубахшед, фармоиши шумо қатъ карда шуд .Занг занед: +79649687004",
    'await_pickup': 'Интизори додани',
    'thank_txt': 'Ташаккур барои фармоиш.\nИштиҳои хуб!',
    'st_kb': "Статуси фармоиш",
    'skipped': 'Фармоиш <b>боздошта шуд </b>',
    "pending": '<b>Чустуҷӯи хаткашон</b>',
    'visited': 'Хаткашон дар роҳ аст'

}
