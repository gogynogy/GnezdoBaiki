import sqlite3

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
            OstalosL int NOT NULL DEFAULT 8
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `Bikes` (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Model TEXT,
            RegNumber TEXT,
            Owner TEXT,
            OwnerPrise INT,
            OwnerDayPrice INT,
            Profit INT,
            Status TEXT,
            PhotoLink TEXT
            )""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `Owners` (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT
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

    def addSQL(self, message):
        """checks if the photo exists in the database and adds"""
        name = message.photo[0].file_unique_id + ".jpeg"
        try:
            self.cursor.execute("SELECT qrname FROM QRPetrol WHERE qrname = (?)", (name,))
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
            self.cursor.execute('''UPDATE QRPetrol SET kolichestvo = ? WHERE qrname = ?''', (num, id))
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
        self.cursor.execute("SELECT qrname FROM QRPetrol WHERE kolichestvo = ?", ("4",))
        name = self.cursor.fetchone()
        return name[0]

    def changeCountClient(self, id):
        """changes the amount of fuel on the client's balance"""
        try:
            self.cursor.execute('''UPDATE accounts SET OstalosL = (OstalosL -4) WHERE IDTelegram = ?''', (id,))
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite changeCountClient", error)
        finally:
            self.conn.commit()

    def addBikeToSQL(self, data):
        """checks if the photo exists in the database and adds"""
        try:
            self.cursor.execute(f"INSERT INTO Bikes (Model, RegNumber, Owner, OwnerPrise, OwnerDayPrice) VALUES "
                                f"(?, ?, ?, ?, ?)", (data['Model'], data['RegNumber'], data['Owner'],
                                                     data['OwnerPrise'], int(int(data['OwnerPrise']) / 30)))
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