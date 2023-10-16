# Import the necessary modules
from google.cloud import texttospeech
import json
import requests

# Set up the credentials for the Google Cloud service
client = texttospeech.TextToSpeechClient.from_service_account_json('your service account.json')

# Define the Google Cloud function URL and JSON data
url = 'replace with your cloud function'
data = {'name': 'test'} # Replace this with your own JSON data

# Send the push request with JSON data to the Cloud function and retrieve the response
response = requests.post(url, json=data)
response_data = response.text

# Set up the text-to-speech request for Cantonese
input_text = texttospeech.SynthesisInput(text=response_data)
voice = texttospeech.VoiceSelectionParams(language_code='yue-HK', name='yue-HK-Standard-A') # Cantonese language
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

# Generate the audio file using the Google Cloud Text-to-Speech service
response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

# Save the audio file to your local directory
with open('test1.mp3', 'wb') as out:
    out.write(response.audio_content)
    print('Audio content written to file "test1.mp3"')


