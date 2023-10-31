from flask import *
from datetime import datetime, timedelta
from module_program.database import *
from module_program.env_key import *
from module_program.token_function import *
from module_program.boto3_function import *
import json
import uuid

app=Flask(__name__)
app.secret_key = 'your_secret_key'

def results_convert(result):
	response = Response(json.dumps(result,ensure_ascii = False), content_type = 'application/json; charset = utf-8')
	return response

# @app.route("/api/user",methods=["POST"])
# def memberSignup():
#     data = request.get_json()
#     account = data.get("account")
#     email = data.get("email")
#     password = data.get("password")
#     emailData = list(databaseConnect("SELECT email FROM member"))
#     try:
#         for data in emailData:
#             if email == data[0]:
#                 result = {"error": True,"message": "此信箱已註冊"}
#                 return results_convert(result),403
#             else:
#                 pass
#         databaseConnect("INSERT INTO member(account,email,password)VALUES(%s,%s,%s)",(account,email,password))
#         result = {"data":"註冊成功"}
#         return results_convert(result)        
#     except Exception as err:
#         result = {
#             "error":True,
#             "message":err
#         }
#         return results_convert(result),500

# @app.route("/api/user/auth",methods=["PUT"])
# def signin():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#     memberInfor = databaseConnect("SELECT email,password FROM member")
#     try:
#         if (email,password) in memberInfor:
#             baseInfor = databaseConnect("SELECT id,account,email FROM member WHERE email = %s AND password = %s",(email,password))
#             filedict = {
#                 "id":baseInfor[0][0],
#                 "name":baseInfor[0][1],
#                 "email":baseInfor[0][2],
#                 "exp":datetime.utcnow()+timedelta(days=7)
#             }
#             token_algorithm = 'HS256'
#             encode_token = encoding(filedict, token_key, algorithm= token_algorithm)
#             return encode_token
#         else:
#             for infoItem in memberInfor:
#                 if email not in infoItem[0]:
#                     result = {"error": True,"message": "此信箱未註冊"}
#                     return results_convert(result),400
#                 elif email in infoItem[0] or password in infoItem[1]:
#                     result = {"error": True,"message": "信箱或密碼錯誤"}
#                     return results_convert(result),400
#     except Exception as err:
#         result = {"error": True,"message": err}
#         return results_convert(result),500
# @app.route("/api/user/auth",methods=['GET'])
# def checkLogin():
#     try:
#         token = request.headers.get('Authorization')
#         if token:
#             decode_token = token.split('Bearer ')
#             decode_algorithms = ['HS256']
#             information = decoding(decode_token[1], token_key, decode_algorithms)
#             return information
#         else:
#             return redirect("/")
#     except Exception as err:
#         result = {"error": True,"message": err}
#         finalresult = results_convert(result)
#         return finalresult,500

# @app.route("/api/message",methods=['POST'])
# def storeMessage():
#     try:
#         message = request.form.get('text')
#         messageID = request.form.get('message_id')
#         picture = request.files['photo']
#         databaseConnect("INSERT INTO message (message_id, photo, message) VALUE (%s, %s, %s)",\
#                         (messageID, picture, message))
#         return "{'data':'success'}"
#     except Exception as err:
#         print(err)
#         return "{'error':True,'message':err}"

@app.route("/api/message",methods=['POST'])
def storeMessage():
    try:
        messageID = str(uuid.uuid4())
        message = request.form['text']
        picture = request.files['photo']
        bucket_name = getBucketName()
        uploadToS3(picture,bucket_name,picture.filename)
        s3_url = f"https://dx26yxwvur965.cloudfront.net/{messageID}+{picture.filename}"
        print(s3_url)
        databaseConnect("INSERT INTO message (message_id, photo, message) VALUE (%s, %s, %s)",\
                        (messageID, s3_url, message))
        return "{'data':'success'}"
    except Exception as err:
        print(err)
        return "{'error':True,'message':err}"
    
@app.route("/api/record",methods=['GET'])
def showRecords():
    datas = databaseConnect("SELECT * FROM message")
    count = 1
    result={}
    for data in datas:
        result[f"data{count}"]= {
            'recordID': data[0],
            'picture': data[1],
            'text': data[2]
        }
        count+=1
    return results_convert(result)

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True, host="0.0.0.0", port=4000)