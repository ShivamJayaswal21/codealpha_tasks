import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

df = pd.read_csv("Unemployment in India.csv")

print(df.head())
print(df.columns)

df.columns = df.columns.str.strip()
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'].str.strip(), dayfirst=True)

print(df['Date'].min(), df['Date'].max())

cutoff_date = pd.Timestamp('2020-03-01')
df['Period'] = df['Date'].apply(lambda x: 'Covid' if x >= cutoff_date else 'Pre-Covid')

print(df['Period'].value_counts())

plt.figure(figsize=(14, 7))
sns.lineplot(data=df, x='Date', y='Estimated Unemployment Rate (%)', hue='Area')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df,
    x='Period',
    y='Estimated Unemployment Rate (%)',
    order=['Pre-Covid', 'Covid'],
    ci=None
)
plt.show()

covid_df = df[df['Period'] == 'Covid']

top_states = (
    covid_df
    .groupby('Region')['Estimated Unemployment Rate (%)']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_states.values, y=top_states.index)
plt.show()

selected_columns = [
    'Estimated Unemployment Rate (%)',
    'Estimated Employed',
    'Estimated Labour Participation Rate (%)'
]

plt.figure(figsize=(8, 6))
sns.heatmap(df[selected_columns].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.show()

print("Unemployment increased sharply during Covid")
print("Urban areas were more affected than rural areas")
print("Some states faced very high unemployment during lockdown")
print("Labour participation rate shows negative correlation with unemployment")
