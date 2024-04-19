# process all data and create a dataset for average customer sentiments per day
import pandas as pd

satisfaction_data = pd.DataFrame()
dates = ['2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09', '2024-04-04', '2024-04-05', '2024-04-06', '2024-04-07', '2024-04-08', '2024-04-09']
for i in range(0,15):
    data = pd.read_csv('transcripts/sentiment_data' + str(i+1) +'.csv')
    customer_pos = 0
    customer_neg = 0
    customer_neu = 0

    agent_pos = 0
    agent_neg = 0
    agent_neu = 0
    
    for index, row in data.iterrows():
        # speaker A is the customer
        if row['Speaker'] == 'A':
            if row['Sentiment'] == 'NEGATIVE':
                customer_neg = customer_neg + row['Duration']
            if row['Sentiment'] == 'POSITIVE':
                customer_pos = customer_pos + row['Duration']
            if row['Sentiment'] == 'NEUTRAL':
                customer_neu = customer_neu + row['Duration']
        else:
            if row['Sentiment'] == 'NEGATIVE':
                agent_neg = agent_neg + row['Duration']
            if row['Sentiment'] == 'POSITIVE':
                agent_pos = agent_pos + row['Duration']
            if row['Sentiment'] == 'NEUTRAL':
                agent_neu = agent_neu + row['Duration']

    total_cus = customer_neg + customer_neu + customer_pos
    total_agent = agent_neg + agent_neu + agent_pos
    new_row = {'Number': i+1, "Date": dates[i], 
               'Negative_Customer': customer_neg/total_cus, 
               'Neutral_Customer' : customer_neu/total_cus, 
               'Positive_Customer': customer_pos/total_cus,
               'Negative_Agent' : agent_neg/total_agent,
               'Neutral_Agent': agent_neu/total_agent,
               'Positive_Agent': agent_pos/total_agent}

    # Inserting the new row into the DataFrame
    satisfaction_data = satisfaction_data._append(new_row, ignore_index=True)
print(satisfaction_data)
satisfaction_data.to_csv('satisfaction_data/avg_sentiments.csv')

