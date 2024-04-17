# create the bar chart for average sentiment improvement for customers on a given day
import pandas as pd
import matplotlib.pyplot as plt

improvement_data = pd.read_csv('satisfaction_data/improvement_rates.csv')
improvement_data['Improvement_Rate'] = improvement_data['Improvement_Rate']* 100
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
y = [[],[],[],[],[],[]]
for i, row in improvement_data.iterrows():
    if row['Date'] == '2024-04-04':
        y[0].append(row['Improvement_Rate'])
    if row['Date'] == '2024-04-05':
        y[1].append(row['Improvement_Rate'])
    if row['Date'] == '2024-04-06':
        y[2].append(row['Improvement_Rate'])
    if row['Date'] == '2024-04-07':
        y[3].append(row['Improvement_Rate'])
    if row['Date'] == '2024-04-08':
        y[4].append(row['Improvement_Rate'])
    if row['Date'] == '2024-04-09':
        y[5].append(row['Improvement_Rate'])
fig, ax = plt.subplots(figsize=(10, 6))
bplot = ax.boxplot(y,
        vert=True,  # vertical box alignment
        patch_artist=True,  # fill with color
        labels=dates,
        )  # will be used to label x-ticks
print(bplot['boxes'])
for patch, color in zip(bplot['means'], ['pink']):
    print(patch)

    patch.set_facecolor(color)
    
plt.xlabel('Date')
plt.ylabel('Improvement Rate (%)')
plt.title('Average Customer Mood Improvement per Day')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()