from flask import Flask, request, json
from flask_mail import Message, Mail
from emailFunctions import configureEmail, createMessage
import db, utilities

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# token authentication
secretToken = "xdxdxd"
def checkToken(func):
    def wrapper():
        givenToken = request.headers.get('token')
        if givenToken != secretToken:
            return json.dumps({"success" : False, 'error' : 'wrong token'})
        return func()
    return wrapper

# gmail configurations
mail = configureEmail(app)



@app.route('/login', methods=['GET', 'POST'])
@checkToken
def login():
    if request.method == 'POST':
        user = request.json['user']
        if not db.userExists(user):
            return {'success': False, 'error' : 'wrong username or email'}
        username, userMail = db.getData(user)
        code = send_email(userMail)
        response = json.dumps({"success" : True, "username" : username, "mail" : userMail, "code" : code })
        return response
    return {'success': False, 'error': 'wrong method'}

@app.route('/register', methods=['GET', 'POST'])
@checkToken
def register():
    if request.method == 'POST':
        username = request.json['username']
        userMail = request.json['userMail']
        if db.userOccupied(username, userMail):
            return {'success': False, 'error' : 'this username or email already is registered'}
        code = send_email(userMail)
        response = json.dumps({"success": True, "username" : username, "mail" : userMail, "code" : code})
        return response
    return {'success': False, 'error': 'wrong method'}

@app.route('/createUser', methods=['GET', 'POST'])
@checkToken
def createUser():
    if request.method == 'POST':
        username = request.json['username']
        userMail = request.json['userMail']
        db.createUser(username, userMail)
        response = json.dumps({"success" : True})
        return response
    return {'success': False, 'error': 'wrong method'}

def send_email(toMail):
    codeLength = 6
    code = utilities.getCode(codeLength)
    msg = createMessage(toMail, "Your code is " + code)
    mail.send(msg)
    return code



