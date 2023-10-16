# Import the necessary modules
from google.cloud import texttospeech
import sys
sys.path.append("")
from config import GOOGLE_SERVICE_ACCOUNT_PATH
import requests


def text_to_speech(text):
    # Set up the credentials for the Google Cloud service
    client = texttospeech.TextToSpeechClient.from_service_account_json(GOOGLE_SERVICE_ACCOUNT_PATH)
    '''
    # Define the Google Cloud function URL and JSON data
    url = 'replace with your cloud function'
    data = {'name': 'test'} # Replace this with your own JSON data

    # Send the push request with JSON data to the Cloud function and retrieve the response
    response = requests.post(url, json=data)
    response_data = response.text

    # Set up the text-to-speech request for Cantonese
    input_text = texttospeech.SynthesisInput(text=response_data)
    '''
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='yue-HK', name='yue-HK-Standard-A') # Cantonese language
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Generate the audio file using the Google Cloud Text-to-Speech service
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    # Save the audio file to your local directory
    audio_file_path = 'temp_audio.mp3'
    with open(audio_file_path, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {audio_file_path}')
    return audio_file_path

def play_audio(file_path):
    pass

if __name__ == "__main__":
    audio = text_to_speech('偵測到有工人沒有佩戴頭盔！')
    play_audio(audio)