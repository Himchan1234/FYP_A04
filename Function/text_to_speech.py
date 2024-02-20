# Import the necessary modules
from google.cloud import texttospeech
import sys
sys.path.append("")
from config import GOOGLE_SERVICE_ACCOUNT_PATH
import os
from playsound import playsound
from docx import Document

def text_to_speech(text, language_code='yue-HK', name='yue-HK-Standard-A', speaking_rate=1.5):
    # Set up the credentials for the Google Cloud service
    client = texttospeech.TextToSpeechClient.from_service_account_json(GOOGLE_SERVICE_ACCOUNT_PATH)
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=name) 
    # yue-HK and yue-HK-Standard-A for Cantonese language
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3,
                                            speaking_rate=speaking_rate)

    # Generate the audio file using the Google Cloud Text-to-Speech service
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    # Save the audio file to your local directory
    audio_file_path = 'temp.mp3'
    with open(audio_file_path, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {audio_file_path}')
    return audio_file_path

def play_audio(file_path):
    abs_path = os.path.abspath(file_path)
    print(abs_path)
    playsound(abs_path)

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []

    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)

    return '\n'.join(full_text)

if __name__ == "__main__":
    file_path = './Script/GDSC_competition_Video_Script_A04-1 (1).docx'
    content = read_docx(file_path)
    audio = text_to_speech(content, "us-EN", "en-US-Standard-A", 1.5)
    
