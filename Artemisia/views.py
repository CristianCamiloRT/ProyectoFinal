"""
Routes and views for the flask application.
"""
from flask import render_template, flash, request, redirect, url_for,session
import os, re, yagmail, random
import Artemisia.database
import Artemisia.Class
import Artemisia.Forms
from Artemisia.database import *
from Artemisia import app,db
from Artemisia.Forms import *

db.create_all()

@app.route("/", methods=['POST','GET'])
def index():
    if (request.method == 'GET'):
        images = get_all_img() #obtenerImagenes()
        return render_template('principal.html', images=images, target='db')
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
    session=None
    a=LoginForm()
    if(session!=None):
        session.pop("id",None)
        session.pop("username",None)
        session.pop("admin",None)
        session.pop("correo",None)
    if request.method == 'POST':
        if a.is_submitted():
            if check_login(a.username.data,a.password.data):
                flash("¡Has accedido correctamente!")
                return redirect("/")
            else:
                return render_template('/login.html', form=a)
        else:  # You only want to print the errors since fail on validate
            #print(a.errors.items())  
            return render_template('/login.html', form=a)
    elif request.method == 'GET':
        return render_template('/login.html',form=a)
    #if(verify_login(username, password)):
    #    print(session["id"])
    #    print(session["username"])
    #    print(session["admin"])
    #    print(session["correo"])
    #    return redirect('/')
    #else:
        #return render_template('login.html',form=a)        
    #return render_template('login.html',form=a)

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
    a = RegisterForm()
    if request.method == 'POST':
       # if a.is_submitted():
       #     print("Form successfully submitted")
        if a.validate_on_submit():
            if add_user(a.username.data,a.password.data,a.email.data,a.cellphone.data,**{'last_name':a.last_name.data,'name':a.name.data, 'profession':a.profesion.data, 'birth_date':a.date.data, 'user_active':True, 'user_admin':False}):
                flash("Registro exitoso, ¡Accede con tus credenciales!",category="login")
                return redirect("/login")
            else:
                return render_template('/registro.html', form=a)
        else:  # You only want to print the errors since fail on validate
            #print(a.errors.items())  
            return render_template('/registro.html', form=a)
    elif request.method == 'GET':
        return render_template('/registro.html',form=a)


@app.route("/subirImagen", methods=['POST','GET'])
def subirImg():
    imf=ImageForm()
    if request.method == 'POST':
        if imf.validate_on_submit():
            if add_img(imf.title.data,imf.tags.data,imf.binary.data,imf.description.data,imf.public.data,"3"):
                flash("Carga de imagen exitosa")
                return render_template('/subirImg.html', form=imf)
            else:
                return render_template('/subirImg.html', form=imf)
        else:  
            return render_template('/subirImg.html', form=imf)
    elif request.method == 'GET':
        return render_template('/subirImg.html',form=imf)
 
@app.route("/verImagen/<int:id>", methods=['GET'])
def vistaImg(id):
    im=[get_by_img_id(id)]
    username=get_user_param(get_by_img_id(id).user_id,flag='id',param_to_search='username')
    return render_template('vistaImg.html', imagen=im,usr=username)

@app.route("/test", methods=['POST','GET'])
def test():
    if request.method == 'GET':
        images=list(get_all_img())

        return render_template('/test.html', images=images, target='db')

@app.route("/img/db/<int:id>")
def im_db(id):
    res=get_by_img_id(id)
    return app.response_class(res.binary,mimetype='application/octet-stream')