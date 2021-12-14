import sqlite3, hashlib, base64, copy
def conecta_db(name):
	return sqlite3.connect(name)

def close_db(conexion):
	conexion.close()

def crea_tbs(conexion):
	cursor_tb = conexion.cursor()
	cursor_tb.execute(
			"""
				create table if not exists credenciales(
					usr text not null primary key,
					psw text not null
				)				
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists tipoUsr(
					idTipoUsr integer not null primary key,
					descrip text not null
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists persona(
					email text not null primary key,
					usr text not null,					
					nom text not null,
					apep text not null,
					apem text not null,
					edad text not null,
					sexo text not null,
					idTipoUsr integer not null,
					foreign key(usr) references credenciales(usr),
					foreign key(idTipoUsr) references tipoUsr(idTipoUsr)
				)
			"""
		)
	cursor_tb.execute(
			"""
				create table if not exists artes(
					hashname text not null primary key,
					usr text not null,
					email text not null,
                    statusFirma text not null,
                    titulo text not null,
					fecha timestamp default current_timestamp,
                    foreign key(usr) references credenciales(usr),
					foreign key(email) references persona(email)
				)
			"""
		)    
	cursor_tb.execute(
			"""
				create table if not exists keySinFirma(
					idKey integer not null primary key autoincrement,
					namekey text not null,
					hashname text not null,
					fecha timestamp default current_timestamp,
					foreign key(hashname) references artes(hashname)
				)
			"""
		)
    
	# Ingresamos los tipos de usuario que tendra el sistema
	llena_cats(conexion,"tipoUsr","idTipoUsr","1",[1,'Artist'],'idTipoUsr,descrip')
	llena_cats(conexion,"tipoUsr","idTipoUsr","2",[2,'Client'],'idTipoUsr,descrip')
	llena_cats(conexion,"tipoUsr","idTipoUsr","3",[3,'Public notary'],'idTipoUsr,descrip')

def llena_cats(conexion,tabla,campo,valor,list_data,columnas):
	cursor_tb = conexion.cursor()
	respuesta = cursor_tb.execute("select * from {} where {}={}".format(tabla,campo,valor))
	existencia = respuesta.fetchone()
	if existencia == None:
		sentencia = "insert into {}({}) values(?,?)".format(tabla,columnas)
		cursor_tb.execute(sentencia,list_data)
		conexion.commit()

def clearDict(dicInfo):
    result = list()
    result.append(dicInfo['email'])
    user = hashlib.sha256(dicInfo['usur'].encode()).hexdigest()
    result.append(user)
    result.append(dicInfo['name'])
    result.append(dicInfo['ape1'])
    result.append(dicInfo['ape2'])
    result.append(dicInfo['age'])
    result.append(dicInfo['gend'])
    result.append(dicInfo['uTyp'])
    pswd = hashlib.sha256(dicInfo['pswd'].encode()).hexdigest()
    result.append(pswd)
    dicInfo.clear()
    return result

def hash_credentials(dicInfo):
    result = list()
    user = hashlib.sha256(dicInfo['usur'].encode()).hexdigest()
    result.append(user)
    pswd = hashlib.sha256(dicInfo['pswd'].encode()).hexdigest()
    result.append(pswd)
    dicInfo.clear()
    return result

def valida_login(conexion,user,pswd):
    mensaje = ""
    cursor_tb = conexion.cursor()
    sentencia = "select count(*) from credenciales where usr='{}' and psw='{}'".format(user,pswd)
    respuesta = cursor_tb.execute(sentencia).fetchone()[0]
    if(respuesta != 0):
        mensaje = "Welcome!"
    else:
        mensaje = "Credentials error"
    return mensaje

def valida_usr(conexion,user):
    mensaje = ""
    cursor_tb = conexion.cursor()
    sentencia = "select count(*) from credenciales where usr='{}'".format(user)
    respuesta = cursor_tb.execute(sentencia).fetchone()[0]
    if(respuesta != 0):
        mensaje = "Usuario existente"
    else:
        mensaje = "Sin existencia"
    return mensaje

def valida_email(conexion,email):
    mensaje = ""
    cursor_tb = conexion.cursor()
    sentencia = "select count(*) from persona where email='{}'".format(email)
    respuesta = cursor_tb.execute(sentencia).fetchone()[0]
    if(respuesta != 0):
        mensaje = "Correo registrado"
    else:
        mensaje = "Sin existencia"
    return mensaje
    
def alta_usr(conexion,dicInfo):
    mensaje = ""
    cursor_tb = conexion.cursor()
    infoToinser = clearDict(dicInfo)
    msj = valida_usr(conexion,infoToinser[1])    
    if(msj=="Usuario existente"):
        mensaje = "There is a person with that Nickname"
    else:
        msj = valida_email(conexion,infoToinser[0])
        if(msj=="Correo registrado"):
            mensaje = "There is a person with that Email"
        else:
            sentencia = "insert into credenciales values(?,?)"
            cursor_tb.execute(sentencia,(infoToinser[1],infoToinser[8]))
            sentencia = "insert into persona values(?,?,?,?,?,?,?,?)"
            cursor_tb.execute(sentencia,(infoToinser[:-1]))
            conexion.commit()
            mensaje = "Registration successful!"
    return mensaje

def consulta_email(conexion,user):
    cursor_tb = conexion.cursor()
    sentencia = "select email from persona where usr='{}'".format(user)
    respuesta = cursor_tb.execute(sentencia).fetchone()
    if(respuesta==None):
        respuesta = "Not found";
        return respuesta
    else:
        return respuesta[0]

def consulta_nombre(conexion,user):
    cursor_tb = conexion.cursor()
    sentencia = "select nom from persona where usr='{}'".format(user)
    respuesta = cursor_tb.execute(sentencia).fetchone()
    if(respuesta==None):
        respuesta = "Not found";
        return respuesta
    else:
        return respuesta[0]

def consulta_tipousr(conexion,user):
    cursor_tb = conexion.cursor()
    sentencia = "select idTipoUsr from persona where usr='{}'".format(user)
    respuesta = cursor_tb.execute(sentencia).fetchone()
    if(respuesta==None):
        respuesta = "Not found";
        return respuesta
    else:
        return respuesta[0]

def consulta_genero(conexion,user):
    cursor_tb = conexion.cursor()
    sentencia = "select sexo from persona where usr='{}'".format(user)
    respuesta = cursor_tb.execute(sentencia).fetchone()
    if(respuesta==None):
        respuesta = "Not found";
        return respuesta
    else:
        return respuesta[0]

def valida_art(conexion,art):
    mensaje = ""
    cursor_tb = conexion.cursor()
    sentencia = "select count(*) from artes where hashname='{}'".format(art)
    respuesta = cursor_tb.execute(sentencia).fetchone()[0]
    if(respuesta != 0):
        mensaje = "Arte existente"
    else:
        mensaje = "Sin existencia"
    return mensaje

def registra_art(conexion,art,user,email,titulo):
    mensaje = ""
    cursor_tb = conexion.cursor()
    msj = valida_art(conexion,art)
    if(msj=="Arte existente"):
        mensaje = "There is a similar art in the system"
    else:
        sentencia = "insert into artes(hashname,usr,email,statusFirma,titulo) values(?,?,?,?,?)"
        cursor_tb.execute(sentencia,(art,user,email,'No',titulo))
        conexion.commit()
        mensaje = "Art stored"
    return mensaje

def consulta_art_sinFirma(conexion,user):
    cursor_tb = conexion.cursor()
    sentencia = "select * from artes where usr='{}' and statusFirma='No' order by fecha desc".format(user)
    respuesta = cursor_tb.execute(sentencia)
    return respuesta

def consulta_art_conFirma(conexion,user):
    cursor_tb = conexion.cursor()
    sentencia = "select * from artes where usr='{}' and statusFirma='Si' order by fecha desc".format(user)
    respuesta = cursor_tb.execute(sentencia)
    return respuesta

def consulta_art_conFirma_public(conexion):
    cursor_tb = conexion.cursor()
    sentencia = "select * from artes where statusFirma='Si' order by fecha desc"
    respuesta = cursor_tb.execute(sentencia)
    return respuesta

def consulta_art_especifica(conexion,art):
    cursor_tb = conexion.cursor()
    sentencia = "select * from artes where hashname='{}'".format(art)
    respuesta = cursor_tb.execute(sentencia)
    return respuesta

def modifica_art(conexion,art):
    cursor_tb = conexion.cursor()
    sentencia = "update artes set statusFirma='Si' where hashname='{}'".format(art)
    cursor_tb.execute(sentencia)
    conexion.commit()
    return "Art signed successful"

def valida_key(conexion,keyname):
    mensaje = ""
    cursor_tb = conexion.cursor()
    sentencia = "select count(*) from keySinFirma where namekey='{}'".format(keyname)
    respuesta = cursor_tb.execute(sentencia).fetchone()[0]
    if(respuesta != 0):
        mensaje = "Key Existente"
    else:
        mensaje = "Sin existencia"
    return mensaje

def registra_keySinFirma(conexion,keyname,hashImg):
    cursor_tb = conexion.cursor()
    mensaje = valida_key(conexion,keyname)
    if(mensaje == "Sin existencia"):
        sentencia = "insert into keySinFirma(namekey,hashname) values(?,?)"
        cursor_tb.execute(sentencia,(keyname,hashImg))
        conexion.commit()

def list_public_art(result_queries):
    rows_for_html = list()
    element_for_row = list()
    counter = 0
    for query in result_queries:
        counter += 1
        element_for_row.append(query)
        if(counter == 3):
            rows_for_html.append(copy.deepcopy(element_for_row))
            element_for_row.clear()
            counter = 0
    if(counter != 0):
        rows_for_html.append(copy.deepcopy(element_for_row))
        element_for_row.clear()
        counter = 0
    return rows_for_html
    # for row in rows_for_html:
    #     print(f"\n Row: \n{row} \n")
        # for element in row:
        #     print(element)
    
    # print(len(rows_for_html))
    # print(rows_for_html)
    

# Test section
# conexion = conecta_db("DESart.db")
# crea_tbs(conexion)
# info = {'usur': 'elias160299', 'pswd': '12345678', 'name': 'Elias', 'ape1': 'Muñoz', 'ape2': 'Primero', 'age': '22', 'gend': '2', 'uTyp': '3', 'email': 'elias160299@hotmail.com'}
# alta_usr(conexion,info)
# consulta_nombre(conexion,'75b3978b7f22dfd20f713d00f8fb2658542c5c4752e163ba21a4e375177a7269')
# print(consulta_art_especifica(conexion,'9c23a9ce1dbdcaf3ad6f6d76f20741c34e3951b1f5d880666cf27b6c9f06e663.png').fetchone())
# print(modifica_art(conexion,'9c23a9ce1dbdcaf3ad6f6d76f20741c34e3951b1f5d880666cf27b6c9f06e663.png'))
# list_public_art(consulta_art_conFirma_public(conexion).fetchall())
# close_db(conexion)