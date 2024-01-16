from flask import *
from datetime import datetime, timedelta
from module_program.database import *
from module_program.env_key import *
from module_program.token_function import *
from module_program.boto3_function import *
import json
import jwt
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests

app=Flask(__name__)
app.secret_key = 'your_secret_key'

def results_convert(result):
	response = Response(json.dumps(result,ensure_ascii = False), content_type = 'application/json; charset = utf-8')
	return response

@app.route("/api/login", methods=['POST'])
def login():
    google_id_token = request.data.decode('utf-8') 
    try:
        idinfo = id_token.verify_oauth2_token(google_id_token, requests.Request(), "575527734855-07an02o2nqore7i6775mk6fnt4p0dhee.apps.googleusercontent.com")
        google_exp = idinfo['exp']
        exp_datetime = datetime.utcfromtimestamp(google_exp)
        userInfo = {
            'name': idinfo['name'],
            'email': idinfo['email'],
            'picture': idinfo['picture'],
            'exp': exp_datetime
        }
        custom_token = jwt.encode(userInfo, 'your_secret_key', algorithm='HS256')
        return jsonify({'custom_token': custom_token})
    except Exception as err:
        return jsonify({'error': f'{err}'})
    
@app.route("/api/login", methods=['GET'])
def memberData():
    header = request.headers.get('Authorization')
    if header is None or not header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401
    custom_token = header.split('Bearer ')[1]
    try:
        decoded_payload = jwt.decode(custom_token, 'your_secret_key', algorithms=['HS256'])
        print(decoded_payload)
        return jsonify(decoded_payload)
    except Exception as err:
        return jsonify({'error': f'{err}'}), 500

@app.route("/api/message",methods=['POST'])
def storeMessage():
    try:
        messageID = str(uuid.uuid4())
        member = request.form['name']
        picture = request.form['picture']
        message = request.form['text']
        message_photo = request.files['photo']
        message_photo_file = f"{messageID}.jpeg"
        bucket_name = getBucketName()
        uploadToS3(message_photo,bucket_name,message_photo_file)
        s3_url = f"https://dx26yxwvur965.cloudfront.net/{message_photo_file}"
        databaseConnect("INSERT INTO message (member_name, picture, message_id, photo, message) VALUES (%s, %s, %s, %s, %s)",\
                        (member, picture, messageID, s3_url, message))
        return jsonify({'data':'success'})
    except Exception as err:
        print(err)
        return jsonify({'error': True, 'message': str(err)})
    
@app.route("/api/record",methods=['GET'])
def showRecords():
    datas = databaseConnect("SELECT * FROM message")
    count = 1
    result={}
    for data in datas:
        result[f"data{count}"]= {
            'recordID': data[0],
            'member_name':data[3],
            'picture': data[4],
            'photo': data[1],
            'text': data[2]
        }
        count+=1
    return results_convert(result)

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True, host="0.0.0.0", port=4000)