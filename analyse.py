import pandas as pd
import numpy as np


def get_min_rolls(df):
    df = df[df['Rarity'] >= 4]['Time'].value_counts().value_counts()
    print(df)


def get_servant_rarity(df):
    df = df[df['CardType'] == 'Servant']
    rarity = df['Rarity'].copy().value_counts()
    print(rarity)
    servant = df['ServantName'].copy().value_counts()
    print(servant)


def get_servant_class(df):
    df = df[df['CardType'] == 'Servant']
    Class = df['Class'].copy().value_counts()
    print(Class)


def get_roll_to_servant(df):
    df = df[(df['CardType'] == 'Servant') & (df['Rarity'] == 4) & (df['Avail'] == 'Story-locked')]
    print(df.index)
    return np.diff(df.index.insert(0, 0))


df1 = pd.read_csv("gacha_data/Account1/gachas.csv", index_col=False)
df2 = pd.read_csv("gacha_data/Account2/gachas.csv", index_col=False)
df3 = pd.read_csv("gacha_data/Account3/gachas.csv", index_col=False)
df4 = pd.read_csv("gacha_data/Account4/gachas.csv", index_col=False)
df5 = pd.read_csv("gacha_data/Account5/gachas.csv", index_col=False)
df6 = pd.read_csv("gacha_data/Account6/gachas.csv", index_col=False)

df = pd.concat([df1,df2,df3,df4,df5,df6], ignore_index=True)
print(df)
get_servant_class(df)
