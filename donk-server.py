#!/usr/bin/env python3

import os
from flask import Flask, request


app = Flask(__name__)
sonar_key = open('.sonar').read().strip()


def analyze(target):
    os.chdir('upload-src')
    try:
        print(target)
        tdir = target.replace('.tar.gz', '')
        os.system('mkdir '+tdir)
        os.system('tar xfzv '+target+' -C '+tdir)
        os.chdir(tdir)
        try:
            os.system('mvn sonar:sonar -Dsonar.projectKey=JbTryout -Dsonar.host.url=http://localhost:9000 -Dsonar.login=%s' % sonar_key)
        except Exception as e:
            print(e)
        os.chdir('..')
    except Exception as e:
        print(e)
    os.chdir('..')


@app.route('/upload-src', methods='GET POST'.split())
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        target = os.path.join('upload-src', file.filename)
        file.save(target)
        analyze(file.filename)
    return '''
    <!doctype html>
    <title>Upload Source</title>
    <h1>Upload source</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Push>
    </form>
    '''


try: os.mkdir('upload-src')
except: pass
app.run()
