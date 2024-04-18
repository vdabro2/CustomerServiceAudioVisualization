# Plots the sentiment avagrges per day 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

improvement_data = pd.read_csv('satisfaction_data/avg_sentiments.csv')
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
Negative_Customer = improvement_data.groupby('Date')['Negative_Customer'].mean()*100
Neutral_Customer = improvement_data.groupby('Date')['Neutral_Customer'].mean()*100
Positive_Customer = improvement_data.groupby('Date')['Positive_Customer'].mean()*100
Negative_Agent = improvement_data.groupby('Date')['Negative_Agent'].mean()*100
Neutral_Agent = improvement_data.groupby('Date')['Neutral_Agent'].mean()*100
Positive_Agent = improvement_data.groupby('Date')['Positive_Agent'].mean()*100
fig, ax = plt.subplots(figsize=(10, 6))


plt.xlabel('Date')
neg_customer, = plt.plot(Negative_Customer, label='Negative Customer', linestyle='dotted', marker='o', color='#bf2b23')
neu_customer, = plt.plot(Neutral_Customer, label='Neutral Customer', linestyle='dotted', marker='o', color='#c3a4cf')
pos_customer, = plt.plot(Positive_Customer, label='Positive Customer', linestyle='dotted', marker='o', color='#2f67b1')
neg_agent, = plt.plot(Negative_Agent, label='Negative Agent', linestyle='-', marker='o', color='#bf2b23')
neu_agent, = plt.plot(Neutral_Agent, label='Neutral Agent', linestyle='-', marker='o', color='#c3a4cf')
pos_agent, = plt.plot(Positive_Agent, label='Positive Agent', linestyle='-', marker='o', color='#2f67b1')


plt.ylabel('Percentage (%)')
plt.title('Average Sentiments per Day')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.legend(loc=2)

# Tooltips
annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind, data):
    x,y = data.get_data()
    annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
    text = "{}".format(str(round(y[ind["ind"][0]], 2)))
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
    cont, ind = neg_customer.contains(event)
    if cont:
        return (cont, ind, neg_customer)
    
    cont, ind = neu_customer.contains(event)
    if cont:
        return (cont, ind, neu_customer)
    
    cont, ind = pos_customer.contains(event)
    if cont:
        return (cont, ind, pos_customer)
    
    cont, ind = neg_agent.contains(event)
    if cont:
        return (cont, ind, neg_agent)
    
    cont, ind = neu_agent.contains(event)
    if cont:
        return (cont, ind, neu_agent)
    
    cont, ind = pos_agent.contains(event)
    if cont:
        return (cont, ind, pos_agent)
    
    else:
        return (False, None, None)

fig.canvas.mpl_connect("motion_notify_event", hover)

# Help Tooltip
help_axes = plt.axes([.5, .85, .1, .4])
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
        text = "This graph shows the average postive, \nnegative, and neutral sentiments per day of \nboth the customer and agent."
        help_annot.set_text(text)
        help_annot.get_bbox_patch().set_alpha(1)

        is_help_visible = True
        help_annot.set_visible(True)
        fig.canvas.draw_idle()

button_axes = plt.axes([0.66, 0.95, 0.03, 0.03])
bnext = Button(button_axes, '?',color="white")
bnext.on_clicked(toggle_help)

plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()