import requests
import json

def baichuan_call(messages):
    url = "https://api.baichuan-ai.com/v1/chat/completions"
    api_key = "your_api_key"

    data = {
        "model": "Baichuan2-Turbo",
        "messages": messages,
        "stream": True
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    stream = requests.post(url, data=json_data, headers=headers, timeout=60)
    text = ''
    for chunk in stream:
        print(chunk)
    if len(text) > 0:
        return text
    return 'ERROR'
