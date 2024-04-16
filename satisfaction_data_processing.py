# process all data and create a dataset for average satisfaction rates
import pandas as pd

satisfaction_data = pd.DataFrame()
for i in range(1,9):
    data = pd.read_csv('transcripts/sentiment_data' + str(i) +'.csv')
    total_time = sum(data['Duration'])
    current_time = 0
    before_average = 0
    after_average = 0
    # speaker A is the customer
    for index, row in data.iterrows():
        if row['Speaker'] == 'A':
            if current_time < (total_time/2):
                # before
                if row['Sentiment'] == "NEGATIVE":
                    before_average = before_average - row['Duration']
                elif row['Sentiment'] == "POSITIVE":
                    before_average = before_average + row['Duration']
            else:
                # after
                if row['Sentiment'] == "NEGATIVE":
                    after_average = after_average - row['Duration']
                elif row['Sentiment'] == "POSITIVE":
                    after_average = after_average + row['Duration']
            current_time = current_time + row['Duration']
    # New row data
    new_row = {'Number': i, 'Begining_Sentiment': before_average, 'After_Sentiment': after_average}

    # Inserting the new row into the DataFrame
    satisfaction_data = satisfaction_data._append(new_row, ignore_index=True)
print(satisfaction_data)
satisfaction_data.to_csv('satisfaction_data/all.csv')

