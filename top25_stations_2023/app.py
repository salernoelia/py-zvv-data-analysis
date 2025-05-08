import pandas as pd
import matplotlib.pyplot as plt

df_main = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/REISENDE.csv", delimiter=";")

df_haltestellen = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/HALTESTELLEN.csv", delimiter=";")

merged_df = pd.merge(df_main, df_haltestellen, on="Haltestellen_Id")

grouped_df = merged_df.groupby('Haltestellenlangname').agg({'Einsteiger': 'sum', 'Aussteiger': 'sum'}).reset_index()

grouped_df['Total'] = grouped_df['Einsteiger'] + grouped_df['Aussteiger']

sorted_df = grouped_df.nlargest(25, 'Total')

plt.figure(figsize=(12, 6))

for i, row in sorted_df.iterrows():
    plt.barh(row['Haltestellenlangname'], row['Einsteiger'], label='Einsteiger', color='blue', alpha=0.5)
    plt.barh(row['Haltestellenlangname'], row['Aussteiger'], left=row['Einsteiger'], label='Aussteiger', color='orange', alpha=0.5)
    plt.annotate(f"{int(row['Total'])}", (row['Total'], row['Haltestellenlangname']), va='center')

plt.xlabel('Anzahl Passagiere')
plt.ylabel('Haltestellenlangname')
plt.title('Top 25 Haltestellen nach Anzahl Passagiere')
plt.legend(['Einsteiger', 'Aussteiger'])
plt.tight_layout()
plt.show()
