import pandas as pd
from sklearn.impute import SimpleImputer

from main import calculate_yearly_comparison


# Adım 4: Boş Başarı Skorlarını Doldurma

def fill_empty_success_scores(df):
    """
    Boş olan başarı skorlarını doldurur.
    """
    # Başarı skorlarını hesapla ve genel başarı skoru olarak ortalamalarını al
    scores_columns = ['Format_score', 'Tür_score', 'Kanal_score', 'Yapım Şirketi_score',
                      'Gösterim Süresi_score', 'Sezon Sayısı_score', 'Bölüm Sayısı_score', 'Yearly_Success_Score']
    df['Overall_Success_Score'] = df[scores_columns].mean(axis=1) * 2  # Başarı skorlarını 2 ile çarp

    return df

def format_success_percentage(df):
    """
    Başarı yüzdesini formatlar ve DataFrame'e ekler.
    """
    # Başarı yüzdesini yüzdelik formata dönüştür ve DataFrame'e ekler
    df[['Dizi Adı', 'Overall_Success_Score']] = df[['Dizi Adı', 'Overall_Success_Score']].astype(str)
    df['Overall_Success_Score'] = (df['Overall_Success_Score'].astype(float) * 100).round(2).astype(str) + '%'

    return df


def calculate_numeric_score(df, param):
    pass


def calculate_score(df, param):
    pass


def sort_by_year(df):
    pass


def impute_missing_values(df):
    pass


def main():
    # Excel dosyasından veriyi oku
    df = pd.read_excel('turk_dizileri.xlsx')

    # Adım 1: Eksik değerleri doldur
    df = impute_missing_values(df)

    # Adım 2: Yapım yılına göre sırala
    df = sort_by_year(df)

    # Adım 2: Kategorik ve sayısal sütunlar için başarı skorlarını hesapla
    df = calculate_score(df, 'Format')
    df = calculate_score(df, 'Tür')
    df = calculate_score(df, 'Kanal')
    df = calculate_score(df, 'Yapım Şirketi')
    df = calculate_numeric_score(df, 'Gösterim Süresi')
    df = calculate_numeric_score(df, 'Sezon Sayısı')
    df = calculate_numeric_score(df, 'Bölüm Sayısı')

    # Adım 3: Yıllık Karşılaştırma ve Boş Başarı Skorları Doldurma
    df = calculate_yearly_comparison(df)

    # Adım 4: Boş Başarı Skorlarını Doldur
    df = fill_empty_success_scores(df)

    # Adım 5: Başarı Yüzdesini Formatla ve Kaydet
    df = format_success_percentage(df)
    df[['Dizi Adı', 'Overall_Success_Score']].to_excel('Başarı_Yüzdeleri.xlsx', index=False)

if __name__ == "__main__":
    main()
