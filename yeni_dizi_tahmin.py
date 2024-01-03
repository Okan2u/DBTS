import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer


def calculate_score(df, column):
    scores = df[column].value_counts().to_dict()
    df[column + '_score'] = df[column].map(scores)
    df[column + '_score'] = df[column + '_score'] / df[column + '_score'].max()
    return df


def calculate_numeric_score(df, column):
    df[column + '_score'] = df[column] / df[column].max()
    return df


def impute_missing_values(df):
    numeric_columns = ['Gösterim Süresi', 'Sezon Sayısı', 'Bölüm Sayısı']
    imputer = SimpleImputer(strategy='mean')
    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
    return df


def calculate_yearly_comparison(df):
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


def fill_empty_success_scores(df):
    scores_columns = ['Format_score', 'Tür_score', 'Kanal_score', 'Yapım Şirketi_score',
                      'Gösterim Süresi_score', 'Sezon Sayısı_score', 'Bölüm Sayısı_score', 'Yearly_Success_Score']
    df['Overall_Success_Score'] = df[scores_columns].mean(axis=1)
    return df


def format_success_percentage(df):
    df[['Dizi Adı', 'Overall_Success_Score']] = df[['Dizi Adı', 'Overall_Success_Score']].astype(str)
    df['Overall_Success_Score'] = (df['Overall_Success_Score'].astype(float) * 200).round(2).astype(str) + '%'
    return df


def calculate_new_dizi_success_percentage(df, new_dizi):
    # Yeni dizi bilgilerini dataframe'e ekleme
    df = pd.concat([df, pd.DataFrame([new_dizi])], ignore_index=True)

    # Yeni dizi için başarı yüzdesini hesaplamak için aynı adımları takip et
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

    # Yeni dizi başarı yüzdesini döndür
    new_dizi_index = df[df['Dizi Adı'] == new_dizi['Dizi Adı']].index[0]
    success_percentage = df.loc[new_dizi_index, 'Overall_Success_Score']

    # Başarı yüzdesini duruma göre değerlendir
    success_percentage_value = float(success_percentage.strip('%'))
    if success_percentage_value <= 20:
        durum = "Birinci Sezonda yayından kaldırılacak (Başarısız)"
    elif success_percentage_value <= 40:
        durum = "Sadece iki sezon devam edecek (Kısmen Başarılı)"
    elif success_percentage_value <= 60:
        durum = "Üç sezon ile Beş sezon arasında sonlanacak (Başarılı)"
    elif success_percentage_value <= 80:
        durum = "Beş sezon ile On sezon arasında sonlanacak (Kısmen Olgun)"
    else:
        durum = "On sezon veya daha uzun devam edecek (Olgun)"

    return success_percentage, durum


def main():
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

    # Kullanıcıdan yeni dizi bilgilerini al
    new_dizi = {
        'Dizi Adı': input('Dizi Adı: '),
        'Format': input('Format: '),
        'Tür': input('Tür: '),
        'Kanal': input('Kanal: '),
        'Yapım Şirketi': input('Yapım Şirketi: '),
        'Gösterim Süresi': int(input('Gösterim Süresi(dakika): ')),
        'Sezon Sayısı': int(input('Sezon Sayısı(Tahmini): ')),
        'Bölüm Sayısı': int(input('Bölüm Sayısı(Tahmini): ')),
        'Yapım Yılı': int(input('Yapım Yılı: '))
    }

    _, durum = calculate_new_dizi_success_percentage(df, new_dizi)
    print(f"Dizi Durumu: {durum}")


if __name__ == "__main__":
    main()

