import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import CheckButtons
import mplcursors

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

data = pd.read_csv('transcripts/sentiment_data' + data_to_use +'.csv')
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

    ###
    # going thru the sentence to parse each word 
    tokenized_sentence = nltk.word_tokenize(sentence)

    sid = SentimentIntensityAnalyzer()
    pos_word_list=[]
    neu_word_list=[]
    neg_word_list=[]

    # classifying each word as positive, neutral, negative (the neutral words are ignored)
    for word in tokenized_sentence:
        if (sid.polarity_scores(word)['compound']) >= 0.1:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.1:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)  

    word_list = []              

    if row['Sentiment'] == 'POSITIVE':
        #print('Positive:',pos_word_list)  
        word_list = pos_word_list
    elif row['Sentiment'] == 'NEGATIVE':        
        #print('Negative:',neg_word_list) 
        word_list = neg_word_list
    else:
        word_list = []

    def underline_words(sentence, words):
        underlined_sentence = sentence

        for word in words:
            start_index = underlined_sentence.find(word)
            
            if start_index != -1:
                first_char = word[0]  
                middle_chars = ''.join(['\u0332' + char for char in word[1:-1]])  
                last_char = '\u0332' + word[-1] if len(word) > 1 else ''  
                underlined_word = first_char + middle_chars + last_char
                
                underlined_sentence = underlined_sentence[:start_index] + underlined_word + underlined_sentence[start_index+len(word):]
        return underlined_sentence

    underlined_sentence = underline_words(sentence, word_list)

    if row['Speaker'] == 'A':
        line, = plt.plot([time/60, time/60], [-y, y], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=3, label= person + "\nSentiment: " +row['Sentiment']+ "\nTimestamp: " + str(float_to_timestamp(round(time/60, 2))) + "\n" + "Duration: " + str(seconds_to_timestamp(round(row['Duration'],2))) + "\n" + underlined_sentence)#label=row['Text'
    else:
        line, = plt.plot([time/60, time/60], [-y-8, y-8], color=color_mapping.get(row['Sentiment'], 'black'), linewidth=3, label= person + "\nSentiment: " +row['Sentiment']+ "\nTimestamp: " + str(float_to_timestamp(round(time/60, 2))) + "\n" + "Duration: " + str(seconds_to_timestamp(round(row['Duration'],2))) + "\n" + underlined_sentence)#label=row['Text'

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
