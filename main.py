import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

from dizi_pasari_hesaplama import format_success_percentage, calculate_numeric_score, calculate_score, sort_by_year, \
    impute_missing_values


# Adım 3: Yıllık Karşılaştırma ve Boş Başarı Skorları Doldurma

def calculate_yearly_comparison(df):
    """
    Yıllık karşılaştırmayı yaparak, her dizi için yıllık başarı skorunu hesaplar.
    """
    df['Yearly_Success_Score'] = 0.0  # Başlangıçta tüm yıllık başarı skorlarını 0 olarak ayarla
    imputer = SimpleImputer(strategy='mean')  # Eksik değerleri ortalama ile doldur

    for year in df['Yapım Yılı'].unique():
        subset = df[df['Yapım Yılı'] == year]
        subset_index = subset.index.tolist()

        # Önceki yıllardaki verileri eğitim verisi olarak kullan
        previous_years = df[df['Yapım Yılı'] < year]
        training_data = previous_years.drop(subset_index, errors='ignore')

        # Eğitim verisi varsa, modeli eğit
        if not training_data.empty:
            numeric_columns = ['Gösterim Süresi', 'Sezon Sayısı', 'Bölüm Sayısı']
            X_train = training_data[numeric_columns]
            X_test = subset[numeric_columns]

            # Eksik değerleri doldur
            X_train_imputed = imputer.fit_transform(X_train)
            X_test_imputed = imputer.transform(X_test)

            y_train = training_data['Yearly_Success_Score']

            # Lineer Regresyon modelini eğit
            model = LinearRegression()
            model.fit(X_train_imputed, y_train)

            # Test verileri için tahminler yap ve güncelle
            subset.loc[:, 'Yearly_Success_Score'] = model.predict(X_test_imputed)
            df.update(subset)

    return df

def fill_empty_success_scores(df):
    """
    Boş olan başarı skorlarını doldurur.
    """
    # Başarı skorlarını hesapla ve genel başarı skoru olarak ortalamalarını al
    scores_columns = ['Format_score', 'Tür_score', 'Kanal_score', 'Yapım Şirketi_score',
                      'Gösterim Süresi_score', 'Sezon Sayısı_score', 'Bölüm Sayısı_score', 'Yearly_Success_Score']
    df['Overall_Success_Score'] = df[scores_columns].mean(axis=1) * 2  # Başarı skorlarını 2 ile çarp

    return df

def main():
    # Excel dosyasından veriyi oku
    df = pd.read_excel('turk_dizileri.xlsx')

    # Eksik değerleri doldur (Adım 1'den)
    df = impute_missing_values(df)

    # Yapım yılına göre sırala (Adım 2'den)
    df = sort_by_year(df)

    # Kategorik ve sayısal sütunlar için başarı skorlarını hesapla (Adım 2'den)
    df = calculate_score(df, 'Format')
    df = calculate_score(df, 'Tür')
    df = calculate_score(df, 'Kanal')
    df = calculate_score(df, 'Yapım Şirketi')
    df = calculate_numeric_score(df, 'Gösterim Süresi')
    df = calculate_numeric_score(df, 'Sezon Sayısı')
    df = calculate_numeric_score(df, 'Bölüm Sayısı')

    # Yıllık karşılaştırma ve boş başarı skorları doldurma
    df = calculate_yearly_comparison(df)
    df = fill_empty_success_scores(df)

    # Adım 4 ve 5: Skorları Yüzde Olarak Formatlama ve Sonuçları Kaydetme
    df = format_success_percentage(df)
    df[['Dizi Adı', 'Overall_Success_Score']].to_excel('Başarı_Yüzdeleri.xlsx', index=False)

if __name__ == "__main__":
    main()
