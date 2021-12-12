import json
from Script.BD.database import *
from flask import Flask, render_template, request, url_for, redirect, session
app = Flask(__name__, static_folder='static',template_folder='templates')
app.config['SECRET_KEY'] = '12345678'

@app.route('/',methods=['GET'])
def init():
    session.clear()
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    dataJson = json.loads(request.form['dataJson'])
    print(dataJson)
    credentials = hash_credentials(dataJson)
    conexion = conecta_db("DESart.db")
    response = valida_login(conexion,credentials[0],credentials[1])
    if(response == "Welcome!"):
        session["user"] = credentials[0]
        session["pswd"] = credentials[1]
    else:
        session.clear()
    close_db(conexion)
    return response

@app.route('/registration',methods=['GET'])
def registration():
    return render_template('create count.html')

@app.route('/register',methods=['POST'])
def register():
    dataJson = json.loads(request.form['dataJson'])
    conexion = conecta_db("DESart.db")
    response = alta_usr(conexion,dataJson)
    close_db(conexion)
    return response

@app.route('/menu',methods=['GET'])
def menu():
    try:
        if session["user"]!=None:
            conexion = conecta_db("DESart.db")
            response = consulta_nombre(conexion,session["user"])
            if(response!="Not found"):
                session["name"] = response
                response = consulta_tipousr(conexion,session["user"])
                session["typeUser"] = response
                response = consulta_genero(conexion,session["user"])
                session["gender"] = response
                close_db(conexion)
                if(session["typeUser"] == 1):
                    return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"])
                if(session["typeUser"] == 2):
                    return render_template('client_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"])
                if(session["typeUser"] == 3):
                    return render_template('notary_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"])
            else:
                close_db(conexion)
                return redirect(url_for("init"))
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n {} \n".format(e))
        return redirect(url_for("init"))

def init_db():
    conexion = conecta_db("DESart.db")
    crea_tbs(conexion)
    close_db(conexion)
    print(" * Data Base Status: Ok")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=80,debug=True)