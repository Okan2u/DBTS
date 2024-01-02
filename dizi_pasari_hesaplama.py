import pandas as pd
from sklearn.impute import SimpleImputer

# Adım 2: Başarı Skorları Hesaplama ve Sıralama

def calculate_score(df, column):
    """
    Verilen sütunun başarı skorlarını hesaplar ve DataFrame'e ekler.
    Skor, her bir değerin frekansına göre orantılı olarak belirlenir.
    """
    # Sütundaki değerlerin sayısını hesapla
    scores = df[column].value_counts().to_dict()

    # Her bir değerin skorunu oransal olarak hesapla
    df[column + '_score'] = df[column].map(scores)
    df[column + '_score'] = df[column + '_score'] / df[column + '_score'].max()

    return df

def calculate_numeric_score(df, column):
    """
    Sayısal bir sütun için normalleştirilmiş skorlar hesaplar ve DataFrame'e ekler.
    Skor, her bir değerin maksimum değere oranı olarak hesaplanır.
    """
    # Sayısal sütunu normalleştirilmiş skorları ile güncelle
    df[column + '_score'] = df[column] / df[column].max()
    return df

def sort_by_year(df):
    """
    DataFrame'i yapım yılına göre sıralar.
    """
    df = df.sort_values(by='Yapım Yılı')
    return df


def calculate_yearly_comparison(df):
    pass


def fill_empty_success_scores(df):
    pass


def format_success_percentage(df):
    pass


def impute_missing_values(df):
    pass


def main():
    # Excel dosyasından veriyi oku
    df = pd.read_excel('turk_dizileri.xlsx')

    # Eksik değerleri doldur (Adım 1'den)
    df = impute_missing_values(df)

    # Yapım yılına göre sırala
    df = sort_by_year(df)

    # Kategorik sütunlar için başarı skorlarını hesapla
    df = calculate_score(df, 'Format')
    df = calculate_score(df, 'Tür')
    df = calculate_score(df, 'Kanal')
    df = calculate_score(df, 'Yapım Şirketi')

    # Sayısal sütunlar için başarı skorlarını hesapla
    df = calculate_numeric_score(df, 'Gösterim Süresi')
    df = calculate_numeric_score(df, 'Sezon Sayısı')
    df = calculate_numeric_score(df, 'Bölüm Sayısı')

    # Adım 3: Yıllık Karşılaştırma ve Boş Başarı Skorları Doldurma
    df = calculate_yearly_comparison(df)
    df = fill_empty_success_scores(df)
    df = format_success_percentage(df)

    # Başarı yüzdesini kaydet
    df[['Dizi Adı', 'Overall_Success_Score']].to_excel('Başarı_Yüzdeleri.xlsx', index=False)

if __name__ == "__main__":
    main()
