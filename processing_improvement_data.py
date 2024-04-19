# process all data and create a dataset for average satisfaction rates
import pandas as pd

satisfaction_data = pd.DataFrame()
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
for i in range(0,15):
    data = pd.read_csv('transcripts/sentiment_data' + str(i+1) +'.csv')
    total_time = sum(data['Duration'])
    current_time = 0
    before_average = 0.0
    after_average = 0.0
    
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
    
    if after_average > before_average:
        # the customers mood improved
        improvement_rate =  abs((after_average - before_average) / before_average)
    else: 
        improvement_rate = (-1.00) * abs((after_average - before_average) / before_average)
        if abs((after_average - before_average) / before_average) > 2:
            improvement_rate = -2.0
    new_row = {'Number': i+1, "Date": dates[i], 'Begining_Sentiment': before_average, 'After_Sentiment': after_average, 'Improvement_Rate': improvement_rate}

    # Inserting the new row into the DataFrame
    satisfaction_data = satisfaction_data._append(new_row, ignore_index=True)
print(satisfaction_data)
satisfaction_data.to_csv('satisfaction_data/improvement_rates.csv')

