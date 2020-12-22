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
        images = get_all_img()
        return render_template('principal.html', images=images, target='db')
    elif (request.method == 'POST'):
        tag = str(request.form['tag'])
        images = search_img(tag)
        return render_template('principal.html', images=images, target='db')

@app.route("/misImagenes", methods=['POST','GET'])
def misImagenes():
    mis_imagenes = get_usr_img()
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
    a=LoginForm()
    if(session!=None):
        session.pop("id",None)
        session.pop("username",None)
        session.pop("admin",None)
        session.pop("correo",None)
    if request.method == 'POST':
        if a.is_submitted():
            if check_login(a.username.data,a.password.data):
                var=search_entry(a.username.data)
                session['username']=var.username
                session['user_id']=var.id
                session['email']=var.email
                session['user_admin']=var.user_admin
                flash("¡Has accedido correctamente!")
                return redirect("/")
            else:
                return render_template('/login.html', form=a)
        else:
            return render_template('/login.html', form=a)
    elif request.method == 'GET':
        return render_template('/login.html',form=a)
@app.route("/contralang",methods=['POST','GET'])
def recuperarContraend():
    t=0
    if 'recovery-timmer' in session:
        t=session['recovery-timmer']
    b=PasswordResetForm()
    if (request.method == 'POST'):

        if b.validate_on_submit():
            if b.password.data==b.password_conf.data:
                if verify_password(b.password.data):
                    if 'recovery-email' in session:
                        z=search_entry(session['recovery-email'],"email")
                        if z!=None:
                            if check_password_hash(z.event_value,b.recovery_token.data):
                                z.password=generate_password_hash(b.password.data)
                                db.session.commit()
                                flash("Cambio de contraseña exitoso")
                                return redirect("/login")
                            else:
                                flash("Token incorrecto")
                                return render_template('RecoverToken.html',form_b=b,timer=t)
                    elif 'recovery-usr' in session:
                        z=search_entry(session['recovery-usr'])
                        if z!=None:
                            if check_password_hash(z.event_value,z.b.recovery_token.data):
                                z.password=generate_password_hash(b.password.data)
                                db.session.commit()
                                flash("Cambio de contraseña exitoso")
                                return redirect("/login")
                            else:
                                flash("Token incorrecto")
                                return render_template('RecoverToken.html',form_b=b,timer=t)
        return render_template('RecoverToken.html',form_b=b,timer=t)
    elif (request.method == 'GET'):
        return render_template('RecoverToken.html',form_b=b,timer=t)

@app.route("/recuperarContra", methods=['POST','GET'])
def recuperarContra():
    a=PasswordRecoveryForm()
    if (request.method == 'POST'):
        if a.validate_on_submit():
            if a.email.data!=None or a.username.data!=None:
                if a.email.data!=None and a.email.data!="":
                    if verify_email(a.email.data):
                        k=search_entry(a.email.data,"email")
                        if k==None:
                            flash("Este usuario no existe en el sistema")
                            return render_template('recuperarContra.html',form_a=a)
                        else:
                            session['recovery-email']=a.email.data
                            generate_token(a.email.data)
                            session['recovery-timmer']=k.event_end
                            return redirect("contralang")
                elif verify_username(a.username.data):
                    k=search_entry(a.username.data)
                    if k==None:
                        flash("Este usuario no existe en el sistema")
                        return render_template('recuperarContra.html',form_a=a)
                    else:
                        session['recovery-usr']=a.username.data
                        generate_token(a.username.data)
                        session['recovery-timmer']=k.event_end
                        return redirect("contralang")
                else:
                    flash("El usuario o el correo están escritos en un formato invalido")
                    return render_template('recuperarContra.html',form_a=a) 
            else:
                flash("Debes escribir al menos uno de los dos campos para enviar el token al correo...")
                return render_template('recuperarContra.html',form_a=a) 
    elif (request.method == 'GET'):
        return render_template('recuperarContra.html',form_a=a)
        
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