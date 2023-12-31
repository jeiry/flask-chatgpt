#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import json
import yaml
file = open("conf.yaml", 'r', encoding="utf-8")
file_data = file.read()
file.close()
config = yaml.load(file_data, Loader=yaml.FullLoader)

import openai
openai.api_key = config['key']

import uuid
uid = uuid.uuid1()
uid =str(uid).split('-')[4]

from flask_cors import CORS
from flask import Flask, request,render_template,send_from_directory,send_file,request
app = Flask(__name__, template_folder='templates', static_folder='static')

CORS(app)
isSent = False
chatArr = []
selectModel = ''
completion_text = ''
isFinish = False
iserror = False
def chat():
    global isSent,selectModel,isFinish,completion_text,iserror
    completion_text = ""
    # isFinish = False
    # iserror = False
    print(chatArr,selectModel)
    try:
        completion = openai.ChatCompletion.create(model=selectModel,
                                            stream=True,
                                            temperature=0.8,
                                            messages=chatArr)
        collected_events = []
        # iterate through the stream of events
        for event in completion:
            # if event['choices'][0]['finish_reason'] != 'stop':
            # print(event['choices'][0]['delta'])
            # if "content" in event['choices'][0]['delta']:
            if event['choices'][0]['finish_reason'] != 'stop':
                collected_events.append(event)  # save the event response
                event_text = event['choices'][0]['delta']['content']  # extract the text
                print(event_text)
                # print(event['choices']['delta']['content'])
                completion_text += event_text  # append the textnt the delay and text
            else:
                print(event['choices'][0],'end')
                chatArr.append({'role':'assistant','content':completion_text})
                # completion_text = ""
                isFinish = True
                isSent = False
    except FileNotFoundError:
        iserror = True
        isFinish = True
        isSent = False
        print('error')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sent',methods=["POST"])
def sent():
    global isSent,selectModel,isFinish,iserror
    isFinish = False
    # account = request.form.get("account")
    json_data = request.json

    role = json_data['params']['role']
    input = json_data['params']['input']
    inputM = json_data['params']['inputM']
    if role == 'system':
        chatArr.append({
            'role':role,'content':input
        })
        isFinish = True
    elif role == 'user':
        selectModel = inputM
        chatArr.append({
            'role':role,'content':input
        })

        if isSent == False:
            isFinish = False
            iserror = False
            t1 = threading.Thread(target=chat)
            t1.daemon = True
            t1.start()
            isSent = True
            pass

    return json.dumps({'status':1})


@app.route('/check')
def check():
    global isSent,completion_text,iserror
    print(completion_text,isFinish,'check')
    return json.dumps({'status':1,'completion_text':completion_text,'isstop':isFinish,'error':iserror})

@app.route('/reset')
def reset():
    global isSent,completion_text,iserror,isFinish,chatArr
    iserror = False
    isFinish = True
    isSent = False
    completion_text=""
    chatArr = []
    return json.dumps({'status':1})
@app.route('/caps/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    path = './caps/'+filename
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False, debug=True)
