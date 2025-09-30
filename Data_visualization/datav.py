import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

train_data = pd.read_csv('../mitsui-commodity-prediction-challenge/train.csv')
test_data = pd.read_csv('../mitsui-commodity-prediction-challenge/test.csv')
pairs = pd.read_csv('../mitsui-commodity-prediction-challenge/target_pairs.csv')
labels = pd.read_csv('../mitsui-commodity-prediction-challenge/train_labels.csv')

train_names = list(train_data.columns)

train_names = [name.replace("open_interest", "open interest")
                    .replace("settlement_price", "settlement price")
                    .replace("US_Stock", "US Stock")
                    .replace("adj_", "adjusted ")
               for name in train_names]

train_names = [re.split("_", name) for name in train_names]

for col in train_names:
    print(col)

columnid = list(range(1,len(train_names)+1))
column = list(train_data.columns)
category = [x[0] if len(x) > 0 else "" for x in train_names]

Ticker = [
    "_".join(x[1:len(x)-1]) if len(x) > 2 else "" 
    for x in train_names
]
Type = [x[-1] if len(x) > 0 else "" for x in train_names]

train_info = pd.DataFrame({
    "Column_Id": columnid,
    "Column": column,
    "Category": category,
    "Ticker": Ticker,
    "Type": Type
})

train_info["Ticker"] = train_info.apply(
    lambda row: row["Type"] if row["Ticker"] == "" else row["Ticker"], axis=1

)

print(train_info)

subset = train_info.iloc[1:,:]

summary = (
    subset.groupby("Category")
    .agg(
        column_count = ("Column", "count"),
        ticker_count = ("Ticker", lambda x: x.nunique())
        ).reset_index()
)

print(summary)

lme_info = train_info[train_info["Category"] == "LME"]
lme_info

lme_long = train_data.iloc[:,:5]
lme_long.columns = ["date_id", "Alminium", "Copper", "Lead", "Zinc"]
lme_long = lme_long.melt(
    id_vars="date_id",
    var_name = "Metal",
    value_name = "Price"
)

plt.figure(figsize=(16,6))
for metal in lme_long["Metal"].unique():
    metal_data = lme_long[lme_long["Metal"] == metal]
    plt.plot(metal_data["date_id"], metal_data["Price"], label =metal)

plt.xlabel("Data(data_id)")
plt.ylabel("Price")
plt.title("Lme : closing price of metal")
plt.legend(title = "Metal")
plt.grid()
plt.show()

jpx_info = train_info[ (train_info["Category"] == "JPX") & (train_info["Type"] == "Close")]
jpx_info

jpx_iinfo = jpx_info[jpx_info["Type"] == "Close"]

colums =[0] + jpx_iinfo["Column_Id"].tolist()
jpx_long = train_data.iloc[:,colums].copy()

jpx_long.columns = [ "date_id", "Gold Mini", "Gold Rolling Spot", "Gold Standard",
    "Platinum Mini", "Platinum Standard", "RSS3 Rubber"]

jpx_long = jpx_long.melt(
    id_vars= "date_id",
    value_name="Price",
    var_name="Futures"
)

futures_list = jpx_long["Futures"].unique()
ncol = 3 
nrow = (len(futures_list)+ ncol -1) //ncol

fig , axs = plt.subplots(nrow , ncol, figsize= (16,6),sharex = True , sharey = True )
axs = axs.flatten()

for i,future in enumerate(futures_list):
    df = jpx_long[jpx_long["Futures"] == future]
    axs[i].plot(df["date_id"], df["Price"] , color = "tab:blue")
    axs[i].set_title(future)
    axs[i].grid()

for j in range(i + 1, len(axs)):
    fig.delaxes(axs[j])


fig.suptitle("Japani", fontsize=14)
fig.text(0.5, 0.04, "Date (date_id)", ha='center')
fig.text(0.04, 0.5, "Price", va='center', rotation='vertical')
plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])
plt.show()

us_info = train_info[(train_info["Category"] == "US Stock") & (train_info["Type"] == "adjusted close")]
us_tkr = us_info["Ticker"].tolist()

colums =[0] + jpx_iinfo["Column_Id"].tolist()
jpx_long = train_data.iloc[:,colums].copy()

jpx_long.columns = [ "date_id", "Gold Mini", "Gold Rolling Spot", "Gold Standard",
    "Platinum Mini", "Platinum Standard", "RSS3 Rubber"]

jpx_long = jpx_long.melt(
    id_vars= "date_id",
    value_name="Futures",
    var_name="Price"
)

futures_list = jpx_long["Futures"].unique()
ncol = 3 
nrow = (len(futures_list)+ ncol -1) //ncol

fig , axs = plt.subplots(nrow , ncol, figsize= (16,6),sharex = True , sharey = True )
axs = axs.flatten()

for i,future in enumerate(futures_list):
    df = jpx_long[jpx_long["Futures"] == future]
    axs[i].plot(df["date_id"], df["Price"] , color = "tab:blue")
    axs[i].set_title(future)
    axs[i].grid()

for j in range(i + 1, len(axs)):
    fig.delaxes(axs[j])


fig.suptitle("Japani", fontsize=14)
fig.text(0.5, 0.04, "Date (date_id)", ha='center')
fig.text(0.04, 0.5, "Price", va='center', rotation='vertical')
plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])
plt.show()
