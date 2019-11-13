#!/usr/bin/env python3

from flask import Flask, request
from functools import partial
import os
from threading import Thread


app = Flask(__name__)
sonar_key = open('.sonar').read().strip()


def analyze(target):
    os.chdir('upload-src')
    try:
        print(target)
        tdir = target.replace('.tar.gz', '')
        os.system('mkdir '+tdir)
        os.system('tar xfz '+target+' -C '+tdir)
        os.chdir(tdir)
        try:
            os.system('mvn -P!update-parent,nogui clean compile')
            os.system('mvn sonar:sonar -Dsonar.projectKey=ProvGot -Dsonar.host.url=http://localhost:7000 -Dsonar.login=%s' % sonar_key)
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
        Thread(target=partial(analyze, file.filename)).start()
    return '''
    <!doctype html>
    <title>Upload Source</title>
    <h1>Upload source</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Push>
    </form>
    '''


app.run()
