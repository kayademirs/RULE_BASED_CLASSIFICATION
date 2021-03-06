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
# G??REV 1
# Soru 1: persona.csv dosyas??n?? okutunuz ve veri seti ile ilgili genel bilgileri g??steriniz.
df = load_persona()
dataframe_summary(df)


# Soru 2: Ka?? unique SOURCE vard??r? Frekanslar?? nedir?
print("Unique Source:", len(pd.unique(df['SOURCE'])))
df['SOURCE'].value_counts()
# df["SOURCE"].nunique()


# Soru 3: Ka?? unique PRICE vard??r?
print("Unique Price: ", len(pd.unique(df['PRICE'])))


# Soru 4: Hangi PRICE'dan ka??ar tane sat???? ger??ekle??mi???
print(df['PRICE'].value_counts())


# Soru 5: Hangi ??lkeden ka??ar tane sat???? olmu???
print(df['COUNTRY'].value_counts())


# Soru 6: ??lkelere g??re sat????lardan toplam ne kadar kazan??lm?????
print(df[["PRICE", "COUNTRY"]].groupby('COUNTRY').agg("sum"))
# df.groupby("COUNTRY").agg({"PRICE": "sum"})
# df.groupby("COUNTRY").PRICE.agg("sum")


# Soru 7: SOURCE t??rlerine g??re sat???? say??lar?? nedir?
print(df['SOURCE'].value_counts())
# df.groupby("SOURCE").agg({"PRICE": "count"})
# df.groupby("SOURCE").PRICE.agg("count")


# Soru 8: ??lkelere g??re PRICE ortalamalar?? nedir?
print(df[["PRICE", "COUNTRY"]].groupby('COUNTRY').agg("mean"))


# Soru 9: SOURCE'lara g??re PRICE ortalamalar?? nedir?
print(df[["PRICE", "SOURCE"]].groupby('SOURCE').agg("mean"))


# Soru 10: COUNTRY-SOURCE k??r??l??m??nda PRICE ortalamalar?? nedir?
print(df[["PRICE", "COUNTRY", "SOURCE"]].groupby(["COUNTRY", "SOURCE"]).agg("mean"))
# df.groupby(["SOURCE","COUNTRY"]).agg({"PRICE": "mean"})

###############################
# G??REV 2
# COUNTRY, SOURCE, SEX, AGE k??r??l??m??nda  toplam kazan??lar nedir?
print(df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg("sum"))

###############################
# G??REV 3
# ????kt??y?? PRICE???a g??re s??ralay??n??z.
# ??nceki sorudaki ????kt??y?? daha iyi g??rebilmek i??in sort_values metodunu azalan
# olacak ??ekilde PRICE???a g??re uygulay??n??z.
# ????kt??y?? agg_df olarak kaydediniz.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).sum()\
    .sort_values(by=['PRICE'], ascending=False)
agg_df.head()

# agg_df = df.groupby(["SOURCE","COUNTRY","SEX","AGE"]).agg({"PRICE": "sum"}).sort_values(by= "PRICE",ascending=False)

##################################
# G??rev 4
# Index???te yer alan isimleri de??i??ken ismine ??eviriniz.
# ??????nc?? sorunun ????kt??s??nda yer alan price d??????ndaki t??m de??i??kenler index isimleridir.
# Bu isimleri de??i??ken isimlerine ??eviriniz.
agg_df.reset_index(inplace=True)
agg_df.head()
##################################
# G??rev 5
# age de??i??kenini kategorik de??i??kene ??eviriniz ve agg_df???e ekleyiniz.
# Age say??sal de??i??kenini kategorik de??i??kene ??eviriniz.
# Aral??klar?? ikna edici ??ekilde olu??turunuz.
# ??rne??in: '0_19', '20_24', '24_31', '31_41', '41_70'
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, 70],
                           labels=["0_18", "19_23", "24_30", "31_40", "41_70"])
agg_df.head()

##################################
# G??rev 6
# Yeni seviye tabanl?? m????terileri (persona) tan??mlay??n??z
# ve veri setine de??i??ken olarak ekleyiniz.
# Yeni eklenecek de??i??kenin ad??: customers_level_based
# ??nceki soruda elde edece??iniz ????kt??daki g??zlemleri bir araya getirerek
# customers_level_based de??i??kenini olu??turman??z gerekmektedir.

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
# G??rev 7
# Yeni m????terileri (personalar??) segmentlere ay??r??n??z.
# Yeni m????terileri (??rnek: USA_ANDROID_MALE_0_18) PRICE???a g??re 4 segmente ay??r??n??z.
# Segmentleri SEGMENT isimlendirmesi ile de??i??ken olarak agg_df???e ekleyiniz.
# Segmentleri betimleyiniz (Segmentlere g??re group by yap??p price mean, max, sum???lar??n?? al??n??z).
# C segmentini analiz ediniz (Veri setinden sadece C segmentini ??ekip analiz ediniz).

persona["SEGMENT"] = pd.qcut(persona["PRICE"], 4, labels=["D", "C", "B", "A"])
persona.groupby(["SEGMENT"]).agg({"PRICE": ["max", "mean", "sum"]})

persona.groupby("SEGMENT").agg({"sum", "mean", "count", "median", "min", "max"})
segment_c = persona[persona["SEGMENT"] == 'C']
dataframe_summary(segment_c)
segment_c.describe()
##################################
# G??rev 8
# Yeni gelen m????terileri segmentlerine g??re s??n??fland??r??n??z ve
# ne kadar gelir getirebilece??ini tahmin ediniz.
# 33 ya????nda ANDROID kullanan bir T??rk kad??n?? hangi segmente aittir ve
# ortalama ne kadar gelir kazand??rmas?? beklenir?
# 35 ya????nda IOS kullanan bir Frans??z kad??n?? hangi segmente ve ortalama ne
# kadar gelir kazand??rmas?? beklenir?

users = ["TUR_ANDROID_FEMALE_31_40", "FRA_ANDROID_FEMALE_31_40"]
for user in users:
    print(persona[persona["customers_level_based"] == user].iloc[:, 1:])

