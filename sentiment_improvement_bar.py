# create the bar chart for average sentiment improvement for customers on a given day
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import Button

improvement_data = pd.read_csv('satisfaction_data/improvement_rates.csv')
improvement_data['Improvement_Rate'] = improvement_data['Improvement_Rate']* 100
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
average_improvement_rate = improvement_data.groupby('Date')['Improvement_Rate'].mean()
print(average_improvement_rate)
fig, ax = plt.subplots(figsize=(8, 6))
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
    sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
    sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=.8)
    sel.annotation.set(text=f"{round(height, 2)}",
                       position=(0, 20), anncoords="offset points")
    sel.annotation.xy = (x + width / 2, y + height)

# Help Tooltip
help_axes = plt.axes([.45, .78, .1, .1])
help_axes.set_axis_off()
help_annot = help_axes.annotate("", xy=(0,0),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"))
is_help_visible = False
def toggle_help(val):
    global is_help_visible
    if is_help_visible:
        is_help_visible = False
        help_annot.set_visible(False)
        fig.canvas.draw_idle()
    else:
        help_annot.xy = ([0,0])
        text = "This graph shows the average percent customer \nsentiment improvement rate, comparing \nthe difference between a customer's sentiment at the \nbeginning and end of a call. The percent increase \nfor each call's customer sentiment is calculated, and \naveraged with the other calls for the day."
        help_annot.set_text(text)
        help_annot.get_bbox_patch().set_alpha(1)

        is_help_visible = True
        help_annot.set_visible(True)
        fig.canvas.draw_idle()

button_axes = plt.axes([0.81, 0.95, 0.03, 0.03])
bnext = Button(button_axes, '?',color="white")
bnext.on_clicked(toggle_help)

plt.show()