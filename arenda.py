from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils import executor
import buttons as but
import ossistem as osSiS
from config import TOKEN, id_dopusk, id_gosha
from SQLBD import SQL
from statemash import AddBike, AddOwner, AddQRPetrol

osSiS.checkDir()

BD = SQL()
BD.checkDB()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])  # /start command processing
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=1)
    if message.chat.id in id_dopusk:
        markup.add(but.newWeekStart, but.GiveQR, but.ShowFreeBikes, but.somethingNew)
        await bot.send_message(message.chat.id, f"На данный момент есть свободных байков: {len(BD.checkFreeBikesSQL())}")
        await bot.send_message(message.chat.id, f"До конца недели осталось {BD.howMutchIsTheFish()}L", reply_markup=markup)
    elif BD.CheckAccount(message):
        markup.add(but.GiveQRclient)
        count = BD.howMutchIsTheFishClient(message.chat.id)
        await bot.send_message(message.chat.id, f"Пс! Хочешь не много горючки?\n"
                             f"до конца недели осталось {count}L", reply_markup=markup)
    else:
        if message.chat.username == None:
            await bot.send_message(message.chat.id, f"доброе утро\nА потом мопед заправим.")
            await bot.send_message(id_gosha, f"Кто-то {message.chat.first_name} хочет топлива\n"
                                             f"Вот его ID {message.chat.id}", reply_markup=but.knopkaADDAccount
            (message.chat.id, message.chat.first_name))
        else:
            await bot.send_message(message.chat.id, f"доброе утро\nА потом мопед заправим.")
            await bot.send_message(id_gosha, f"Кто-то {message.chat.username} хочет топлива\n"
                                             f"Вот его ID {message.chat.id}", reply_markup=but.knopkaADDAccount
            (message.chat.id, message.chat.username))

@dp.callback_query_handler(but.cb.filter())  # adds the account to the table
async def button_hendler(query: types.CallbackQuery, callback_data: dict):
    username, id = callback_data.get('username'), callback_data.get("id")
    BD.addAccountSQL(username, id)
    markup = InlineKeyboardMarkup().add(but.GiveQR)
    await bot.send_message(id, "Поздравляю, тебе доступны QR коды для заправки, недельный лимит 8 литров",
                           reply_markup=markup)
    await bot.send_message(id_gosha, "Добавлено")

@dp.callback_query_handler(lambda c: c.data == "newWeekStart")
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    markup.add(but.GiveQR)
    BD.nullCount()
    await bot.send_message(call.message.chat.id, "Все qr обнулились", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "GiveQR")  #даёт qr
async def giveQR(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    markup.add(but.sushi, but.Kosiak)
    try:
        global name
        name = BD.giveFreshQR()
        photo = open(f"{name}", "rb")
        BD.changeCount('0', name)
        await bot.send_photo(call.message.chat.id, photo=photo, reply_markup=markup)
        await bot.answer_callback_query(call.id)
    except:
        await bot.send_message(call.message.chat.id, "Топливо на неделю кончилось")

@dp.callback_query_handler(lambda c: c.data == "somethingNew")  #даёт qr
async def giveQRclient(call: types.callback_query):
    markup = InlineKeyboardMarkup(row_width=1).add(
        but.DownloadQR, but.addNewBike, but.addNewOwner)
    await bot.send_message(call.message.chat.id, "что же нового появилось?", reply_markup=markup)

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
async def CourseChoise(message: types.Message, state: FSMContext):
    await state.update_data(RegNumber=message.text.upper())
    global NewBike
    data = await state.get_data()
    NewBike = (data['Model'], data['RegNumber'])
    await state.finish()
    await message.answer(f"Оунер байка", reply_markup=but.makeButtonAgent())

@dp.callback_query_handler(but.knopkaAgent.filter())  # adds the account to the table
async def button_hendler(call: types.callback_query, callback_data: dict, state: FSMContext):
    location = callback_data.get('agent')
    await state.update_data(Owner=location)
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

@dp.message_handler(state=AddBike.photo, content_types=['photo']) #дописать загрузку фотографий
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo)
    data = await state.get_data()
    BD.addBikeToSQL(data)
    name = data['RegNumber']
    await message.photo[-1].download(destination_file=f'{osSiS.DirBikes}/{name}.jpg')
    await message.answer("байк добавлен в базу")
    await state.finish()

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
    await state.update_data(contact=message.text)
    data = await state.get_data()
    BD.addOwnerToSQL(data)
    await message.answer(f"Oунер сохранен")
    await state.finish()

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


@dp.callback_query_handler(lambda c: c.data == "cancel", state="*")  #закрывает текущее действие
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Заполнение прекращено")

@dp.callback_query_handler(lambda c: c.data == "ShowFreeBikes")  #даёт qr
async def ShowFreeBikes(call: types.callback_query):
    await bot.send_message(call.message.chat.id, f"На данный момент свободны:", reply_markup=but.makeButtonBikes())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)

