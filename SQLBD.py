import sqlite3
from datetime import datetime

from dateTime import GetFinishRentDate, GetToodayDate


class SQL:
    def __init__(self):
        """Initializing Database Connection"""
        self.conn = sqlite3.connect("baiki.db")
        self.cursor = self.conn.cursor()

    def checkDB(self):
        """проверяет наличие базы данных"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `QRPetrol` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Qrname TEXT,
            Kolichestvo int NOT NULL DEFAULT 4,
            Kosiak int NOT NULL DEFAULT 0
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `accounts` (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            TelegramNikName TEXT,
            IDTelegram TEXT,
            Prava TEXT NOT NULL DEFAULT no,
            NumRentBike TEXT NOT NULL DEFAULT NO
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `Bikes` (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Model TEXT,
            RegNumber TEXT,
            Owner TEXT,
            OwnerPrise INT,
            OwnerDayPrice INT,
            OwnerRentStart TEXT,
            Profit INT NOT NULL DEFAULT 0,
            Status NOT NULL DEFAULT free,
            curentRentFinish TEXT
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `Owners` (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `History` (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            bike TEXT,
            customer TEXT,
            dateStart TEXT,
            dateFinish TEXT,
            moneyPerDay TEXT,
            daysCount TEXT,
            moneyTotal TEXT
            )""")
        self.conn.commit()

    def howMutchIsTheFish(self):
        """counts the fuel balance"""
        try:
            self.cursor.execute(f"""SELECT SUM(kolichestvo) FROM `QRPetrol`""")
            result = self.cursor.fetchone()[0]
            return result
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFish", error)
        finally:
            self.conn.commit()

    def CheckAccount(self, message):
        """checks if the id exists in the database"""
        try:
            self.cursor.execute("SELECT IDTelegram FROM accounts WHERE IDTelegram = (?)", (message.chat.id,))
            if self.cursor.fetchone() is None:
                return False
            else:
                return True
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)
        finally:
            self.conn.commit()

    def addAccountSQL(self, username, id):
        """checks if the photo exists in the database and adds"""
        try:
            self.cursor.execute(f"INSERT INTO accounts (TelegramNikName, IDTelegram) VALUES (?, ?)", (username, id))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)
        finally:
            self.conn.commit()

    def howMutchIsTheFishClient(self, id):
        """counts the fuel balance"""
        try:
            self.cursor.execute(f"""SELECT SUM(OstalosL) FROM `accounts` WHERE IDTelegram = ?""", (id,))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite howMutchIsTheFishClient", error)

    def changeCount(self, num, id):  # changes the amount of fuel in the remainder
        try:
            self.cursor.execute('''UPDATE QRPetrol SET kolichestvo = ? WHERE Qrname = ?''', (num, id))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCount", error)
        finally:
            self.conn.commit()

    def nullCount(self):
        """zeroes in on fuel for the week"""
        try:
            self.cursor.execute('''UPDATE QRPetrol SET kolichestvo = 4''')
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite nullCount", error)
        finally:
            self.conn.commit()

    def giveFreshQR(self):
        """gives out a code with fuel"""
        try:
            self.cursor.execute("SELECT Qrname FROM QRPetrol WHERE kolichestvo = ?", ("4",))
            name = self.cursor.fetchone()
            return name[0]
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCountClient", error)
        finally:
            self.conn.commit()

    def changeCountClient(self, id):
        """changes the amount of fuel on the client's balance"""
        try:
            self.cursor.execute('''UPDATE accounts SET OstalosL = (OstalosL -4) WHERE IDTelegram = ?''', (id,))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCountClient", error)
        finally:
            self.conn.commit()

    def addQRCode(self, message):
        """checks if the photo exists in the database and adds"""
        name = message
        try:
            self.cursor.execute("SELECT Qrname FROM QRPetrol WHERE Qrname = (?)", (name,))
            data = self.cursor.fetchone()
            if data is None:
                self.cursor.execute(f"INSERT INTO QRPetrol (qrname) VALUES (?)", (name,))
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addSQL", error)
        finally:
            self.conn.commit()

    def addBikeToSQL(self, data):
        """checks if the photo exists in the database and adds"""
        try:
            self.cursor.execute(f"INSERT INTO Bikes (Model, RegNumber, Owner, OwnerPrise, OwnerDayPrice, OwnerRentStart)"
                                f" VALUES (?, ?, ?, ?, ?, ?)", (data['Model'], data['RegNumber'], data['Owner'],
                                data['OwnerPrise'], int(int(data['OwnerPrise']) / 30), str(GetToodayDate())))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addBikeToSQL", error)
        finally:
            self.conn.commit()

    def addOwnerToSQL(self, data):
        """checks if the photo exists in the database and adds"""
        try:
            self.cursor.execute(f"INSERT INTO Owners (name, contact) VALUES "
                                f"(?, ?)", (data['owner'], data['contact']))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite addBikeToSQL", error)
        finally:
            self.conn.commit()

    def makeButtonagentSQL(self):
        """выдает кнопки с агентами по локации"""
        try:
            self.cursor.execute("""SELECT * FROM Owners""")
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def checkBikesSQL(self, status):
        """gives out a code with fuel"""
        try:
            self.cursor.execute("SELECT Model, RegNumber, OwnerPrise, OwnerDayPrice "
                                "FROM Bikes WHERE Status = ?", (status,))
            name = self.cursor.fetchall()
            return name
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def checkallBikesSQL(self):
        """gives out a code with fuel"""
        try:
            self.cursor.execute("SELECT * FROM Bikes")
            name = self.cursor.fetchall()
            return name
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def giveBikefromSQL(self, reg_num):
        """gives out a code with fuel"""
        try:
            self.cursor.execute("SELECT * FROM Bikes WHERE RegNumber = ?", (reg_num,))
            bike = self.cursor.fetchone()
            return bike
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def checkClientLicense(self, id):
        """check drive license"""
        try:
            self.cursor.execute("SELECT Prava FROM accounts WHERE IDTelegram = ?", (id,))
            if self.cursor.fetchone()[0] == "no":
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def giveClientList(self):
        """check drive license"""
        try:
            self.cursor.execute("SELECT * FROM accounts")
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def StopRentBike(self, RegNumber, Status):
        try:
            self.cursor.execute('''UPDATE Bikes SET (Status, curentRentFinish) = (?, ?) WHERE RegNumber = ?''',
                                (Status, "None", RegNumber))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeStatusBike", error)
        finally:
            self.conn.commit()

    def giveBikeRent(self, data):
        profit = (int(data["Money"]) - int(data["OwnerPrice"])) * int(data["HowLong"])
        today = str(GetToodayDate())
        stopRent = str(GetFinishRentDate(data["HowLong"]))
        totalMoney = int(data["Money"]) * int(data["HowLong"])
        try:
            self.cursor.execute('''UPDATE accounts SET NumRentBike = ? WHERE TelegramNikName = ?''',
                                (data["RegNumber"], data["Client"]))
            self.cursor.execute('''UPDATE Bikes SET (Status, curentRentFinish) = (?, ?) WHERE RegNumber = ?''',
                                ("rent", stopRent, data["RegNumber"]))
            self.cursor.execute('''UPDATE Bikes SET Profit = (Profit + ?) WHERE RegNumber = ?''',
                                (int(profit), data["RegNumber"]))
            self.cursor.execute('''INSERT INTO History (bike, customer, dateStart, dateFinish, moneyPerDay, daysCount, 
                                moneyTotal) VALUES (?, ?, ?, ?, ?, ?, ?)''', (data["RegNumber"], data["Client"], today,
                                stopRent, data["Money"], data["HowLong"], totalMoney))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite giveBikeRent", error)
        finally:
            self.conn.commit()

    def calculateRent(self, regNumber):
        today = str(GetToodayDate())
        try:
            bike = self.giveBikefromSQL(regNumber)
            self.cursor.execute("SELECT * FROM History WHERE (bike, dateFinish) = (?, ?)", (regNumber, bike[9]))
            bikeHistory = self.cursor.fetchone()
            daysCount = datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(bikeHistory[3], "%Y-%m-%d")
            moneyTotal = daysCount.days * bikeHistory[6]
            moneyReturn = int(bikeHistory[5]) - int(moneyTotal)
            self.cursor.execute('''UPDATE History SET (dateFinish, daysCount, moneyTotal) WHERE 
            (bike, dateFinish) = (?, ?, ?, ?, ?, ?)''', (today, daysCount, moneyTotal, regNumber, bike[9]))
            # self.cursor.execute('''INSERT INTO History (bike, customer, dateStart, dateFinish) VALUES (?, ?, ?, ?)''',
            #                     (regNumber, client, today, stopRent))
            return f"байк {regNumber} пробыл в аренде {daysCount} стоимость периода {moneyTotal} возврат {moneyReturn}"
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite giveBikeRent", error)
        finally:
            self.conn.commit()

    def giveAccountInfo(self, telegramID):
        try:
            self.cursor.execute("""SELECT * FROM accounts WHERE IDTelegram = ?""", (telegramID, ))
            print(self.cursor.fetchone())
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)