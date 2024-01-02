import requests
from bs4 import BeautifulSoup as bs
import urllib.parse
import pandas as pd

# Wikipedia sayfasının adresi
adres = "https://tr.wikipedia.org/wiki/T%C3%BCrk_dizileri_listesi"

# HTTP isteği yaparken kullanılacak başlık
baslik = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Wikipedia sayfasını çekme
sayfa = requests.get(adres, headers=baslik)
icerik = bs(sayfa.content, 'html.parser')

# Tablo verilerini içeren HTML etiketlerini bulma
tablo_listesi = icerik.find_all('table', {'class': 'wikitable'})

# Dizi bilgilerini çekme fonksiyonu
def dizi_bilgileri_cek(dizi_url):
    """
    Verilen dizi URL'sinden gerekli bilgileri çeken fonksiyon.
    """
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

# Çekilecek dizi bilgilerinin listesi
istenen_bilgiler = ['Format', 'Tür', 'Senarist', 'Yönetmen', 'Başrol', 'Gösterim süresi',
                    'Kanal', 'Durumu', 'Besteci', 'Sezon sayısı', 'Bölüm sayısı', 'Yapımcı',
                    'Yapım şirketi', 'Yayın tarihi', 'Platform']

# Dizi bilgilerini toplamak için boş liste
dizi_listesi = []

# Wikipedia sayfasındaki tablolardaki satırları ve hücreleri döngü içinde kontrol etme
for tablo in tablo_listesi:
    satirlar = tablo.find_all('tr')
    for i in range(len(satirlar)):
        satir = satirlar[i]
        hucreler = satir.find_all(['th', 'td'])
        dizi_linki = hucreler[0].find('a', href=True)
        if dizi_linki:
            dizi_adi = dizi_linki.get_text().strip()
            dizi_url = urllib.parse.urljoin(adres, dizi_linki['href'])
            bilgiler = dizi_bilgileri_cek(dizi_url)
            bilgiler['Dizi Adı'] = dizi_adi
            dizi_listesi.append(bilgiler)

# Dizi bilgilerini içeren liste üzerinden DataFrame oluşturma
df = pd.DataFrame(dizi_listesi)

# Excel dosyasına kaydetme işlemi
excel_adı = 'turk_dizileri.xlsx'
df.to_excel(excel_adı, index=False)
print(f"Excel dosyası '{excel_adı}' adıyla kaydedildi.")
