#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json

from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    abort
)

app = Flask(__name__)


def setup():
    global data, options
    with open('data.json') as f:
        data = json.load(f)

    options = {'slugs': set()}
    for item in data:
        options['slugs'].add(item['slug'])


@app.route('/')
def home():

    # split data list into rows containing <cols> items
    cols = 4
    content = [data[i:min(i+4, len(data))] for i in range(0, len(data), cols)]
    return render_template('projects.html', content=content)


@app.route('/project/<slug>')
def project(slug):

    # check if all params are valid
    if slug not in options['slugs']:
        abort(404)

    project = [x for x in data if x['slug'] == slug][0]
    return render_template('project_page.html', content=project)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Setup
setup()

if __name__ == '__main__':
#    setup()
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
