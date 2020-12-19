"""
Routes and views for the flask application.
"""
from flask import render_template, flash, request, redirect, url_for
import os, re, yagmail, random
import Artemisia.database
import Artemisia.Class
from Artemisia.database import *
from Artemisia import app,db

db.create_all()

@app.route("/", methods=['POST','GET'])
def index():
    if (request.method == 'GET'):
        lista_imagenes = fakeobj() #obtenerImagenes()
        return render_template('principal.html', lista_imagenes=lista_imagenes)
    elif (request.method == 'POST'):
        tag = str(request.form['tag'])
        lista_imagenes = buscarImagenes(tag)
        return render_template('principal.html', lista_imagenes=lista_imagenes)

@app.route("/misImagenes", methods=['POST','GET'])
def misImagenes():
    mis_imagenes = obtenerMisImagenes()
    return render_template('misImagenes.html', mis_imagenes=mis_imagenes)

@app.route("/cerrarSesion", methods=['POST','GET'])
def cerrarSesion():
    session.pop("id",None)
    session.pop("username",None)
    session.pop("admin",None)
    session.pop("correo",None)
    return redirect('/')

@app.route("/header.html", methods=['GET'])
def header():
    return render_template('header.html')

@app.route("/footer.html", methods=['GET'])
def footer():
    return render_template('footer.html')

@app.route("/login", methods=['POST','GET'])
def login():
    try:
        error = None
        session.pop("id",None)
        session.pop("username",None)
        session.pop("admin",None)
        session.pop("correo",None)
        print(request.method)
        if request.method == 'POST':
            username = request.form['usuario']
            password = request.form['password']
        else:
            username = request.args.get['usuario']
            password = request.args.get['password']

        if(validar_login(username, password)):
            print(session["id"])
            print(session["username"])
            print(session["admin"])
            print(session["correo"])
            return redirect('/')
        else:
            error = "Usuario o contraseña incorrecto"
            print(error)
            flash(error)  
            return render_template('login.html')        
    except Exception as e:
        print(e)
        return render_template('login.html')
    return render_template('login.html')

@app.route("/recuperarContra", methods=['POST','GET'])
def recuperarContra():
    if (request.method == 'GET'):
        return render_template('recuperarContra.html')
    elif (request.method == 'POST'):
        try:
            correo = None
            token = None
            TokenForm = None
            correo = request.form['emailRecuperar']

            if(correo != None and TokenForm == None):
                r = re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', correo)
                if( r != None):
                    token = str(random.randint(100000, 1000000))
                    contents = [
                        "Acabas de recibir un correo prueba",
                        "El siguiente es tu token: ", token
                    ]
                    yag.send(correo, 'Recuperar contraseña', contents)
                    flash("Token enviado (Puede llegar a tu carpeta de spam)")
                    return render_template('recuperarContra.html')
                else:
                    flash("Correo no valido")
                    return render_template('recuperarContra.html')
            else:
                pass1 = request.form['contra']
                pass2 = request.form['contrac']
                TokenForm = request.form['token']

                if(pass1 == pass2):
                    m = re.search('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', pass1)
                    if(m != None ):
                        if(token == TokenForm):
                            flash("Cambio realizado!")
                            return render_template('principal.html')
                        else:
                            flash("El token no corresponde al enviado")
                            return render_template('recuperarContra.html')
                    else:
                        flash("La contraseña no cumple con los requisitos exigidos")
                        return render_template('recuperarContra.html')
                else:
                    flash("Las contraseñas no coinciden ")
                    return render_template('recuperarContra.html')
        except Exception as e:
            print(e)
            flash("Error en el envio de token")
            return render_template('recuperarContra.html')

@app.route("/registro", methods=['POST','GET'])
def registro():
    if (request.method == 'GET'):
        return render_template('registro.html')
    elif (request.method == 'POST'):
        try:
            passwd = str(request.form['passWd'])
            passco = str(request.form['passConf'])
            emailv = str(request.form['emailv'])
            username = str(request.form['username'])
            nombre = str(request.form['nombre'])
            apellido = str(request.form['apellido'])
            telefono = str(request.form['telefono'])
            profesion = str(request.form['profesion'])
            fecha = str(request.form['fecha'])
            if(passwd==passco):
                if add_user(username,passwd,emailv,telefono,**{'apellido':apellido, 'nombre':nombre, 'profesion':profesion, 'fecha_nacimiento':fecha, 'user_active':True, 'user_admin':False}):
                    flash("registro correcto!")
                    return render_template('principal.html')
                return render_template('registro.html')
            else:
                flash("Las contraseñas no coinciden ")
                return render_template('registro.html')

        except Exception as e:
            print(e)
            se = str(e)
            if(se.startswith("(sqlite3.IntegrityError) UNIQUE constraint failed: user.username")): 
                flash("Error en el registro (Ya existe el nombre de usuario)")
            if(se.startswith("(sqlite3.IntegrityError) UNIQUE constraint failed: user.email")):
                flash("Error en el registro (Correo ya registrado)")
            return render_template('registro.html')


@app.route("/subirImagen", methods=['POST','GET'])
def subirImg():
    if (request.method == 'GET'):
        return render_template('subirImg.html')
    elif (request.method == 'POST'):
        try:
            titulo = str(request.form['titulo'])
            titulo = titulo.upper()
            tags = str(request.form['tags'])
            descripcion = str(request.form['descripcion'])
            descripcion = descripcion.capitalize()
            option = bool(request.form['estado'])

            # obtenemos el archivo del input "archivo"
            f = request.files['archivo']
            filename = f.filename
            filename = str(random.randint(100000, 1000000))+'-image-'+str(date.today())+'-'+filename
            # Guardamos el archivo en el directorio "Archivos PDF"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # bytesVar = f.read()
            ruta = app.config['UPLOAD_FOLDER']+'/'+filename
            # Retornamos una respuesta satisfactoria
            insertar_imagen_facil(db, titulo, {'tags':tags, 'descripcion':descripcion, 'estado':option, 'ruta':ruta, 'user_id':session["id"]})
            flash("GUARDADA")
            return render_template('subirImg.html')
        except Exception as e:
            print(e)
            flash(str(e))
            return render_template('subirImg.html')

@app.route("/verImagen", methods=['GET'])
def vistaImg():
    id = request.args.get('id')
    lista_imagen = obtenerPorId(id)
    return render_template('vistaImg.html', lista_imagen=lista_imagen)
