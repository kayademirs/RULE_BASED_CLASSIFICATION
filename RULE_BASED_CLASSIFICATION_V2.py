import pandas as pd
###################################
# Custom function


def dataframe_summary(dataframe, head=5, tail=5):
    """
    This function summarizes the data frame (include info: shape, dtype, head, tail, missing values, quantile)

    Parameters
    ----------
    dataframe: Dataframe
        Any dataframe

    head: int (default 5)
        returns the first n rows

    tail: int (default 5)
        returns the last n rows


    Examples
    ---------
    import pandas as pd
    df = pd.read_csv(path)
    dataframe_summary(dataframe)

    """
    print("****************** SHAPE ******************")
    print(dataframe.shape)
    print("****************** DTYPES ******************")
    print(dataframe.dtypes)
    print("****************** HEAD ******************")
    print(dataframe.head(head))
    print("****************** TAIL ******************")
    print(dataframe.tail(tail))
    print("****************** MISSING VALUES ******************")
    print(dataframe.isnull().sum())
    print("****************** QUANTILES ******************")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


def load_persona():
    """
    This function returns the data frame

    Returns
    ----------
        dataframe

    Examples
    ---------
    df = read_dataset()
    """
    return pd.read_csv('datasets/persona.csv')


def join_columns(dataframe, columns, upper=True):
    """
    It combines the bras it receives as parameters for the data frame it receives as parameters.
    Parameters
    ----------
    dataframe: DataFrame
        A dataframe
    columns: list
        Contains columns to merge
    upper: boolean (default=True)
        Makes it uppercase

    Returns
    -------
        Returns a list

    """
    if upper:
        return ["_".join(value).upper() for value in dataframe[columns].values]
    else:
        return ["_".join(value) for value in dataframe[columns].values]


###################################
# GÖREV 1
# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = load_persona()
dataframe_summary(df)


# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
print("Unique Source:", len(pd.unique(df['SOURCE'])))
df['SOURCE'].value_counts()
# df["SOURCE"].nunique()


# Soru 3: Kaç unique PRICE vardır?
print("Unique Price: ", len(pd.unique(df['PRICE'])))


# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
print(df['PRICE'].value_counts())


# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
print(df['COUNTRY'].value_counts())


# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
print(df[["PRICE", "COUNTRY"]].groupby('COUNTRY').agg("sum"))
# df.groupby("COUNTRY").agg({"PRICE": "sum"})
# df.groupby("COUNTRY").PRICE.agg("sum")


# Soru 7: SOURCE türlerine göre satış sayıları nedir?
print(df['SOURCE'].value_counts())
# df.groupby("SOURCE").agg({"PRICE": "count"})
# df.groupby("SOURCE").PRICE.agg("count")


# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
print(df[["PRICE", "COUNTRY"]].groupby('COUNTRY').agg("mean"))


# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
print(df[["PRICE", "SOURCE"]].groupby('SOURCE').agg("mean"))


# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
print(df[["PRICE", "COUNTRY", "SOURCE"]].groupby(["COUNTRY", "SOURCE"]).agg("mean"))
# df.groupby(["SOURCE","COUNTRY"]).agg({"PRICE": "mean"})

###############################
# GÖREV 2
# COUNTRY, SOURCE, SEX, AGE kırılımında  toplam kazançlar nedir?
print(df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg("sum"))

###############################
# GÖREV 3
# Çıktıyı PRICE’a göre sıralayınız.
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan
# olacak şekilde PRICE’a göre uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).sum()\
    .sort_values(by=['PRICE'], ascending=False)
agg_df.head()

# agg_df = df.groupby(["SOURCE","COUNTRY","SEX","AGE"]).agg({"PRICE": "sum"}).sort_values(by= "PRICE",ascending=False)

##################################
# Görev 4
# Index’te yer alan isimleri değişken ismine çeviriniz.
# Üçüncü sorunun çıktısında yer alan price dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
agg_df.reset_index(inplace=True)
agg_df.head()
##################################
# Görev 5
# age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici şekilde oluşturunuz.
# Örneğin: '0_19', '20_24', '24_31', '31_41', '41_70'
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, 70],
                           labels=["0_18", "19_23", "24_30", "31_40", "41_70"])
agg_df.head()

##################################
# Görev 6
# Yeni seviye tabanlı müşterileri (persona) tanımlayınız
# ve veri setine değişken olarak ekleyiniz.
# Yeni eklenecek değişkenin adı: customers_level_based
# Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek
# customers_level_based değişkenini oluşturmanız gerekmektedir.

col = [i for i in agg_df.columns if i not in ["AGE", "PRICE"]]
agg_df["customers_level_based"] = join_columns(agg_df, col)

persona = agg_df.loc[:, ["PRICE", "customers_level_based"]].groupby("customers_level_based").mean()
persona.reset_index(inplace=True)

"""
cols = [i for i in agg_df.columns if i not in ["AGE", "PRICE"]]
agg_df["customers_level_based"] = ["_".join(i).upper() for i in agg_df[cols].values]
agg_df.head(1)

persona = agg_df[["customers_level_based", "PRICE"]]
persona.head(1)

persona = persona.groupby("customers_level_based").agg("mean").reset_index()
persona.head(1)
"""
##################################
# Görev 7
# Yeni müşterileri (personaları) segmentlere ayırınız.
# Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
# Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
# C segmentini analiz ediniz (Veri setinden sadece C segmentini çekip analiz ediniz).

persona["SEGMENT"] = pd.qcut(persona["PRICE"], 4, labels=["D", "C", "B", "A"])
persona.groupby(["SEGMENT"]).agg({"PRICE": ["max", "mean", "sum"]})

persona.groupby("SEGMENT").agg({"sum", "mean", "count", "median", "min", "max"})
segment_c = persona[persona["SEGMENT"] == 'C']
dataframe_summary(segment_c)
segment_c.describe()
##################################
# Görev 8
# Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve
# ne kadar gelir getirebileceğini tahmin ediniz.
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve
# ortalama ne kadar gelir kazandırması beklenir?
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne
# kadar gelir kazandırması beklenir?

users = ["TUR_ANDROID_FEMALE_31_40", "FRA_ANDROID_FEMALE_31_40"]
for user in users:
    print(persona[persona["customers_level_based"] == user].iloc[:, 1:])

