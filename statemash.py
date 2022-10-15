from aiogram.dispatcher.filters.state import StatesGroup, State


class AddBike(StatesGroup):
    Model = State()
    RegNumber = State()
    Owner = State()
    OwnerPrise = State()
    photo = State()

class AddOwner(StatesGroup):
    owner = State()
    contact = State()

class AddQRPetrol(StatesGroup):
    RegNumber = State()
    QRFile = State()