from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from SQLBD import SQL

BD = SQL()
#QR
newWeekStart = InlineKeyboardButton("Обнулить все QR", callback_data="newWeekStart")
GiveQR = InlineKeyboardButton("Выдать QR", callback_data="GiveQR")
GiveQRclient = InlineKeyboardButton("Выдать QR", callback_data="GiveQRclient")
DownloadQR = InlineKeyboardButton("Загрузить новый QR на топливо", callback_data="DownoadQR")
sushi = InlineKeyboardButton("Заправился, спасибо)", callback_data="sushi")
Kosiak = InlineKeyboardButton("QR не работает", callback_data="Kosiak")

#Bikes
BikesMenu = InlineKeyboardButton("bikes", callback_data="BikesMenu")
ShowFreeBikes = InlineKeyboardButton("Посмотреть доступные байки", callback_data="ShowFreeBikes")
ShowFreeBikesClient = InlineKeyboardButton("Посмотреть доступные байки", callback_data="ShowFreeBikesClient")
ShowRentBikes = InlineKeyboardButton("ShowRentBikes", callback_data="ShowRentBikes")
addNewBike = InlineKeyboardButton("Добавить новый байк", callback_data="addNewBike")
BookingBike = InlineKeyboardButton("BookingBike", callback_data="BookingBike")

#Owners
somethingNew = InlineKeyboardButton("добавить что-то новое", callback_data="somethingNew")
addNewOwner = InlineKeyboardButton("Добавить нового оунера", callback_data="addNewOwner")

#Menu
cancel = InlineKeyboardButton(f'Отменить заполнение', callback_data="cancel")
home = InlineKeyboardButton(f"Главное меню", callback_data="start")

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

buttonAgent = CallbackData('siski', 'agent')
def makeButtonAgent():
    buttons = InlineKeyboardMarkup(row_width=1)
    list = BD.makeButtonagentSQL()
    button_list = [InlineKeyboardButton(text=f"{name[1]}",
                                        callback_data=buttonAgent.new(agent=name[1])) for name in list]
    buttons.add(*button_list)
    return buttons

buttonFreeBikes = CallbackData('sosiski', 'RegNumber')
def makeButtonBikes():
    buttons = InlineKeyboardMarkup(row_width=1)
    free_bikes = BD.checkFreeBikesSQL()
    button_list = [InlineKeyboardButton(text=f"{name[0]}, {name[1]}, {name[2]} LKR",
                                        callback_data=buttonFreeBikes.new(RegNumber=name[1])) for name in free_bikes]
    buttons.add(*button_list)

    return buttons

buttonFreeClient = CallbackData('pososiski', 'RegNumber')
def makeButtonBikesFC():
    buttons = InlineKeyboardMarkup(row_width=1)
    free_bikes = BD.checkFreeBikesSQL()
    button_list = [InlineKeyboardButton(
        text=f"{name[0]}", callback_data=buttonFreeClient.new(RegNumber=name[1])) for name in free_bikes]
    buttons.add(*button_list)
    return buttons

gofromWatchBikes = CallbackData('kiski', 'RegNumber')
def WatchBikes(regNum):
    buttons = InlineKeyboardMarkup(row_width=1)
    button_list = [InlineKeyboardButton(text=f"i want it", callback_data=gofromWatchBikes.new(RegNumber=regNum)),
                   InlineKeyboardButton("Посмотреть доступные байки", callback_data="ShowFreeBikesClient"),
                   InlineKeyboardButton("Main menu", callback_data="start")]
    buttons.add(*button_list)
    return buttons
