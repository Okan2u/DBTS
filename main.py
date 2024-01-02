# Adım 1: Temel Yapı Oluşturma

import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
import pandas as pd

# Wikipedia sayfasından veri çekme
adres = "https://tr.wikipedia.org/wiki/T%C3%BCrk_dizileri_listesi"
baslik = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
sayfa = requests.get(adres, headers=baslik)
icerik = bs(sayfa.content, 'html.parser')
tablo_listesi = icerik.find_all('table', {'class': 'wikitable'})
