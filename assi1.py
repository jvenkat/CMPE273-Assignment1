from flask import Flask, render_template,request, Response,jsonify
import rocksdb
import uuid
import os
from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import subprocess
from subprocess import Popen, PIPE
import sys


UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['py'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/scripts', methods=['POST'])

def post():
        db = rocksdb.DB("Assignment2.db", rocksdb.Options(create_if_missing=True))
        print("post")
        if request.method == 'POST':
              file = request.files['data']
              if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        key = uuid.uuid4().hex
                        keyb= key.encode('utf-8')
                        unicode_name=unicode(filename, "utf-8", errors="ignore")
                        value=unicode_name.encode("utf-8")
                        valueb=value.encode('utf-8')
                        db.put(keyb,valueb)
                        a={'script-id': keyb}
                        #a= ""+"{"+ "\n"+"   "+"script-id:"+keyb+ "\n"+"}"
                        resp=jsonify(a)
                        if resp.status_code == 200:
                            resp.status_code=201
                            resp.headers[''] = ''
                        #resp = Response(js, status=201, mimetype='application/json')
                        return resp
                        #return jsonify({"Created": True}), 201

#@app.errorhandler(404)


@app.route('/api/v1/scripts/<script_id>', methods=['GET'])
def get(script_id):
        db = rocksdb.DB("Assignment2.db", rocksdb.Options(create_if_missing=True))
        print("get")
        if request.method == 'GET':
            #file = request.files['data']
        #- retrieve the value from DB by the given key. Needs to convert request.data string to utf-8 bytes.
            #key = (request.data).encode(encoding='UTF-8',errors='strict')
            value = db.get(script_id)
            path="./"+value
            p=subprocess.Popen([sys.executable, path],stdout=subprocess.PIPE)
            return p.stdout.read()
            #system('python' value)


if(__name__=="__main__"):
    app.run(debug=True)
