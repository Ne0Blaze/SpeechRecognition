import json
from time import time
from webbrowser import Elinks
import requests
import json
import time


#API token to connect and request 
API_KEY_LISTENNOTES="929d25cf24e34626bd87bd62bf7bb413"
API_KEY_ASSEMBLYAI= "11572bf615e44255ad4e12ec42cdb1cc"


#config endpoints and authorization
transcript_endpoint='https://api.assemblyai.com/v2/transcript'
headers_assemblyai={
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

listennotes_episode_endpoint= 'https://listen-api.listennotes.com/api/v2/episodes'
headers_listennotes={
    "X-ListenAPI-Key": API_KEY_LISTENNOTES
}

#getting podcast episode info

def get_episode_url(episode_id):
    url=listennotes_episode_endpoint +'/'+ episode_id
    response= requests.request('GET', url, headers=headers_listennotes)
    data=response.json()

    episode_title= data['title']
    thumbnail= data['thumbnail']
    podcast_title= data['podcast']['title']
    audio_url= data['audio']
    return episode_title,thumbnail,podcast_title,audio_url

#trancribing the audio file
def transcribe(audio_url, auto_chapters):     #auto chapertx is a tool from Assembly AI that helps in identifying different chapters 
    transcript_request= {
        'audio_url': audio_url,
        'auto_chapters': auto_chapters
    }

    transcript_response = requests.post(transcript_endpoint, json= transcript_request, headers= headers_assemblyai)
    return transcript_response.json()['id']


#polling API to get the result 

def poll(transcript_id):
    polling_endpoint= transcript_endpoint +'/'+ transcript_id
    polling_response= requests.get(polling_endpoint, headers=headers_assemblyai)
    return polling_response.json()


#fetching the request status 

def get_trnascript_result_url(url, auto_chapters):
    transcript_id= transcribe(url, auto_chapters)
    while True:
        polling_response=poll(transcript_id)
        if polling_response['status']=='completed':
            return polling_response, None
        elif polling_response['status']=='error':
            return polling_response, polling_response['error']
        
        print("Wating for 60 sec")
        time.sleep(60)

#saving the transcript in a json file-- easier to work with in web application

def save_transcript(episode_id):
    episode_title,thumbnail,podcast_title,audio_url= get_episode_url(episode_id)
    data, error= get_trnascript_result_url(audio_url, auto_chapters=True)

    if data:
        filename=episode_id+'.json'
        with open(filename,'w') as f:
            chapters=data['chapters']

            data={'chapters': chapters}
            data['audio_url'] =audio_url
            data['thumbnail']= thumbnail
            data['podcast_title']= podcast_title
            data['episode_title']= episode_title

            json.dump(data, f)
            print('Trascript saved')
            return True
        
    elif error:
        print("Error!!", error)
        return False

        