#transcripting audio from a recorded file using assemblyAI API

import requests
from speechRecognitionFromAudioFile.apiConnect import *
import sys

filename = sys.argv[1]      #takes the second argument in the console as the filename
audio_url = upload(filename)

save_transcript(audio_url, filename)