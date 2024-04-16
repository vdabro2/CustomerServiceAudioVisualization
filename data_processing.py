# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai
import requests
from time import sleep
import pandas as pd
API_key = "API_key"
aai.settings.api_key = API_key
#transcriber = aai.Transcriber()

#transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
#file = transcriber.transcribe("./customercall1.mp3")
#print(file.text)

headers = {
    'authorization': API_key, 
    'content-type': 'application/json',
}

endpoint = 'https://api.assemblyai.com/v2/upload'
file = 'audio_data/customercall9.mp3'
def read_file(file):
    with open(file, 'rb') as f:
        while True:
            data = f.read(5_242_880)
            if not data:
                break
            yield data
res_upload = requests.post(
    endpoint, 
    headers=headers, 
    data=read_file(file)
)

print(res_upload.json())

upload_url = res_upload.json().get('upload_url')
endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
    "audio_url": upload_url,
    "sentiment_analysis": True,
    "speaker_labels": True
}

headers = {
    "authorization": API_key,
    "content-type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)

response.json()

response_id = response.json()['id']

endpoint = f"https://api.assemblyai.com/v2/transcript/{response_id}"

headers = {
    "authorization": API_key,
}
response = requests.get(endpoint, headers=headers)

response.json()
current_status = "queued"
response_id = response.json()['id']
endpoint = f"https://api.assemblyai.com/v2/transcript/{response_id}"
headers = {
    "authorization": API_key,
}

while current_status not in ("completed", "error"):
    
    response = requests.get(endpoint, headers=headers)
    current_status = response.json()['status']
    
    if current_status in ("completed", "error"):
        print(response)
    else:
        sleep(10)
        
current_status
sent_data = []

for idx, sentence in enumerate(response.json()["sentiment_analysis_results"]):

    sent = sentence["text"]
    sentiment = sentence["sentiment"]
    duration = (sentence["end"] - sentence["start"]) / 1000
    speaker = sentence["speaker"]
    sent_data.append([idx +1 , sent, duration, speaker, sentiment])

sent_data = pd.DataFrame(sent_data, 
                         columns = ["SentenceID", "Text", "Duration", 
                                    "Speaker", "Sentiment"])

sent_data.to_csv('sentiment_data9.csv', index=False) 