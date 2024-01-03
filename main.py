# Gerekli kütüphanelerin import edilmesi
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
import pandas as pd

# Hedef web sayfasının URL'si
adres = "https://tr.wikipedia.org/wiki/T%C3%BCrk_dizileri_listesi"

# Tarayıcı bilgisi içeren başlık bilgisi
baslik = {
    'user-agent': "..."}

# Web sayfasından içerik çekme
sayfa = requests.get(adres, headers=baslik)
icerik = bs(sayfa.content, 'html.parser')

# Web sayfasından tüm tabloları çekme
tablo_listesi = icerik.find_all('table', {'class': 'wikitable'})


# Belirli bir diziye ait bilgileri çeken fonksiyon
def dizi_bilgileri_cek(dizi_url):
    bilgiler = {}
    sayfa = requests.get(dizi_url, headers=baslik)
    icerik = bs(sayfa.content, 'html.parser')
    infobox = icerik.find('table', {'class': 'infobox'})
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            if header:
                header_text = header.get_text().strip()
                value = row.find('td')
                if value and header_text in istenen_bilgiler:
                    value_text = value.get_text().strip()
                    bilgiler[header_text] = value_text
    return bilgiler


# Çekmek istenen dizi bilgilerinin listesi
istenen_bilgiler = ['Format', 'Tür', 'Senarist', 'Yönetmen', 'Başrol', 'Gösterim süresi',
                    'Kanal', 'Durumu', 'Besteci', 'Sezon sayısı', 'Bölüm sayısı', 'Yapımcı',
                    'Yapım şirketi', 'Yayın tarihi', 'Platform']

dizi_listesi = []

# Ana sayfadaki her tabloyu ve içindeki dizileri dolaşan döngü
for tablo in tablo_listesi:
    satirlar = tablo.find_all('tr')
    for i in range(len(satirlar)):
        satir = satirlar[i]
        hücreler = satir.find_all(['th', 'td'])
        dizi_linki = hücreler[0].find('a', href=True)
        if dizi_linki:
            dizi_adı = dizi_linki.get_text().strip()
            dizi_url = urllib.parse.urljoin(adres, dizi_linki['href'])
            bilgiler = dizi_bilgileri_cek(dizi_url)
            bilgiler['Dizi Adı'] = dizi_adı
            dizi_listesi.append(bilgiler)

# Elde edilen bilgileri bir DataFrame'e dönüştürme
df = pd.DataFrame(dizi_listesi)

# DataFrame'i Excel dosyası olarak kaydetme
excel_adı = 'turk_dizileri.xlsx'
df.to_excel(excel_adı, index=False)

# Kaydetme işleminin tamamlandığını bildiren mesaj
print(f"Excel dosyası '{excel_adı}' adıyla kaydedildi.")
