# Adım 1: Veri Okuma ve Eksik Değerleri Doldurma

import pandas as pd
from sklearn.impute import SimpleImputer

def impute_missing_values(df):
    # Sayısal sütunları doldur
    numeric_columns = ['Gösterim Süresi', 'Sezon Sayısı', 'Bölüm Sayısı']
    imputer = SimpleImputer(strategy='mean')

    for column in numeric_columns:
        if column not in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')

    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
    return df

def main():
    df = pd.read_excel('turk_dizileri.xlsx')
    df = impute_missing_values(df)
