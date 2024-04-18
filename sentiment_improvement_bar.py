# create the bar chart for average sentiment improvement for customers on a given day
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

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

cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Transient)
@cursor.connect("add")
def on_add(sel):
    x, y, width, height = sel.artist[sel.index].get_bbox().bounds
    sel.annotation.get_bbox_patch().set(fc="white")
    sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=.8)
    sel.annotation.set(text=f"{round(height, 2)}",
                       position=(0, 20), anncoords="offset points")
    sel.annotation.xy = (x + width / 2, y + height)

plt.show()