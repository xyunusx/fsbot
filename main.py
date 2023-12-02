import os
import re
import sys
import calendar
import time
from datetime import datetime
from itertools import product
import pymysql
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from audioplayer import AudioPlayer
import locale
from telethon import TelegramClient, events, utils
import time

from selenium import webdriver
from selenium.webdriver.ie.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telethon.sync import TelegramClient, events

from chromedriver_py import binary_path # this will get you the path variable


# Current GMT time in a tuple format
current_GMT = time.gmtime()

# ts stores timestamp
ts = calendar.timegm(current_GMT)
# ! Standart giriş

def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)


session = os.environ.get('TG_SESSION', 'mesajoku')
session2 = os.environ.get('TG_SESSION2', 'mesajoku2')
api_id = "24194207"
api_hash = "c34d1a5e6add74ef68e0b2d845cada74"
proxy = None  # https://github.com/Anorov/PySocks

# Create and start the client so we can make requests (we don't here)
client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()
client2 = TelegramClient(session2, api_id, api_hash, proxy=proxy).start()

# `pattern` is a regex, see https://docs.python.org/3/library/re.html
# Use https://regexone.com/ if you want a more interactive way of learning.
#
# "(?i)" makes it case-insensitive, and | separates "options".

def zabah():
    an = datetime.now()
    locale.setlocale(locale.LC_ALL, '')
    tarih = datetime.strftime(an, '%c')
    parcala = tarih.split()
    tarihparca = parcala[0].split(".")
    sabah = (tarihparca[2]+"-"+tarihparca[1]+"-"+tarihparca[0]+ " 00:00:00")
    return sabah
    
@client.on(events.NewMessage(pattern=r'(?i).*\b()\b'))
async def handler(event):
    db = pymysql.connect(host='localhost', user='root', password='', db='bonus', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    baglanti = db.cursor()

    saat = zabah()
    ts = calendar.timegm(current_GMT)
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    mesaj = (event.text)
    mesaj = mesaj.replace("'","")
    ilk = mesaj.split()
    if ilk[0] == "kodbot":
        await client2.send_message(1945197206,"KodBot Online")
    if ilk[0] == "kodbot" and ilk[1] == "rapor":
       sorgu3 = f"SELECT * FROM promo where time > '{saat}'"
       baglanti.execute(sorgu3)
       rapor = baglanti.fetchall()
       sayim = len(rapor)
       await client2.send_message(1945197206,"KodBot Online - " + str(sayim))
    
    kelimesay = (len(ilk))

    durum = False

    mesajlar = []
    satırlar=mesaj.splitlines()
    uzunluk = (len(ilk))
    link_re = re.compile('(https?://\S+)')
    sor = None
    sor2 = None
    msj = "Beni bırakın Furkanı banlayın \n !ban @furkankbl"
    if mesaj == "!ban @fsburada_bot":
        await client2.send_message(1945197206,msj)

        

    if kelimesay == 2:
        kelime1 = ilk[0]
        kelime2 = ilk[1]
        sor = kelime1.find("https")
        sor2 = kelime2.find("https")
    if sor == 0:
        url = ilk[0]
        kod = ilk[1]
        durum = True
        print(1)
    elif sor2 == 0:
        url = ilk[1]
        kod = ilk[0]
        print(2)

        durum = True

    if durum == True:
        print("Durum aktif")
        try:
            db = pymysql.connect(host='localhost', user='root', password='', db='bonus', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
            baglanti = db.cursor()
            sorgu = "INSERT INTO `promo` (`id`, `kod`, `url`, `time`) VALUES (NULL, '"+kod+"','"+url+"', current_timestamp());"
            sonuclar = baglanti.execute(sorgu)
            db.commit()

            print(sor,sor2,mesaj)
            yeni = url +"\n\n`"+ kod +"`"
  
            await client2.send_message(1945197206,mesaj)
            svc = webdriver.ChromeService(executable_path=binary_path)
            driver = webdriver.Chrome(service=svc)
            driver.get(url)
        except:
            print("Kod daha önce paylaşılmış")
    else:
        print(mesaj)
    peer = event.peer_id
    chann = peer.channel_id
    arama = mesaj.find("https")
    username = name

    mesaj.replace("'","")
    mesaj.replace('"','')
    sorgu = f"INSERT INTO test (id, kanal, user, mesaj) VALUES (NULL, '{chann}','{username}', '{mesaj}')"
    sonuclar = baglanti.execute(sorgu)
    db.commit()

try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()

finally:
    client.disconnect()




