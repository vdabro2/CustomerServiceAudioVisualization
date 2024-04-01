import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import CheckButtons
import mplcursors


data = pd.read_csv('sentiment_data.csv')
color_mapping = {'NEGATIVE': 'red', 'NEUTRAL': 'blue', 'POSITIVE': 'green'}
time = 0
# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
agent_lines = []
customer_lines = []
for index, row in data.iterrows():
    line, = plt.plot([time/60, time/60], [-row['Duration']/2, row['Duration']/2], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=3, label=row['Text'])
    time += row['Duration']
    if row['Speaker'] == 'A':
        customer_lines.append(line)
    else:
        agent_lines.append(line)

# tooltip 
# cursor = mplcursors.cursor(hover=True)
# @cursor.connect("add")
#def on_add(sel):
    #x, y, width, height = sel.artist[sel.index].get_bbox().bounds
    #sel.annotation.set_text(sel.artist.get_label())
    #sel.annotation.get_bbox_patch().set(fc="white")
    #sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=.5)

# tick calculations
time =[]
totoal = 0
for t in data['Duration']:
    totoal = totoal + t
totoal = totoal / 60
i = 0
while i < totoal:
    time.append(i)
    i = i +1
frame1 = plt.gca()
frame1.axes.get_yaxis().set_visible(False)
patches = [mpatches.Patch(color=color, label=sentiment) for sentiment, color in color_mapping.items()]
plt.legend(handles=patches)
plt.xticks(range(len(time)), time)
plt.xlabel('Timestamp (min)')
plt.ylabel('Duration')
plt.title('Audio Sentiment')

axCheck = plt.axes([0.01, 0.02, 0.15, 0.1])
check = CheckButtons(axCheck, ['Customer', 'Agent'], [True, True])

# Function to handle checkbox changes
def func(label):
    if label == 'Customer':
        for line in customer_lines:
            if line.get_visible():
                line.set_visible(False)
            else:
                line.set_visible(True)
    elif label == 'Agent':
        for line in agent_lines:
            if line.get_visible():
                line.set_visible(False)
            else:
                line.set_visible(True)
    plt.draw()

check.on_clicked(func)


plt.show()