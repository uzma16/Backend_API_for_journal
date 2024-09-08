from django.core.files.base import ContentFile
from mutagen.mp3 import MP3
from textblob import TextBlob

def calculate_audio_length(audio_file):
    try:
        audio_content = audio_file.open().read()  # Read the content of the audio file
    except Exception:
        # Handle the exception, e.g., log or raise a more specific error
        return None

    audio_content_file = ContentFile(audio_content)  # Create a ContentFile
    audio = MP3(audio_content_file)
    audio_length_seconds = audio.info.length
    return audio_length_seconds

def get_sentiments(text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        return sentiment