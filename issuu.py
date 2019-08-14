import os
import hashlib
import urllib
import urllib2
import requests
import json
import sys
import upload
import ast


from werkzeug import secure_filename
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, make_response, send_from_directory
from embed import embeds

version = '0.7.166'


app = Flask(__name__)

issuu_key = os.environ.get('ISSUU_KEY')
issuu_secret = os.environ.get('ISSUU_SECRET')

access = 'public'
documentSortBy = 'publishDate'
documentStates = 'A'
format = 'json'
orgDocTypes = 'pdf,doc'
pageSize = 100
resultOrder = 'desc'
startIndex = 0


# test of issuu request
@app.route('/', methods=['GET'])
@app.route('/issuu', methods=['GET'])
def on_issuu_get():
    issues = get_issuu()
    result = set_flag(issues)
    return render_template('issuu.tpl', result = result, version = version)

@app.route('/new', methods=['GET'])
def give_issuu():
    return render_template('new.tpl', version = version)

@app.route('/digital', methods=['GET'])
def go_stats():
    return render_template('digital.tpl', version = version)

@app.route('/<name>', methods=['GET'])
def find_issuu(name):
    if name in embeds:
        result = embeds[name]
        print result
        return render_template('doc.tpl', result = result, name = name, version = version)
    else:
        return redirect(url_for('on_issuu_get'))

@app.route('/embed', methods=['POST'])
def post_embed():
    action = 'issuu.document_embed.add'
    issuu_url = 'http://api.issuu.com/1_0'
    documentId = '140702225753-ee2087e9ac60465babc876065483da86'
    readerStartPage = 0
    width = 400
    height = 300
    sig_query = issuu_secret + 'access' + access + 'action' + action + 'apiKey' + issuu_key + 'commentsAllowed' + commentsAllowed + 'description' + description + 'name' + name + 'publishDate' + publishDate + 'title' + title
    signature = hashlib.md5(sig_query).hexdigest()
    post_data = {'signature':signature, 'access':access, 'action':action, 'apiKey':issuu_key, 'commentsAllowed':commentsAllowed, 'description':description, 'name':name, 'publishDate':publishDate, 'title':title}
    r = requests.post(issuu_url, data=post_data, files={'file':f})
    message = str(r.text)
    print r.headers
    print r.text
    print r.status_code
    print message
    upload.delete_file(file)
    return render_template('ok.tpl', message = message, version = version)

@app.route('/upload', methods=['POST'])
def upload_issuu():
    action = 'issuu.document.upload'
    issuu_url = 'http://upload.issuu.com/1_0'
    btn = request.form['btn']
    if btn == 'Cancel':
        return redirect(url_for('on_issuu_get'))
    name = request.form['name']
    print name
    title = request.form['title']
    description = request.form['description']
    publishDate = request.form['publishDate']
    access = request.form['access']
    file = request.files['file']
    commentsAllowed = 'false'
    f = upload.upload_file(file)
    sig_query = issuu_secret + 'access' + access + 'action' + action + 'apiKey' + issuu_key + 'commentsAllowed' + commentsAllowed + 'description' + description + 'name' + name + 'publishDate' + publishDate + 'title' + title
    signature = hashlib.md5(sig_query).hexdigest()
    post_data = {'signature':signature, 'access':access, 'action':action, 'apiKey':issuu_key, 'commentsAllowed':commentsAllowed, 'description':description, 'name':name, 'publishDate':publishDate, 'title':title}
    r = requests.post(issuu_url, data=post_data, files={'file':f})
    message = str(r.text)
    print r.headers
    print r.text
    print r.status_code
    print message
    upload.delete_file(file)
    return render_template('ok.tpl', message = message, version = version)

def get_issuu():
    issuu_url = 'http://api.issuu.com/1_0?'
    action = 'issuu.documents.list'
    responseParams='name,documentId,title,description,publishDate'
    i = []
    result = []
    sig_query = issuu_secret + 'action' + action + 'apiKey' + issuu_key + 'documentSortBy' + documentSortBy + 'documentStates' + documentStates + 'format' + format + 'orgDocTypes' + orgDocTypes + 'pageSize' + str(pageSize) + 'responseParams' + responseParams + 'resultOrder' + resultOrder + 'startIndex' + str(startIndex)
    req_query = 'action' + '=' + action + '&' + 'apiKey' + '=' + issuu_key + '&' + 'documentSortBy' + '=' + documentSortBy + '&' + 'documentStates' + '=' + documentStates + '&' + 'format' + '=' + format + '&' + 'orgDocTypes' + '=' + orgDocTypes + '&' + 'pageSize' + '=' + str(pageSize) + '&' + 'responseParams' + '=' + responseParams + '&' + 'resultOrder' + '=' + resultOrder + '&' + 'startIndex' + '=' + str(startIndex)
    signature = hashlib.md5(sig_query).hexdigest()
    query = issuu_url + req_query + '&' + 'signature' + '=' + signature
    response = urllib2.urlopen(query)
    response = json.loads(response.read())
    i = response['rsp']['_content']['result']['_content']
    for doc in i:
        if not 'description' in list(doc['document']):
            doc['document']['description'] = doc['document']['title']
        if not doc['document']['description'][0] == '*':
            result.append({'description': doc['document']['description'], 'documentId': doc['document']['documentId'], 'name': doc['document']['name'], 'title': doc['document']['title']})
    # print result
    return result

def get_embed(documentId):
    issuu_url = 'http://api.issuu.com/1_0?'
    action = 'issuu.document_embeds.list'
    responseParams = 'dataConfigId,documentId'
    embedSortBy = 'documentId'
    i = []
    result = []
    sig_query = issuu_secret + 'action' + action + 'apiKey' + issuu_key + 'documentId' + documentId + 'embedSortBy' + embedSortBy + 'format' + format + 'pageSize' + str(pageSize) + 'responseParams' + responseParams + 'resultOrder' + resultOrder + 'startIndex' + str(startIndex)
    req_query = 'action' + '=' + action + '&' + 'apiKey' + '=' + issuu_key + '&' + 'documentId' + '=' + documentId + '&' + 'embedSortBy' + '=' + embedSortBy + '&'  + 'format' + '=' + format + '&' +  'pageSize' + '=' + str(pageSize) + '&' + 'responseParams' + '=' + responseParams + '&' + 'resultOrder' + '=' + resultOrder + '&' + 'startIndex' + '=' + str(startIndex)
    signature = hashlib.md5(sig_query).hexdigest()
    query = issuu_url + req_query + '&' + 'signature' + '=' + signature
    response = urllib2.urlopen(query)
    response = json.loads(response.read())
    result = response['rsp']['_content']['result']['_content'][0]['documentEmbed']['dataConfigId']
    return result

def set_flag(issues):
    result = []
    for i in issues:
        if i['name'] in embeds:
            i['dataconfigId'] = embeds[(i['name'])]['dataconfigId']
            result.append(i)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 17939))
    app.run(host='0.0.0.0', port=port, debug=True)
