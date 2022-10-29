from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils import executor
import buttons as but
import ossistem as osSiS
from config import BOT_TOKEN, id_dopusk, id_gosha
from SQLBD import SQL
from statemash import AddBike, AddOwner, AddQRPetrol, AddBookingBike
from weather import get_weather

osSiS.checkDir()

BD = SQL()
BD.checkDB()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])  # /start command processing
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    if message.chat.id in id_dopusk:
        markup.add(but.newWeekStart, but.GiveQR, but.BikesMenu, but.somethingNew)
        await bot.send_message(message.chat.id, f"На данный момент есть свободных байков: {len(BD.checkBikesSQL('free'))}"
                                                f"\nвсего байков: {len(BD.checkallBikesSQL())}")
        await bot.send_message(message.chat.id, f"До конца недели осталось {BD.howMutchIsTheFish()}L", reply_markup=markup)
    elif BD.CheckAccount(message):
        markup.add(but.GiveQRclient, but.ShowFreeBikesClient)
        await bot.send_message(message.chat.id, f"Привет, это бот по мопедам и сопутствующего\n"
                             f"Отправь мне локацию, расскажу погоду)", reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, f"Заявка отправлена модератору, ожидай.")
        await bot.send_message(id_gosha, f"Кто-то {message.chat.first_name} хочет топлива\n"
                                         f"Вот его ID {message.chat.id}", reply_markup=but.knopkaADDAccount
        (message.chat.id, message.chat.first_name))

@dp.callback_query_handler(lambda c: c.data == "start")  # /start command processing
async def begin(call: types.callback_query):
    markup = InlineKeyboardMarkup(row_width=1)
    if call.message.chat.id in id_dopusk:
        markup.add(but.newWeekStart, but.GiveQR, but.BikesMenu, but.somethingNew)
        await bot.send_message(call.message.chat.id, f"На данный момент есть свободных байков: {len(BD.checkBikesSQL('free'))}"
                                                f"\nвсего байков: {len(BD.checkallBikesSQL())}")
        await bot.send_message(call.message.chat.id, f"До конца недели осталось {BD.howMutchIsTheFish()}L", reply_markup=markup)
    elif BD.CheckAccount(call.message):
        markup.add(but.GiveQRclient, but.ShowFreeBikesClient)
        await bot.send_message(call.message.chat.id, f"Привет, это бот по мопедам и сопутствующего\n"
                             f"Отправь мне локацию, расскажу погоду)", reply_markup=markup)
    else:
        await bot.send_message(call.message.chat.id, f"Заявка отправлена модератору, ожидай.")
        await bot.send_message(id_gosha, f"Кто-то {call.message.chat.first_name} хочет топлива\n"
                                         f"Вот его ID {call.message.chat.id}", reply_markup=but.knopkaADDAccount
        (call.message.chat.id, call.message.chat.first_name))

@dp.callback_query_handler(but.cb.filter())  # adds the account to the table
async def button_hendler(query: types.CallbackQuery, callback_data: dict):
    username, id = callback_data.get('username'), callback_data.get("id")
    BD.addAccountSQL(username, id)
    markup = InlineKeyboardMarkup().add(but.GiveQR)
    await bot.send_message(id, "Поздравляю, тебе доступны QR коды для заправки, недельный лимит 8 литров",
                           reply_markup=markup)
    await bot.send_message(id_gosha, "Добавлено")

@dp.callback_query_handler(lambda c: c.data == "newWeekStart")
async def newWeekStart(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    markup.add(but.GiveQR)
    BD.nullCount()
    await bot.send_message(call.message.chat.id, "Все qr обнулились", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "GiveQR")  #даёт qr
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup().add(but.sushi, but.Kosiak)
    try:
        global name
        name = BD.giveFreshQR()
        photo = open(f"{osSiS.DirQR}/{name}.jpg", "rb")
        BD.changeCount('0', name)
        markup = InlineKeyboardMarkup().add(but.sushi, but.Kosiak)
        await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
        await bot.answer_callback_query(call.id)
    except:
        markup = InlineKeyboardMarkup().add(but.home)
        await bot.send_message(call.message.chat.id, "Топливо на неделю кончилось", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "GiveQRclient")  #даёт qr
async def giveQRclient(call: types.callback_query):
    markup = InlineKeyboardMarkup().add(but.sushi, but.Kosiak)
    try:
        global name
        name = BD.giveFreshQR()
        photo = open(f"{osSiS.DirQR}/{name}.jpg", "rb")
        BD.changeCount('0', name)
        await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
        await bot.answer_callback_query(call.id)
    except:
        await bot.send_message(call.message.chat.id, "Топливо на неделю кончилось")

@dp.callback_query_handler(lambda c: c.data == "Kosiak")
async def kosiak(call: types.callback_query):
    markup = InlineKeyboardMarkup().add(but.home, but.GiveQR)
    await bot.send_message(call.message.chat.id, "QR помечен не рабочим", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "somethingNew")  #создает список пополняемого
async def somethingNew(call: types.callback_query):
    markup = InlineKeyboardMarkup(row_width=1).add(
        but.DownloadQR, but.addNewBike, but.addNewOwner)
    await bot.send_message(call.message.chat.id, "что же нового появилось?", reply_markup=markup)

"""add new bike"""
@dp.callback_query_handler(lambda c: c.data == 'addNewBike', state=None)  #добавление байка в базу
async def continueReg(call: types.callback_query):
    await AddBike.Model.set()
    await bot.send_message(call.message.chat.id, "Производитель и модель байка", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddBike.Model)  #запрашивает номер байка
async def ShowNotFullReg(message: types.Message, state: FSMContext):
    await state.update_data(Model=message.text.upper())
    await AddBike.RegNumber.set()
    await message.answer("Регистрационный номер байка", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddBike.RegNumber)  #запрашивает оунера
async def OwnerChoise(message: types.Message, state: FSMContext):
    await state.update_data(RegNumber=message.text.upper())
    global NewBike
    data = await state.get_data()
    NewBike = (data['Model'], data['RegNumber'])
    await state.finish()
    await message.answer(f"Оунер байка", reply_markup=but.makeButtonAgent())

@dp.callback_query_handler(but.buttonAgent.filter())  # adds the account to the table
async def button_hendler(call: types.callback_query, callback_data: dict, state: FSMContext):
    agent = callback_data.get('agent')
    await state.update_data(Owner=agent)
    await AddBike.OwnerPrise.set()
    await bot.send_message(call.message.chat.id, f"Стоимость байка", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddBike.OwnerPrise)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(Model=NewBike[0])
    await state.update_data(RegNumber=NewBike[1])
    await state.update_data(OwnerPrise=message.text)
    data = await state.get_data()
    await message.answer(f"Модель: {data['Model']}\n"
                         f"Номер: {data['RegNumber']}\n"
                         f"Оунер: {data['Owner']}\n"
                         f"Стоимость байка {data['OwnerPrise']} LKR\n"
                         f"Стоимость байка в день {int(int(data['OwnerPrise'])/31)} LKR\n")
    await AddBike.photo.set()
    await message.answer("Добавь фотографию байка", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddBike.photo, content_types=['photo']) #
async def get_photo(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=1).add(but.ShowFreeBikes, but.home)
    await state.update_data(photo=message.photo)
    data = await state.get_data()
    BD.addBikeToSQL(data)
    name = data['RegNumber']
    await message.photo[-1].download(destination_file=f'{osSiS.DirBikes}/{name}.jpg')
    await message.answer("байк добавлен в базу", reply_markup=markup)
    await state.finish()

"""add New Owner"""
@dp.callback_query_handler(lambda c: c.data == 'addNewOwner', state=None)  #добавление оунера в базу
async def continueReg(call: types.callback_query):
    await AddOwner.owner.set()
    await bot.send_message(call.message.chat.id, "ВВеди нового оунера", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddOwner.owner)  #запрашивает контакт оунера
async def CourseChoise(message: types.Message, state: FSMContext):
    await state.update_data(owner=message.text)
    await AddOwner.contact.set()
    await message.answer(f"Контакт оунера", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddOwner.contact)  #сообщает о сохранении оунера
async def CourseChoise(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=1).add(but.ShowFreeBikes, but.home)
    await state.update_data(contact=message.text)
    data = await state.get_data()
    BD.addOwnerToSQL(data)
    await message.answer(f"Oунер сохранен", reply_markup=markup)
    await state.finish()

"""add QR to Base"""
@dp.callback_query_handler(lambda c: c.data == 'DownoadQR', state=None)  #добавление QR в базу
async def continueReg(call: types.callback_query):
    await AddQRPetrol.RegNumber.set()
    await bot.send_message(call.message.chat.id, "Номер байка к которому привязан QR", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddQRPetrol.RegNumber)  #запрашивает номер байка от которого qr
async def CourseChoise(message: types.Message, state: FSMContext):
    await state.update_data(RegNumber=message.text.upper())
    await AddQRPetrol.QRFile.set()
    await message.answer(f"Добавить QR", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddQRPetrol.QRFile, content_types=['photo']) #загружает фотографии QR
async def get_photo_QR(message: types.Message, state: FSMContext):
    await state.update_data(QRFile=message.photo)
    data = await state.get_data()
    name = data["RegNumber"]
    if BD.addQRCode(name):
        await message.photo[-1].download(destination_file=f'{osSiS.DirQR}/{name}.jpg')
        await message.answer("QR добавлен в базу")
    else:
        await message.answer("QR уже в базе")
    await state.finish()

"""Bikes Menu"""

@dp.callback_query_handler(lambda c: c.data == "BikesMenu")  #открывает меню по байкам для админа
async def BikesMenu(call: types.callback_query):
    markup = InlineKeyboardMarkup(row_width=1).add(but.ShowRentBikes, but.ShowFreeBikes, but.home)
    await bot.send_message(call.message.chat.id, "BikesMenu", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "ShowFreeBikes")  # show free bikes
async def ShowFreeBikes(call: types.callback_query):
    await bot.send_message(call.message.chat.id, f"На данный момент свободны:", reply_markup=but.makeButtonBikes('free'))

@dp.callback_query_handler(lambda c: c.data == "ShowRentBikes")  # show free bikes
async def ShowFreeBikes(call: types.callback_query):
    await bot.send_message(call.message.chat.id, f"Вот, что ездит в аренде", reply_markup=but.makeButtonBikes('rent'))
@dp.callback_query_handler(but.buttonFreeBikes.filter())  #
async def openBikeInfo(call: types.callback_query, callback_data: dict):
    markup = InlineKeyboardMarkup(row_width=1).add(but.ShowFreeBikes, but.home)
    if BD.giveBikefromSQL(callback_data.get('RegNumber'))[8] == 'free':
        markup.add(but.BookingBike(callback_data.get('RegNumber')))
    elif BD.giveBikefromSQL(callback_data.get('RegNumber'))[8] == 'rent':
        markup.add(but.StopBookingBike(callback_data.get('RegNumber')))
    bike = BD.giveBikefromSQL(callback_data.get('RegNumber'))
    await bot.send_message(call.message.chat.id, f"{bike[1]}\n{bike[2]}\nОунер: {bike[3]}\n"
                                                 f"Себес в месяц {bike[4]} LKR\nСебес в день {bike[5]} LKR")
    photo = open(f"{osSiS.DirBikes}/{bike[2]}.jpg", "rb")
    await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)

"""BookingBike"""

@dp.callback_query_handler(but.BikeStopRent.filter())  #
async def StopBookingBike(call: types.callback_query, callback_data: dict):
    markup = InlineKeyboardMarkup(row_width=1).add(but.home, but.BikesMenu)
    BD.StopRentBike(callback_data.get('RegNum'), "free")
    await bot.send_message(call.message.chat.id, BD.calculateRent(callback_data.get('RegNum')), reply_markup=markup)

@dp.callback_query_handler(but.BikeStartRent.filter(), state=None)  #
async def BookingBike(call: types.callback_query, callback_data: dict, state: FSMContext):
    await state.update_data(RegNumber=callback_data.get('RegNum'))
    await AddBookingBike.Client.set()
    await bot.send_message(call.message.chat.id, "WHO?", reply_markup=but.ButtonsClients())

@dp.message_handler(state=AddBookingBike.Client)  #
async def CourseChoise(message: types.Message, state: FSMContext):
    await state.update_data(Client=message.text)
    await AddBookingBike.Money.set()
    await message.answer(f"how much per day?", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddBookingBike.Money)  #
async def CourseChoise(message: types.Message, state: FSMContext):
    await state.update_data(Money=message.text)
    data = await state.get_data()
    if int(message.text) * 1.2 < int(BD.giveBikefromSQL(data['RegNumber'])[5]):
        await message.answer("работаем в минус!!!!!")
    await state.update_data(OwnerPrice=BD.giveBikefromSQL(data['RegNumber'])[5])
    await AddBookingBike.HowLong.set()
    await message.answer(f"how long?", reply_markup=but.cancelOperation())

@dp.message_handler(state=AddBookingBike.HowLong) #
async def get_photo_QR(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=1).add(but.ShowFreeBikes, but.home)
    await state.update_data(HowLong=message.text)
    data = await state.get_data()
    BD.giveBikeRent(data)
    await state.finish()
    await message.answer("bike booking complete", reply_markup=markup)

"""client"""
@dp.callback_query_handler(lambda c: c.data == "ShowFreeBikesClient")
async def ShowFreeBikesClient(call: types.callback_query):
    await bot.send_message(call.message.chat.id, "На данный момент есть свободные байки",
                           reply_markup=but.makeButtonBikesFC())

@dp.callback_query_handler(but.buttonFreeClient.filter())  #
async def continueReg(call: types.callback_query, callback_data: dict):
    bike = BD.giveBikefromSQL(callback_data.get('RegNumber'))
    await bot.send_message(call.message.chat.id, f"{bike[1]}\n{bike[2]}")
    photo = open(f"{osSiS.DirBikes}/{bike[2]}.jpg", "rb")
    await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=but.WatchBikes(bike[2]))

@dp.callback_query_handler(but.gofromWatchBikes.filter())  #
async def continueReg(call: types.callback_query, callback_data: dict):
    bike = BD.giveBikefromSQL(callback_data.get('RegNumber'))
    await bot.send_message(call.message.chat.id, "Заявка отправлена модератору")
    await bot.send_message(id_gosha, f"{call.message.chat.first_name} "
                                     f"оставил заявку на байк {bike[1]}, {bike[2]} себес {bike[4]}")

"""all"""
@dp.callback_query_handler(lambda c: c.data == "cancel", state="*")  #закрывает текущее действие
async def cancel(call: types.callback_query, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=1).add(but.home)
    await state.finish()
    await bot.send_message(call.message.chat.id, "Заполнение прекращено", reply_markup=markup)

@dp.message_handler(content_types=["location"])
async def location(message: types.Message):
    if message.location is not None:
        markup = InlineKeyboardMarkup(row_width=1).add(but.home)
        await bot.send_message(message.chat.id, get_weather
        (message.location.latitude, message.location.longitude), reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)