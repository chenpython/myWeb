import json
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'


@app.route('/admin/minio/upload', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']

        path = os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename))

        f.save(path)

        return {'data': [path], 'subPath': request.form['subPath']}

    else:

        return 'hello'


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8050)
