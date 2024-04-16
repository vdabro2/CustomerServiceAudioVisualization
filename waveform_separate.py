import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import CheckButtons
import mplcursors
# choose 1 - 9 
data_to_use = "2"
def seconds_to_timestamp(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    timestamp = ""
    if minutes > 0:
        timestamp += f"{minutes} min "
    if remaining_seconds > 0:
        timestamp += f"{remaining_seconds} sec"

    return timestamp.strip()
def float_to_timestamp(float_value):
    minutes = int(float_value)
    seconds = int((float_value - minutes) * 60)

    timestamp = ""
    if minutes > 0:
        timestamp += f"{minutes} min "
    if seconds > 0:
        timestamp += f"{seconds} sec"

    return timestamp.strip()

data = pd.read_csv('sentiment_data' + data_to_use +'.csv')
color_mapping = {'NEGATIVE': '#bf2b23', 'NEUTRAL': '#c3a4cf', 'POSITIVE': '#2f67b1'}

time = 0
# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
agent_lines = []
customer_lines = []
for index, row in data.iterrows():
    if row['Speaker'] == 'A':
        person = "Customer"
    else:
        person = "Agent"
    sentence = ''
    col = 1
    for c in row['Text']:
        sentence = sentence + c
        if col % 20 == 0:
            if c == ' ':
                sentence = sentence + '\n'
                col = 1
            else:
                col = 20
        else:
            col = col + 1
    #line, = plt.plot([time/60, time/60], [-row['Duration']/2, row['Duration']/2], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=max(1.5,3*(row['Duration']/(max(data['Duration'])))), label= person + "\nSentiment: " +row['Sentiment']+ "\nTimestamp: " + str(float_to_timestamp(round(time/60, 2))) + "\n" + "Duration: " + str(seconds_to_timestamp(round(row['Duration'],2))) + "\n" + sentence)#label=row['Text'
    y = row['Duration']/2
    if row['Speaker'] == 'A':
        line, = plt.plot([time/60, time/60], [-y, y], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=3, label= person + "\nSentiment: " +row['Sentiment']+ "\nTimestamp: " + str(float_to_timestamp(round(time/60, 2))) + "\n" + "Duration: " + str(seconds_to_timestamp(round(row['Duration'],2))) + "\n" + sentence )#label=row['Text'
    else:
        line, = plt.plot([time/60, time/60], [-y-8, y-8], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=3, label= person + "\nSentiment: " +row['Sentiment']+ "\nTimestamp: " + str(float_to_timestamp(round(time/60, 2))) + "\n" + "Duration: " + str(seconds_to_timestamp(round(row['Duration'],2))) + "\n" + sentence)#label=row['Text'

    time += row['Duration']
    if row['Speaker'] == 'A':
        customer_lines.append(line)
    else:
        agent_lines.append(line)

# tooltip 
cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Transient)
@cursor.connect("add")
def on_add(sel):
    sel.annotation.set_text(sel.artist.get_label())
    sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
    sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=1)

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
patches = [mpatches.Patch(color=color, label=sentiment) for sentiment, color in color_mapping.items()]
plt.legend(handles=patches)
plt.xticks(range(len(time)), time)
plt.xlabel('Timestamp (min)')
plt.ylabel('Duration')
plt.title('Audio Sentiment')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.tick_params(axis='y', colors='none')


plt.show()
