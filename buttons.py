from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from SQLBD import SQL

BD = SQL()

newWeekStart = InlineKeyboardButton("Обнулить все QR", callback_data="newWeekStart")
GiveQR = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
GiveQRclient = InlineKeyboardButton("Выдать QR", callback_data="GiveQRclient")
ShowFreeBikes = InlineKeyboardButton("Посмотреть доступные байки", callback_data="ShowFreeBikes")
somethingNew = InlineKeyboardButton("добавить что-то новое", callback_data="somethingNew")
DownloadQR = InlineKeyboardButton("Загрузить новый QR на топливо", callback_data="DownoadQR")
addNewBike = InlineKeyboardButton("Добавить новый байк", callback_data="addNewBike")
addNewOwner = InlineKeyboardButton("Добавить нового оунера", callback_data="addNewOwner")
sushi = InlineKeyboardButton("Заправился, спасибо)", callback_data="sushi")
Kosiak = InlineKeyboardButton("QR не работает", callback_data="Kosiak")
cancel = InlineKeyboardButton(f'Отменить заполнение', callback_data="cancel")
def cancelOperation():
    """Кнопка закрывания текущего действия"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(f'Отменить заполнение', callback_data="cancel")]])

cb = CallbackData('action', 'username', 'id')
def knopkaADDAccount(id, username):
    """Creates a button with the record id"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(f'Добавить @{username} в клуб!', callback_data=cb.new
        (id=id, username=username))]])

knopkaAgent = CallbackData('siski', 'agent')
def makeButtonAgent():
    buttons = InlineKeyboardMarkup(row_width=1)
    list = BD.makeButtonagentSQL()
    button_list = [InlineKeyboardButton(text=f"{name[1]}",
                                        callback_data=knopkaAgent.new(agent=name[1])) for name in list]
    buttons.add(*button_list)
    return buttons

knopkaFreeBikes = CallbackData('sosiski', 'RegNumber')
def makeButtonBikes():
    buttons = InlineKeyboardMarkup(row_width=1)
    list = BD.checkFreeBikesSQL()
    button_list = [InlineKeyboardButton(text=f"{name[0]}, {name[1]}, {name[2]} LKR",
                                        callback_data=knopkaFreeBikes.new(RegNumber=name[1])) for name in list]
    buttons.add(*button_list)
    return buttons