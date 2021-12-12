import json
from Script.BD.database import *
from flask import Flask, render_template, request
app = Flask(__name__, static_folder='static',template_folder='templates')

@app.route('/',methods=['GET'])
def init():
    return render_template('login.html')

@app.route('/registration',methods=['GET'])
def registration():
    return render_template('create count.html')

@app.route('/register',methods=['POST'])
def register():
    dataJson = json.loads(request.form['dataJson'])
    print(type(dataJson))
    print(dataJson)
    return "Ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)