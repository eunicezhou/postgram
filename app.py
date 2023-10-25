from flask import *
from datetime import datetime, timedelta
from module_program.database import *
from module_program.env_key import *
from module_program.token import *
import json

app=Flask(__name__)
app.secret_key = app_key

def results_convert(result):
	response = Response(json.dumps(result,ensure_ascii = False), content_type = 'application/json; charset = utf-8')
	return response

@app.route("/api/user",methods=["POST"])
def memberSignup():
    data = request.get_json()
    account = data.get("account")
    email = data.get("email")
    password = data.get("password")
    emailData = list(connect("SELECT email FROM member"))
    try:
        for data in emailData:
            if email == data[0]:
                result = {"error": True,"message": "此信箱已註冊"}
                return results_convert(result),403
            else:
                pass
        connect("INSERT INTO member(account,email,password)VALUES(%s,%s,%s)",(account,email,password))
        result = {"data":"註冊成功"}
        return results_convert(result)        
    except Exception as err:
        result = {
            "error":True,
            "message":err
        }
        return results_convert(result),500

@app.route("/api/user/auth",methods=["PUT"])
def signin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    memberInfor = connect("SELECT email,password FROM member")
    try:
        if (email,password) in memberInfor:
            baseInfor = connect("SELECT id,account,email FROM member WHERE email = %s AND password = %s",(email,password))
            filedict = {
                "id":baseInfor[0][0],
                "name":baseInfor[0][1],
                "email":baseInfor[0][2],
                "exp":datetime.utcnow()+timedelta(days=7)
            }
            token_algorithm = 'HS256'
            encode_token = encoding(filedict, token_key, algorithm= token_algorithm)
            return encode_token
        else:
            for infoItem in memberInfor:
                if email not in infoItem[0]:
                    result = {"error": True,"message": "此信箱未註冊"}
                    return results_convert(result),400
                elif email in infoItem[0] or password in infoItem[1]:
                    result = {"error": True,"message": "信箱或密碼錯誤"}
                    return results_convert(result),400
    except Exception as err:
        result = {"error": True,"message": err}
        return results_convert(result),500

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True, host="0.0.0.0", port=3000)