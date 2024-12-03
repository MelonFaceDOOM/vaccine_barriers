import pandas as pd

df1 = pd.read_csv("multilabel.csv")
df2 = pd.read_csv("multilabel2.csv")
df2.update(df1.set_index('id'), overwrite=True)
df2.to_csv('multilabel3.csv', index=False, encoding="utf-8")