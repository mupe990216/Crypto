import json, os

from flask.wrappers import Response
from Script.BD.database import *
from Script.PIC.pictures import *
from Script.RSA.RSAFunctions import *
from Script.AES.AESfunctions import *
from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename
KEY_FOLDER = os.path.abspath("./keys/")
ART_FOLDER = os.path.abspath("./static/arts/")
VERIFY_FOLDER = os.path.abspath("./static/verify/")
CIPHER_FOLDER = os.path.abspath("./static/ciphers/")
UPLOAD_FOLDER = os.path.abspath("./static/uploads/")
PREVIEW_FOLDER = os.path.abspath("./static/preview/")
DECIPHER_FOLDER = os.path.abspath("./static/deciphers/")

app = Flask(__name__, static_folder='static',template_folder='templates')
app.config['SECRET_KEY'] = '4c061725a59e73710b110fc19cdfb00598a20a06ac654ffac7808ce5e1b649b0'
app.config["KEY_FOLDER"] = KEY_FOLDER
app.config["ART_FOLDER"] = ART_FOLDER
app.config["VERIFY_FOLDER"] = VERIFY_FOLDER
app.config["CIPHER_FOLDER"] = CIPHER_FOLDER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PREVIEW_FOLDER"] = PREVIEW_FOLDER
app.config["DECIPHER_FOLDER"] = DECIPHER_FOLDER

@app.route('/',methods=['GET'])
def init():
    session.clear()
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    dataJson = json.loads(request.form['dataJson'])
    credentials = hash_credentials(dataJson)
    conexion = conecta_db("DESart.db")
    response = valida_login(conexion,credentials[0],credentials[1])
    if(response == "Welcome!"):
        session["user"] = credentials[0]
        session["pswd"] = credentials[1]
        session["email"] = consulta_email(conexion,session["user"])
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
    response = alta_usr(conexion,dataJson,app.config["KEY_FOLDER"])
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
                    return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=0)
                if(session["typeUser"] == 2):
                    return redirect(url_for("public"))
                if(session["typeUser"] == 3):
                    return render_template('notary_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=0)
            else:
                close_db(conexion)
                return redirect(url_for("init"))
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception menu: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/upload',methods=['GET','POST'])
def upload():
    try:        
        if session["user"]!=None:
            if request.method == 'GET':
                return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=1)
            else:
                if not "imageFile" in request.files:
                    return "No file part in the form."
                file = request.files["imageFile"]
                title = json.loads(request.form["title"])['title']
                filename = file.filename
                if(filename==""):
                    return "Select a valid file"
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
                    path = app.config["UPLOAD_FOLDER"]
                    hashName = hash_img(path,filename)
                    rm_img(path,filename)
                    conexion = conecta_db("DESart.db")
                    response = registra_art(conexion,hashName,session["user"],session["email"],title)
                    close_db(conexion)
                    return response
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception upload: {} \n".format(e))
        return redirect(url_for("init"))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/sign',methods=['GET','POST'])
def sign():
    try:
        if session["user"]!=None:
            if request.method == 'GET':
                conexion = conecta_db("DESart.db")
                response = consulta_art_sinFirma(conexion,session["user"]).fetchall()
                close_db(conexion)
                return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=2,table=response)
            else:
                if not "hashname" in request.form:
                    return redirect(url_for("sign"))
                else:
                    hashname = request.form['hashname']
                    conexion = conecta_db("DESart.db")
                    response = consulta_art_especifica(conexion,hashname).fetchone()
                    close_db(conexion)
                    return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=3,table=response)
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception sign: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/picture',methods=['POST'])
def picture():
    try:
        if session["user"]!=None:
            if not "hashname" in request.form:
                return redirect(url_for("sign"))
            else:
                hashname = request.form['hashname']
                typeUser = request.form['typeUser']
                if(typeUser=="1"): #Artist
                    conexion = conecta_db("DESart.db")
                    response = modifica_art(conexion,hashname)
                    watermark(app.config["UPLOAD_FOLDER"],hashname,app.config["PREVIEW_FOLDER"])
                    keyname = key_generation(app.config["KEY_FOLDER"],'key')
                    registra_keySinFirma(conexion,keyname,hashname)
                    encrypt_AES(app.config["KEY_FOLDER"],keyname,app.config["UPLOAD_FOLDER"],hashname,app.config["CIPHER_FOLDER"])
                    decrypt_AES(app.config["KEY_FOLDER"],keyname,app.config["CIPHER_FOLDER"],hashname,app.config["DECIPHER_FOLDER"])
                    close_db(conexion)
                    # Falta que el artiste firme la imagen
                    return response
                if(typeUser=="2"): #Client
                    artist = request.form['user']
                    conexion = conecta_db("DESart.db")
                    response = crea_precontrato(conexion,hashname,artist,session["user"])
                    close_db(conexion)
                    # Falta que el cliente firme la imagen
                    return response
                if(typeUser=="3"): #Public Notary
                    # Falta que el notario publico firme la imagen
                    dataJson = json.loads(request.form['dataJson'])
                    conexion = conecta_db("DESart.db")
                    response = modifica_precontrato(conexion,dataJson['idPreCont'])
                    response = crea_contrato(conexion,dataJson)
                    close_db(conexion)
                    return response
                    # return "Signed contract"
                return "Error - TypeUser"
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception picture: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/contracts',methods=['GET'])
def contracts():
    try:
        if session["user"]!=None:
            if(session["typeUser"] == 1): #Artis
                conexion = conecta_db("DESart.db")
                response = consulta_contratos(conexion,session["user"],"Artist")
                close_db(conexion)
                return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=5,table=response)
            if(session["typeUser"] == 2): #Client
                conexion = conecta_db("DESart.db")
                response = consulta_contratos(conexion,session["user"],"Client")
                close_db(conexion)
                return render_template('client_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=2,table=response)
            if(session["typeUser"] == 3): #Public notary
                conexion = conecta_db("DESart.db")
                response = consulta_contratos(conexion,session["user"],"Notary")
                close_db(conexion)
                return render_template('notary_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=2,table=response)
    except Exception as e:
        print("\n *** Exception contracts: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/contracts/<certificate>',methods=['GET'])
def certificate(certificate):
    # Mostrar el Certificado en PDF
    return certificate

@app.route('/artPublic',methods=['GET'])
def public():
    try:
        if session["user"]!=None:
            if session["typeUser"]==1: #Artist
                conexion = conecta_db("DESart.db")
                resulset = consulta_art_conFirma(conexion,session["user"]).fetchall()
                response = list_public_art(resulset)
                close_db(conexion)
                return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=4,table=response)
            if session["typeUser"]==2: #Client
                conexion = conecta_db("DESart.db")
                resulset = consulta_art_conFirma_public(conexion).fetchall()
                response = list_public_art(resulset)
                close_db(conexion)
                return render_template('client_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=0,table=response)
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception public: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/buyArt',methods=['POST'])
def buy():
    try:
        if (session["user"]!=None) and (session["typeUser"]==2):       
            hashname = request.form['hashname']
            conexion = conecta_db("DESart.db")
            response = consulta_art_especifica(conexion,hashname).fetchone()
            close_db(conexion)
            return render_template('client_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=1,table=response)     
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception buy art: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/signContracts',methods=['GET','POST'])
def signContracts():
    try:
        if session["user"]!=None:
            if request.method == 'GET':
                conexion = conecta_db("DESart.db")
                response = consulta_precontratos_NOfirmados(conexion)
                close_db(conexion)
                return render_template('notary_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=1,table=response)
            else:
                if not "idContract" in request.form:
                    return redirect(url_for("sign"))
                else:
                    idPreCon = request.form['idContract']
                    conexion = conecta_db("DESart.db")
                    response = consulta_precontrato_especi(conexion,idPreCon)
                    close_db(conexion)
                    return render_template('notary_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],user=session["user"],email=session["email"],opc=11,table=response)
        else:
            return redirect(url_for("init"))
    except Exception as e:
        print("\n *** Exception signContracts: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/verify',methods=['POST'])
def verify():
    try:
        if session["user"]!=None:
            idContract = request.form['idContract']
            conexion = conecta_db("DESart.db")
            response = consulta_contrato_porID(conexion,idContract)
            close_db(conexion)
            if(session["typeUser"] == 1): #Artis
                return render_template('artist_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=6,table=response)
            if(session["typeUser"] == 2): #Client
                return render_template('client_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=3,table=response)
            if(session["typeUser"] == 3): #Public notary
                return render_template('notary_index.html',nombre=session["name"],gen=session["gender"],typeUser=session["typeUser"],opc=3,table=response)
    except Exception as e:
        print("\n *** Exception contracts: {} \n".format(e))
        return redirect(url_for("init"))

@app.route('/CheckSigns',methods=['GET','POST'])
def CheckSigns():
    if not "imageFile" in request.files:
        return "No file part in the form."
    file = request.files["imageFile"]
    idContrac = json.loads(request.form["title"])['title']
    filename = file.filename
    if(filename==""):
        return "Select a valid file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["VERIFY_FOLDER"],filename))
        # Comprobar firma digital de los tres actores
        return "Digital signatures match"


def init_db():
    conexion = conecta_db("DESart.db")
    crea_tbs(conexion)
    close_db(conexion)
    print(" * Data Base Status: Ok")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=80,debug=True)