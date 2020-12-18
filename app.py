import os
from flask import Flask, render_template, flash, request, redirect, url_for #para que flask funciones
from werkzeug.utils import secure_filename
import re #expresiones regulares
import yagmail #correos electronicos
import random #generador seudoaleatorio
from flask_sqlalchemy import SQLAlchemy #base de datos (es la libreria SQLalchemy de python totalmente compatible con flask)
from funciones import * #importa el archivo funciones.py donde puse toda las funciones que no estan aqui :)
from datetime import date

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = 'static/images/imgUsuarios'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artemisia.db' #esta linea pone la base de datos en el mismo directorio que app.py, y la crea como una base de datos SQLite v3
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #devuelve un objeto con los manejadores de la base de datos (crea la conexion con la db configurada arriba)

yag = yagmail.SMTP('minticprueba1234@gmail.com', 'prueba1234')

#modelos de la base de datos
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	contrasena = db.Column(db.String(200), nullable=False)
	nombre = db.Column(db.String(200), nullable=False)
	apellido = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	celular = db.Column(db.String(20), nullable=False)
	profesion = db.Column(db.String(100), nullable=True)
	fecha_nacimiento = db.Column(db.String(20), nullable=True)
	user_active = db.Column(db.Boolean, nullable=False)
	user_admin = db.Column(db.Boolean, nullable=False)
	images = db.relationship('Image', backref='user', lazy=True)
	def __repr__(self):
		return '<User %r>' % self.username


class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(200), nullable=False)
	tags = db.Column(db.String(200), nullable=False)
	descripcion = db.Column(db.String(200), nullable=False)
	estado = db.Column(db.Boolean, nullable=False)
	ruta = db.Column(db.String(250), nullable=False)
	binary = db.Column(db.Binary, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return '<Image %r>' % self.titulo
		
#rutas y sus funciones


db.create_all()


@app.route("/", methods=['POST','GET'])
def index():
    return render_template('principal.html')


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
        print(request.method)
        if request.method == 'POST':
            username = request.form['usuario']
            password = request.form['password']
        else:
            username = request.args.get['usuario']
            password = request.args.get['password']

        if(validar_login(username, password)):
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

            if(passwd == passco):
                m = re.search('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', passwd)
                if(m != None ):
                    r = re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', emailv)
                    if( r != None):
                        insertar_usuario_facil(db, username, {'contrasena':passwd, 'apellido':apellido, 'nombre':nombre, 'email':emailv, 'celular':telefono, 'profesion':profesion, 'fecha_nacimiento':fecha, 'user_active':True, 'user_admin':True})
                        flash("registro correcto!")
                        return render_template('principal.html')
                    else:
                        flash("El correo no es correcto")
                        return render_template('registro.html')
                else:
                    flash("La contraseña no cumple con los requisitos exigidos")
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
            tags = str(request.form['tags'])
            descripcion = str(request.form['descripcion'])
            option = bool(request.form['estado'])

            # obtenemos el archivo del input "archivo"
            f = request.files['archivo']
            filename = secure_filename(f.filename)
            filename = str(random.randint(100000, 1000000))+'-image-'+str(date.today())+'-'+filename
            bytesVar = f.read()
            # Guardamos el archivo en el directorio "Archivos PDF"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ruta = app.config['UPLOAD_FOLDER']+'/'+filename
            # Retornamos una respuesta satisfactoria
            insertar_imagen_facil(db, titulo, {'tags':tags, 'descripcion':descripcion, 'estado':option, 'ruta':ruta, 'user_id':'1', 'binary':bytesVar})
            flash("GUARDADA")
            return render_template('subirImg.html')
        except Exception as e:
            print(e)
            flash(str(e))
            return render_template('subirImg.html')

@app.route("/verImagen", methods=['GET'])
def vistaImg(titulo='Esto es un titulo de prueba', descripcion = 'Vacaciones en la playa con mi familia y amigos, celebramos año nuevo con muchos fuegos artificiales. Una de las mejores experiencias en mi vida.'):
    return render_template('vistaImg.html', titulo=titulo, descripcion=descripcion)

