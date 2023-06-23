import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

# import
df = pd.read_csv('/home/peitscha/PycharmProjects/LidlCandyCase/candy-data.csv', index_col=0)
df = df.sort_values("winpercent", ascending=False)

# Analyse der Daten
df.describe()  # winpercent mean 50, std 14


''' *** Most popular candy in different categories *** '''

# Total count
df1 = df.loc[:, 'chocolate':'pluribus'].apply(pd.Series.value_counts).fillna(0).transpose()[1]\
    .sort_values(ascending=False)

df1 = df1.to_frame()
df1.columns = ['Count']

# Count of most popular products
df2 = df[df['winpercent'] > 50].loc[:, 'chocolate':'pluribus'].apply(pd.Series.value_counts).fillna(0)\
    .transpose()[1].sort_values(ascending=False)

df3 = df[df['winpercent'] > 60].loc[:, 'chocolate':'pluribus'].apply(pd.Series.value_counts).fillna(0)\
    .transpose()[1].sort_values(ascending=False)

df4 = df[df['winpercent'] > 70].loc[:, 'chocolate':'pluribus'].apply(pd.Series.value_counts).fillna(0)\
    .transpose()[1].sort_values(ascending=False)

# Merging of tables
df5 = pd.merge(df2, df3, left_index=True, right_index=True)
df5 = pd.merge(df5, df4, left_index=True, right_index=True)
df5.columns = ["Popularity > 50%", "Popularity > 60%", "Popularity > 70%"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5))

sns.barplot(df1, x=df1.index, y='Count', color='#f6bc00', ax=ax1)
sns.barplot(df5, x=df5.index, y='Popularity > 50%', ax=ax2, color='#0a14d6', label='Popularity > 50%')
sns.barplot(df5, x=df5.index, y='Popularity > 60%', ax=ax2, color='#0000a0', label='Popularity > 60%')
sns.barplot(df5, x=df5.index, y='Popularity > 70%', ax=ax2, color='#000033', label='Popularity > 70%')

ax1.set_title("Total Count")
ax1.set_xlabel("Categories")
ax1.set_ylabel("Count")

ax2.set_title("Count of Most Popular")
ax2.legend()
ax2.set_xlabel("Categories")
ax2.set_ylabel("Count")

fig.tight_layout()
fig.show()


''' *** Correlation of Popularity with Sugar and Price *** '''

# Comparison of means and correlation values

d1 = {'Sugarpercent': [df['sugarpercent'].corr(df['winpercent'])],
      'Pricepercent': [df['pricepercent'].corr(df['winpercent'])]}
d2 = {'Total':  [df.head(10)['sugarpercent'].mean()], 'Top 10': [df['sugarpercent'].mean()]}
d3 = {'Total': [df.head(10)['pricepercent'].mean()], 'Top 10': [df['pricepercent'].mean()]}

df1 = pd.DataFrame(data=d1)
df2 = pd.DataFrame(data=d2)
df3 = pd.DataFrame(data=d3)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

sns.barplot(df1, ax=ax1, color="#f6bc00")
sns.barplot(df2, ax=ax2, color="#0000a0")
sns.barplot(df3, ax=ax3, color="#000073")

ax1.set_title("Correlation Between Winpercent and Sugar/ Price")
ax2.set_title("Pricepercent in Total Dataset vs Top 10")
ax3.set_title("Sugarpercent in Total Dataset vs Top 10")

fig.show()

# Correlation graphs


def roundup_to_10s(series):
    list = []
    for x in series:
        list.append(int(np.ceil(x / 10.0)) * 10)
    return list


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

sns.stripplot(x=roundup_to_10s(df['winpercent']), y=df['sugarpercent'].round(1), ax=ax1, color="#0a08b3")
sns.stripplot(x=roundup_to_10s(df['winpercent']), y=df['pricepercent'].round(1), ax=ax2, color="#f6bc00")

ax1.set(xlabel='Popularity', ylabel='Sugar Percentage')
ax2.set(xlabel='Popularity', ylabel='Price Percentage')

ax1.set_title("Correlation between Popularity and Sugar Percentage")
ax2.set_title("Correlation between Popularity and Price Percentage")

fig.show()


''' *** Most popular combinations of categories *** '''


def count_category_combinations(dfx):
    dfy = pd.DataFrame(0, index=range(dfx.shape[1]), columns=range(dfx.shape[1]))
    dfy.columns = dfx.columns
    dfy.index = dfx.columns

    x = 0
    y = 0
    for i in range(dfx.shape[1]):
        for j in range(dfx.shape[1]):
            for k in range(dfx.shape[0]):
                if dfx.iloc[k, i] == 1 & dfx.iloc[k, j] == 1:
                    dfy.iloc[x, y] += 1
            y += 1
        y = 0
        x += 1
    return dfy


df2 = df[df['winpercent'] > 70].loc[:, 'chocolate':'pluribus']
df3 = count_category_combinations(df.loc[:, 'chocolate':'pluribus'])
df4 = count_category_combinations(df2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

sns.heatmap(df3, ax=ax1, cmap="mako")
sns.heatmap(df4, ax=ax2, cmap="mako")

ax1.set_title("Total Number of Combinations")
ax2.set_title("Number of Combinations with over 70% Popularity")

fig.subplots_adjust(bottom=0.3, right=1)
fig.text(in_layout=True)
fig.tight_layout()

fig.show()
