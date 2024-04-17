# create the bar chart for average sentiment improvement for customers on a given day
import pandas as pd
import matplotlib.pyplot as plt

improvement_data = pd.read_csv('satisfaction_data/improvement_rates.csv')
improvement_data['Improvement_Rate'] = improvement_data['Improvement_Rate']* 100
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
average_improvement_rate = improvement_data.groupby('Date')['Improvement_Rate'].mean()
print(average_improvement_rate)
average_improvement_rate.plot.bar(x=average_improvement_rate.index, y='Improvement_Rate', color='#c3a4cf')
plt.xlabel('Date')
plt.ylabel('Improvement Rate (%)')
plt.title('Average Customer Mood Improvement per Day')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()