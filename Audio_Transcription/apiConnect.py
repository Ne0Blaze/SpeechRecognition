import json
from webbrowser import Elinks
import requests   #used to connect and request API
import time

#diclaring API token to  auth the request
API_KEY_ASSEMBLYAI= "11572bf615e44255ad4e12ec42cdb1cc"

upload_endpoint= "https://api.assemblyai.com/v2/upload"
transcript_endpoint= "https://api.assemblyai.com/v2/transcript"

headers_auth_only= {'authorization': API_KEY_ASSEMBLYAI}

headers={
    "authorization":API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

CHUNK_SIZE= 5_242_880 #API reads data in chunks --- 5MB

#uploading file to the API
def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data=f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data
    
    upload_response= requests.post(upload_endpoint , headers= headers_auth_only, data=read_file(filename))
    return upload_response.json()['upload_url']


#transcribing request to the api

def transcribe(audio_url):
    transcript_request={ 'audio_url':audio_url}
    transcript_response= requests.post(transcript_endpoint , json= transcript_request, headers=headers)
    return transcript_response.json()['id']


#polling API to get the result 

def poll(transcript_id):
    polling_endpoint= transcript_endpoint+'/'+ transcript_id
    polling_response= requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


#fetching the request status 

def get_trnascript_result_url(url):
    transcript_id= transcribe(url)
    while True:
        polling_response=poll(transcript_id)
        if polling_response['status']=='completed':
            return polling_response, None
        elif polling_response['status']=='error':
            return polling_response, polling_response['error']
        
        print("Wating for 10 sec")
        time.sleep(10)

#saving the trancription  in a file

def save_transcript(url, title):
    polling_reponse, error = get_trnascript_result_url(url)
    if polling_reponse:
        filename= title+'.txt'
        with open(filename, 'w') as f:
            f.write(polling_reponse['text'])
        print("Transcription saved")

    elif error:
        print("Error!!", error)





