import sqlite3 as sq


def start_basa():
    global base, cur, mod, m_cur, cart, cart_cur, items_cur, db_item
    base = sq.connect('lazzat_menu.db')
    cur = base.cursor()

    mod = sq.connect('Users.db')
    m_cur = mod.cursor()

    cart = sq.connect('Cart.db')
    cart_cur = cart.cursor()

    db_item = sq.connect('Items.db')
    items_cur = db_item.cursor()

    if base and mod and cart:
        print('Data base connected, OK!')

    base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT PRIMARY KEY, price INT, item TEXT, stoplist TEXT)')
    base.commit()
    mod.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, id TEXT PRIMARY KEY, access TEXT, number TEXT, long INT, '
                'lat INT, delivery INT, msg INT, cat TEXT, offer TEXT, status TEXT, address TEXT, state_pay TEXT, lang TEXT)')
    mod.commit()

    cart.execute('CREATE TABLE IF NOT EXISTS cart(user_id TEXT, name TEXT, count INT, price INT)')
    cart.commit()

    db_item.execute('CREATE TABLE IF NOT EXISTS items(name TEXT PRIMARY KEY)')
    db_item.commit()



async def add_menu(data):  # menu
    cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
    base.commit()


async def del_food(data):
    cur.execute('DELETE FROM menu WHERE  name == ?', (data,))
    base.commit()


async def edit_stop(state, name):
    cur.execute('UPDATE menu SET stoplist = ? WHERE name = ?', (state, name))
    base.commit()


async def sql_read_menu():
    return cur.execute('SELECT * FROM menu').fetchall()


async def is_name_food(name):
    info = cur.execute('SELECT name FROM menu WHERE name == ?', [name, ]).fetchone()
    if info is None:
        return True
    return False


async def add_item(data):  #Item
    items_cur.execute('INSERT INTO items VALUES (?)', [data, ])
    db_item.commit()


async def is_name_item(name):
    info = items_cur.execute('SELECT name FROM items WHERE name == ?', [name, ]).fetchone()
    if info is None:
        return True
    return False


async def get_items():
    return items_cur.execute('SELECT * FROM items').fetchall()


async def get_item(name):
    return items_cur.execute('SELECT * FROM items WHERE name == ?', [name,]).fetchone()


async def del_item(data):
    items_cur.execute('DELETE FROM items WHERE  name == ?', [data,])
    db_item.commit()


async def add_user(name, id, access):  # Moders
    m_cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [name, id, access, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ru'])
    mod.commit()


async def is_moder(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchall()
    if info:
        return info[0][2]
    return False


async def get_info(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchone()
    if info:
        return info


async def add_loc(id, lon, lat):
    m_cur.execute('UPDATE users SET long = ?, lat = ? WHERE id == ?', [lon, lat, id])
    mod.commit()


async def get_loc(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchone()
    return [info[4], info[5]]  # long lat


async def add_num(id, num):
    m_cur.execute('UPDATE users SET number = ? WHERE id == ?', [num,  id])
    mod.commit()

async def add_lang(id, num):
    m_cur.execute('UPDATE users SET lang = ? WHERE id == ?', [num,  id])
    mod.commit()


async def add_score(id, num):
    m_cur.execute('UPDATE users SET score = ? WHERE id == ?', [num,  id])
    mod.commit()


async def get_num(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchone()
    return info[3]


async def add_state(id, state):
    m_cur.execute('UPDATE users SET status = ? WHERE id == ?', [state,  id])
    mod.commit()


async def get_state(id):
    try:
        info = (m_cur.execute('SELECT status FROM users WHERE id == ?', [id, ]).fetchone())[0]
        return info
    except TypeError:
        return 0

async def get_state_pay(id):
    try:
        info = (m_cur.execute('SELECT state_pay FROM users WHERE id == ?', [id, ]).fetchone())[0]
        return info
    except TypeError:
        return 0


async def upp_level(id, access):
    m_cur.execute('UPDATE users SET access = ? WHERE id == ?', [access, id])
    mod.commit()


async def add_cart(user_id, name, price):  # Cart
    cart_cur.execute('INSERT INTO cart VALUES (?, ?, ?, ?)', [user_id, name, 1, price])
    cart.commit()


async def get_cart(user_id):
    return cart_cur.execute('SELECT * FROM cart WHERE user_id == ?', [user_id]).fetchall()


async def get_score(user_id):
    return (m_cur.execute('SELECT score FROM users WHERE id == ?', [user_id]).fetchone())[0]

async def get_delivery(user_id):
    return (m_cur.execute('SELECT delivery FROM users WHERE id == ?', [user_id]).fetchone())[0]

async def get_lang(user_id):
    return (m_cur.execute('SELECT lang FROM users WHERE id == ?', [user_id]).fetchone())[0]

async def get_msg(user_id):
    return (m_cur.execute('SELECT msg FROM users WHERE id == ?', [user_id]).fetchone())[0]

async def get_count_cart(user_id, name):
    count_food = cart.execute('SELECT count FROM cart WHERE user_id == ? AND name == ?', [user_id, name]).fetchall()
    if len(count_food) <= 0:
        return False
    return count_food


async def change_count(user_id, name, count):
    cart_cur.execute('UPDATE cart SET count = ? WHERE user_id == ? AND name == ?', [count, user_id, name])
    cart.commit()


async def remove_one_item(user_id, name):
    cart_cur.execute('DELETE FROM cart WHERE user_id == ? AND name == ?', [user_id, name])
    cart.commit()


async def empty_cart(user_id):
    cart_cur.execute('DELETE FROM cart WHERE user_id == ?', [user_id, ]).fetchall()
    cart.commit()


async def add_msg(id, msg):
    m_cur.execute('UPDATE users SET msg = ? WHERE id == ?', [msg,  id])
    mod.commit()

async def add_state_pay(id, state):
    m_cur.execute('UPDATE users SET state_pay = ? WHERE id == ?', [state,  id])
    mod.commit()


async def add_cat(id, cat):
    m_cur.execute('UPDATE users SET cat = ? WHERE id == ?', [cat,  id])
    mod.commit()


async def add_deliv(id, deliv):
    m_cur.execute('UPDATE users SET delivery = ? WHERE id == ?', [deliv,  id])
    mod.commit()


async def get_deliv(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchone()
    return info[6]


async def add_address(id, address):
    m_cur.execute('UPDATE users SET address = ? WHERE id == ?', [address,  id])
    mod.commit()


async def get_address(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchone()
    return info[11]


async def add_offer(id, offer):
    m_cur.execute('UPDATE users SET offer = ? WHERE id == ?', [offer,  id])
    mod.commit()


async def get_offer(id):
    info = m_cur.execute('SELECT * FROM users WHERE id == ?', [id, ]).fetchone()
    return info[9]