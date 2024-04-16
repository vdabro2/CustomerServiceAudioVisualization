# Plots the sentiment avagrges per day 
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

improvement_data = pd.read_csv('satisfaction_data/avg_sentiments.csv')
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
Negative_Customer = improvement_data.groupby('Date')['Negative_Customer'].mean()
Neutral_Customer = improvement_data.groupby('Date')['Neutral_Customer'].mean()
Positive_Customer = improvement_data.groupby('Date')['Positive_Customer'].mean()
Negative_Agent = improvement_data.groupby('Date')['Negative_Agent'].mean()
Neutral_Agent = improvement_data.groupby('Date')['Neutral_Agent'].mean()
Positive_Agent = improvement_data.groupby('Date')['Positive_Agent'].mean()
fig, ax = plt.subplots(figsize=(10, 6))


plt.xlabel('Date')
plt.plot(Negative_Customer, label='Negative Customer', linestyle='dotted', marker='o', color='#bf2b23')
plt.plot(Neutral_Customer, label='Neutral Customer', linestyle='dotted', marker='o', color='#c3a4cf')
plt.plot(Positive_Customer, label='Positive Customer', linestyle='dotted', marker='o', color='#2f67b1')
plt.plot(Negative_Agent, label='Negative Agent', linestyle='-', marker='o', color='#bf2b23')
plt.plot(Neutral_Agent, label='Neutral Agent', linestyle='-', marker='o', color='#c3a4cf')
plt.plot(Positive_Agent, label='Positive Agent', linestyle='-', marker='o', color='#2f67b1')


plt.ylabel('Percentage')
plt.title('Average Sentiments per Day')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.legend(loc=2)
# todo add tooltips

plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()