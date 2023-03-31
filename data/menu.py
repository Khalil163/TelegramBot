# from data import sql
#
#
# names_file = open(r'C:\Users\79025\Desktop\Projects\Python\TelegramBot\data\foods.txt', 'r',encoding="utf-8")
# prices_file = open(r'C:\Users\79025\Desktop\Projects\Python\TelegramBot\data\prices.txt', 'r',encoding="utf-8")
# items_file = open(r'C:\Users\79025\Desktop\Projects\Python\TelegramBot\data\items.txt', 'r',encoding="utf-8")
#
# names = [line.strip() for line in names_file]
# print(names, len(names))
# prices = [int(line.strip().replace(',00', '')) for line in prices_file]
# print(prices, len(prices))
# items = [line.strip() for line in items_file]
# print(items, len(items))
#
#
# async def write_menu():
#     for i in range(len(names)):
#         a = {'name': names[i], 'price': prices[i], 'item': items[i], 'stoplist': 'ЕСТЬ'}
#         await sql.add_menu(a)
#
#
#
#
# names_file.close()
# prices_file.close()
# items_file.close()
