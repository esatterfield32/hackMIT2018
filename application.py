# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 16:19:53 2018

@author: wilson
"""

import requests
import json
import time
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import Flask
from flask import request
from flask import jsonify

def get_entities(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    # if isinstance(text, six.binary_type):
    #     text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    # entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
    #                'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    entityList = []
    for entity in entities:
        if entity.name not in entityList:
           entityList.append(entity.name)
    
    return entityList

API_KEY = "Bearer KEY"
HEADERS = {'Authorization': API_KEY}

def submit_job_url(media_url):
    url = "https://api.rev.ai/revspeech/v1beta/jobs"
    payload = {'media_url': media_url,
               'metadata': "Hack MIT Team LERL"}
    request = requests.post(url, headers=HEADERS, json=payload)

    if request.status_code != 200:
        raise

    response_body = request.json()
    return response_body['id']

def view_job(id):
    url = f'https://api.rev.ai/revspeech/v1beta/jobs/{id}'
    request = requests.get(url, headers=HEADERS)

    if request.status_code != 200:
        raise

    response_body = request.json()
    return response_body

def get_transcript(id):
    url = f'https://api.rev.ai/revspeech/v1beta/jobs/{id}/transcript'
    headers = HEADERS.copy()
    headers['Accept'] = 'application/vnd.rev.transcript.v1.0+json'
    request = requests.get(url, headers=headers)

    if request.status_code != 200:
        raise

    response_body = request.json()
    return response_body

def get_text_body(transcript1):
    transcript = transcript1
    textBody = ''
    for monologue in transcript.values():
        for item in monologue:
            for nextItem in item['elements']:
                textBody = textBody + nextItem['value']
    return textBody

def submit_job_file(file):
    url = "https://api.rev.ai/revspeech/v1beta/jobs"
    files = { 'media': (file, open(file, 'rb'), 'audio/mp3') }
    request = requests.post(url, headers=HEADERS, files=files)
    if request.status_code != 200:
        raise

    response_body = request.json()
    return response_body['id']

def submit_and_return_file(file):
    print ("Submitting job with file")
    id = submit_job_file(file)
    print ("Job created")
    view_job(id)
    # while True:
    #     job = view_job(id)
    #     status = job["status"]
    #     print (f'Checking job transcription status: { status }')
    #     if status == "transcribed":
    #         break
    #     if status == "failed":
    #         raise

    #     print ("Trying in another 10 seconds")
    #     time.sleep(10)

    return id


def test_workflow_with_url(url):
    print ("Submitting job with URL")
    id = submit_job_url(url)
    print ("Job created")
    print ('ID: ' + id )
    view_job(id)
    
    while True:
        job = view_job(id)
        status = job["status"]
        print (f'Checking job transcription status: { status }')
        if status == "transcribed":
            break
        if status == "failed":
            raise

        print ("Trying in another 10 seconds")
        time.sleep(10)

    return get_transcript(id)



# def main():
#     # Testing with URL
#     #media_url = "http://www.obamadownloads.com/mp3s/yes-we-can-speech.mp3"
#     fileName = 'yes-we-can-speech.mp3'
#     print(get_entities(get_text_body(submit_and_return_file(fileName))))
# #     # get_entities(test_workflow_with_url(media_url))
# #     print(get_entities(get_text_body(get_transcript(216064345)))

# if __name__ == "__main__":
#     main()


application = Flask(__name__)
 
@application.route("/", methods=['GET','POST'])
def start_job():
    # return str(get_entities(get_text_body(test_workflow_with_url(media_url)))) #get_text_body(get_transcript(216064345))
    if request.method == 'GET':
        fileName = 'yes-we-can-speech.mp3'
        return(submit_and_return_file(fileName))
    if request.method == 'POST':
        id = int(request.form['id'])
        job = view_job(id)
        status = job["status"]
        print(status)
        if status == "transcribed":
            finalTranscript = get_text_body(get_transcript(id))
            finalKeywords = get_entities(finalTranscript)
            output = {'complete':'yes'}
            output['transcript'] = finalTranscript
            output['keywords'] = finalKeywords
            print(jsonify(output))
            return jsonify(output)
        else: 
            return jsonify({'complete':'no'})
 
if __name__ == "__main__":
    application.run()
