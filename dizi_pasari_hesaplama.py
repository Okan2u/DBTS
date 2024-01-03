import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer


# Eksik değerleri doldurmak için kullanılan fonksiyon
def impute_missing_values(df):
    """
    Verilen DataFrame'deki sayısal sütunlardaki eksik değerleri ortalama ile doldurur.
    """
    numeric_columns = ['Gösterim Süresi', 'Sezon Sayısı', 'Bölüm Sayısı']
    imputer = SimpleImputer(strategy='mean')

    for column in numeric_columns:
        if column not in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')

    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
    return df


# Kategorik sütunlar için başarı skorlarını hesaplamak için kullanılan fonksiyon
def calculate_score(df, column):
    """
    Verilen DataFrame'deki kategorik bir sütun için başarı skorlarını hesaplar ve DataFrame'e ekler.
    """
    scores = df[column].value_counts().to_dict()
    df[column + '_score'] = df[column].map(scores)
    df[column + '_score'] = df[column + '_score'] / df[column + '_score'].max()
    return df


# Sayısal sütunlar için başarı skorlarını hesaplamak için kullanılan fonksiyon
def calculate_numeric_score(df, column):
    """
    Verilen DataFrame'deki sayısal bir sütun için normalleştirilmiş skorlar hesaplar ve DataFrame'e ekler.
    """
    df[column + '_score'] = df[column] / df[column].max()
    return df


# Yıllık karşılaştırma yaparak boş başarı skorlarını dolduran fonksiyon
def calculate_yearly_comparison(df):
    """
    Verilen DataFrame'e yıllık karşılaştırma yaparak boş başarı skorlarını doldurur.
    """
    df['Yearly_Success_Score'] = 0.0
    imputer = SimpleImputer(strategy='mean')

    for year in df['Yapım Yılı'].unique():
        subset = df[df['Yapım Yılı'] == year]
        subset_index = subset.index.tolist()

        previous_years = df[df['Yapım Yılı'] < year]
        training_data = previous_years.drop(subset_index, errors='ignore')

        if not training_data.empty:
            numeric_columns = ['Gösterim Süresi', 'Sezon Sayısı', 'Bölüm Sayısı']
            X_train = training_data[numeric_columns]
            X_test = subset[numeric_columns]

            X_train_imputed = imputer.fit_transform(X_train)
            X_test_imputed = imputer.transform(X_test)

            y_train = training_data['Yearly_Success_Score']

            model = LinearRegression()
            model.fit(X_train_imputed, y_train)

            subset.loc[:, 'Yearly_Success_Score'] = model.predict(X_test_imputed)
            df.update(subset)

    return df


# Başarı skorlarını genel başarı skoruna dönüştüren fonksiyon
def fill_empty_success_scores(df):
    """
    Verilen DataFrame'deki boş başarı skorlarını doldurur ve genel başarı skorunu hesaplar.
    """
    scores_columns = ['Format_score', 'Tür_score', 'Kanal_score', 'Yapım Şirketi_score',
                      'Gösterim Süresi_score', 'Sezon Sayısı_score', 'Bölüm Sayısı_score', 'Yearly_Success_Score']

    df['Overall_Success_Score'] = df[scores_columns].mean(axis=1) * 2
    return df


# Başarı yüzdesini formatlayan fonksiyon
def format_success_percentage(df):
    """
    Verilen DataFrame'deki başarı yüzdesini formatlar ve DataFrame'e ekler.
    """
    df[['Dizi Adı', 'Overall_Success_Score']] = df[['Dizi Adı', 'Overall_Success_Score']].astype(str)
    df['Overall_Success_Score'] = (df['Overall_Success_Score'].astype(float) * 100).round(2).astype(str) + '%'
    return df


# Ana işlemleri gerçekleştiren fonksiyon
def main():
    """
    Verilen Excel dosyasındaki veriyi işleyerek başarı yüzdelerini hesaplar ve kaydeder.
    """
    df = pd.read_excel('turk_dizileri.xlsx')

    df = impute_missing_values(df)
    df = df.sort_values(by='Yapım Yılı')

    df = calculate_score(df, 'Format')
    df = calculate_score(df, 'Tür')
    df = calculate_score(df, 'Kanal')
    df = calculate_score(df, 'Yapım Şirketi')

    df = calculate_numeric_score(df, 'Gösterim Süresi')
    df = calculate_numeric_score(df, 'Sezon Sayısı')
    df = calculate_numeric_score(df, 'Bölüm Sayısı')

    df = calculate_yearly_comparison(df)
    df = fill_empty_success_scores(df)
    df = format_success_percentage(df)

    df[['Dizi Adı', 'Overall_Success_Score']].to_excel('Başarı_Yüzdeleri.xlsx', index=False)


if __name__ == "__main__":
    main()
