# create the bar chart for average sentiment improvement for customers on a given day
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

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
plt.grid(True)

plotted_points = []

for xe, ye in zip(dates, y):
    for each_y in ye:
        if np.mean(each_y) > 50:
            point = plt.scatter([xe], each_y, color='#2f67b1', s=60)
            plotted_points.append(point)
        elif np.mean(each_y) < 0:
            point = plt.scatter([xe], each_y, color='#bf2b23', s=60)
            plotted_points.append(point)
        else:
            point = plt.scatter([xe], each_y, color='#c3a4cf', s=60)
            plotted_points.append(point)


plt.xlabel('Date')
plt.ylabel('Improvement Rate (%)')
plt.title('Customer Mood Improvement per Day')
plt.xticks(rotation=45)  

# Tooltip
annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind, data):
    pos = data.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}".format(round(pos[1], 2))
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind, data = find_data_point(event)

        if cont:
            update_annot(ind, data)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

def find_data_point(event):
    for point in plotted_points:
        cont, ind = point.contains(event)
        if cont:
            return (cont, ind, point)
    
    return (False, None, None)

fig.canvas.mpl_connect("motion_notify_event", hover)

# Help Tooltip
help_axes = plt.axes([.5, .8, .1, .4])
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
        text = "This graph shows the change in customer sentiment \nfor each call in a day. \nA blue point indicates a drastic mood increase, a \nred point indicates a drastic mood decrease, and \na purple point indicates some mood increase/decrease."
        help_annot.set_text(text)
        help_annot.get_bbox_patch().set_alpha(1)

        is_help_visible = True
        help_annot.set_visible(True)
        fig.canvas.draw_idle()

button_axes = plt.axes([0.7, 0.95, 0.03, 0.03])
bnext = Button(button_axes, '?',color="white")
bnext.on_clicked(toggle_help)

plt.tight_layout()  
plt.show()