import os
import hashlib
import requests
import json
import sys

from flask import Flask, request, redirect, url_for, render_template
from upload import upload_file, delete_file

version = '0.8.173'


app = Flask(__name__)

issuu_key = os.environ.get('ISSUU_KEY')
issuu_secret = os.environ.get('ISSUU_SECRET')
# http = urllib3.PoolManager()

access = 'public'
documentSortBy = 'publishDate'
documentStates = 'A'
docFormat = 'json'
orgDocTypes = 'pdf,doc'
pageSize = 100
resultOrder = 'desc'
startIndex = 0

names = [str(i) for i in range(200)]

# test of issuu request
@app.route('/', methods=['GET'])
def get_issuu():
# ==========================================
    result = list_docs()
    return render_template('issuu.tpl', result=result, version=version)


@app.route('/new', methods=['GET'])
def new_issuu():
# ==========================================
    return render_template('new.tpl', version=version)


@app.route('/digital', methods=['GET'])
def get_stats():
# ==========================================
    return render_template('digital.tpl', version=version)


@app.route('/<name>', methods=['GET'])
def find_issuu(name):
# ==========================================
    if name in names:
        result = list_docs()
        if result != []:
            result = next((i for i in result if i['name'] == name), None)
            return render_template('doc.tpl', result=result, version=version)

    return redirect(url_for('get_issuu'))


@app.route('/upload', methods=['POST'])
def post_issuu():
# ==========================================
    issuu_url = 'http://upload.issuu.com/1_0'
    access = request.form['access']
    action = 'issuu.document.upload'
    commentsAllowed = 'false'
    description = request.form['description']
    name = request.form['name']
    publishDate = request.form['publishDate']
    title = request.form['title']
    btn = request.form['btn']

    if btn == 'Cancel':
        return redirect(url_for('get_issuu'))

    file = request.files['file']
    f = upload_file(file)

    sig_query = '{}access{}action{}apiKey{}commentsAllowed{}description{}name{}publishDate{}title{}'.format(
        issuu_secret, access, action, issuu_key, commentsAllowed, description, name, publishDate, title)
        
    signature = hashlib.md5(sig_query.encode("utf-8")).hexdigest()

    data = {
        'signature': signature,
        'access': access,
        'action': action,
        'apiKey': issuu_key,
        'commentsAllowed': commentsAllowed,
        'description': description,
        'name': name,
        'publishDate': publishDate,
        'title':title
        }
    
    r = requests.post(issuu_url, data=data, files={'file':f})
    message = str(r.text)

    print(r.headers)
    print(r.text)
    print(r.status_code)
    print(message)

    delete_file(file)
    return render_template('ok.tpl', message=message, version=version)


def list_docs():
# ==========================================
    issuu_url = 'http://api.issuu.com/1_0'
    action = 'issuu.documents.list'
    responseParams='name,documentId,title,description,publishDate'

    sig_query = '{}action{}apiKey{}documentSortBy{}documentStates{}format{}orgDocTypes{}pageSize{}responseParams{}resultOrder{}startIndex{}'.format(
            issuu_secret, action, issuu_key, documentSortBy, documentStates, docFormat, orgDocTypes, str(pageSize), responseParams, resultOrder, str(startIndex))

    signature = hashlib.md5(sig_query.encode("utf-8")).hexdigest()

    data = {
        'action': action,
        'apiKey': issuu_key,
        'documentSortBy': documentSortBy,
        'documentStates': documentStates,
        'format': docFormat,
        'orgDocTypes': orgDocTypes,
        'pageSize': str(pageSize),
        'responseParams': responseParams,
        'resultOrder': resultOrder,
        'startIndex': str(startIndex),
        'signature': signature,
        }

    try:
        response = requests.get('http://api.issuu.com/1_0', data)
        response = response.json()['rsp']['_content']['result']['_content']
    except:
        response = None

    result = []

    if response:
        for i in response:
            if i['document']['name'] in names:
                result.append({
                    'name': i['document']['name'],
                    'documentId': i['document']['documentId'],
                    'title': i['document']['title'],
                    'description': i['document']['description']          
                    })

    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 17939))
    app.run(host='0.0.0.0', port=port, debug=True)
