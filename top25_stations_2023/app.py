import pandas as pd
import matplotlib.pyplot as plt

# Read the main dataset
df_main = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/REISENDE.csv", delimiter=";")

# Read the Haltestellen dataset
df_haltestellen = pd.read_csv("../datasets/fahrgastzahlen_2023_ogd/HALTESTELLEN.csv", delimiter=";")

# Merge the two datasets on Haltestellen_Id
merged_df = pd.merge(df_main, df_haltestellen, on="Haltestellen_Id")

# Group by Haltestellenlangname and sum the Einsteiger and Aussteiger
grouped_df = merged_df.groupby('Haltestellenlangname').agg({'Einsteiger': 'sum', 'Aussteiger': 'sum'}).reset_index()

# Calculate total passengers
grouped_df['Total'] = grouped_df['Einsteiger'] + grouped_df['Aussteiger']

# Sort the DataFrame by total number of passengers and select top 25
sorted_df = grouped_df.nlargest(25, 'Total')

# Plot the top 25 most used Haltestellen
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
