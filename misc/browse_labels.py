# check how many rows are in mutlilabel.csv
import pandas as pd


label_negative_true = """
n3zsgk
np015g
kpnqqj
mdrr3c
nexcmn
kzyrjk
lg3y3y
n84gv6
ks8jj8
nachjn
mrzxct
mvrxxh
mupkqj
ouebj6
mppgv8
mth3sd
l6eiuc
pezdbw
nizago
twqi0q
"""

mandate_negative_true = """
rzkeig
r66cuk
nvvvuy
s39gay
ncjc21
spfivn
"""

df = pd.read_csv("multilabel.csv")

turn_n_to_true = mandate_negative_true.strip().split("\n")
for i in turn_n_to_true:
    if i not in df['id'].tolist():
        raise ValueError(f"{i} doesn't exist in data")
    else:
        df.loc[df['id']==i, 'Negative']=True
turn_n_to_true = label_negative_true.strip().split("\n")
for i in turn_n_to_true:
    if i not in df['id'].tolist():
        raise ValueError(f"{i} doesn't exist in data")
    else:
        df.loc[df['id']==i, 'Negative']=True


df.loc[df['id']=="pu59ni", "Mandates"]=False 
df.loc[df['id']=="pl8yosm", "Logistics"]=False 
df.loc[df['id']=="p06nv2", "Mandates"]=False 

df = df[df['Mandates']==True]
nt = df[df['Negative']==True]
nf = df[df['Negative']==False]
print("MANDATES WHERE NEGATIVE TRUE")
for idx, row in nt.iterrows():
    print(row['id'], row['title'])
print("MANDATES WHERE NEGATIVE FALSE")
for idx, row in nf.iterrows():
    print(row['id'], row['title'])

nh = df[df['Highlight Problem']==True]
print("MANDATES WHERE HIGHLIGHTED")
for idx, row in nh.iterrows():
    print(row['id'], row['title'])

df.to_csv("multilabel_fixed.csv", index=False)
df2 = pd.read_csv("multilabel_fixed.csv")
