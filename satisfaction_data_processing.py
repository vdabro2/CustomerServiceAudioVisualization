# todo: process all data and create a dataset for average satisfaction rates
import pandas as pd
for i in range(1,9):
    data = pd.read_csv('transcripts/sentiment_data' + str(i) +'.csv')
    
