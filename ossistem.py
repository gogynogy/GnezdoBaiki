import os

def checkDir():
    if not os.path.exists("QrCode"):
        os.mkdir("QrCode")
    if not os.path.exists("BikesPhoto"):
        os.mkdir("BikesPhoto")

DirQR = os.path.abspath("QrCode")
DirBikes = os.path.abspath("BikesPhoto")

