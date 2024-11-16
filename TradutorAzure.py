import requests, json, uuid
from docx import Document 
import os
from dotenv import load_dotenv

load_dotenv()

subscription_key = os.getenv("AZURE_TRANSLATOR_KEY")
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = os.getenv("AZURE_REGION", "MINHA_REGIAO")
language_destination = 'pt-br'
def translator_text(text, language_destination):
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': language_destination 
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)

    if response.status_code == 200:
        response = response.json()
        if response and isinstance(response, list) and len(response) > 0 and \
           'translations' in response[0] and len(response[0]['translations']) > 0 and \
           'text' in response[0]['translations'][0]:
            return response[0]['translations'][0]['text']
        else:
            print("Error: Unexpected response format:", response)
            return None
    else:
        print("Error: API request failed with status code:", response.status_code)
        print("Error response:", response.text)
        return None



 