import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import CheckButtons
import mplcursors
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

data = pd.read_csv('sentiment_data.csv')
color_mapping = {'NEGATIVE': 'red', 'NEUTRAL': 'blue', 'POSITIVE': 'green'}
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
    line, = plt.plot([time/60, time/60], [-row['Duration']/2, row['Duration']/2], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=3, label= person + "\nSentiment: " +row['Sentiment']+ "\nTimestamp: " + str(float_to_timestamp(round(time/60, 2))) + "\n" + "Duration: " + str(seconds_to_timestamp(round(row['Duration'],2))) + "\n" + sentence)#label=row['Text'
    time += row['Duration']
    if row['Speaker'] == 'A':
        customer_lines.append(line)
    else:
        agent_lines.append(line)

# tooltip 
cursor = mplcursors.cursor(hover=True)
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
