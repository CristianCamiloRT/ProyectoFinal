import os
from flask_sqlalchemy import SQLAlchemy #base de datos (es la libreria SQLalchemy de python totalmente compatible con flask)
from sqlalchemy import and_, or_
from flask import flash, session,render_template
from werkzeug.security import generate_password_hash, check_password_hash #hashes criptograficamente seguros
from Artemisia import Class
from Artemisia import Generic
from Artemisia import app,db,yag
from Artemisia.Class import *
from Artemisia.Generic import *
import secrets
import datetime
from datetime import datetime , timedelta


def add_user(Usuario,Contraseña,Email,Celular,**kwargs):
    state=True
    U=User()
    if verify(username=Usuario,email=Email,password=Contraseña,cellphone=Celular):
        if User.query.filter_by(username=Usuario).first()!=None:
            flash("Usuario ya registrado, elige otro usuario por favor.")
            state=False
        else:
            U.username=Usuario.lower()
        if User.query.filter_by(email=Email).first()!=None:
            flash("Email ya registrado, elige otro email por favor.")
            state=False
        else:
            U.email=Email.lower()
        U.password=generate_password_hash(Contraseña)
        U.cellphone=Celular
    else:
        state=False
    for k,v in kwargs.items():
            if k in ['name','last_name','profession','birth_date']:
                if verify(**{k:v}):
                    setattr(U,k,v)
                else:
                    state=False
    if state:
        db.session.add(U)
        db.session.commit()
    return state

def lower_fix(param):
    return str(param).lower()

def get_user_id(data,flag='username'):
    if flag=='username':
        a=User.query.filter_by(username=data).first()
        if a!=None:
            return User.query.filter_by(username=data).first().id
        return None
    if flag=='email':
        a=User.query.filter_by(email=data).first()
        if a!=None:
            return User.query.filter_by(email=data).first().id
        return None
    if flag=='id':
        return data
    return None

def send_recovery_email(email,info):
    contents=render_template("RecoverT.html",token=info)
    yag.send(email, 'Recuperar contraseña', contents)
    flash("Token enviado (Puede llegar a tu carpeta de spam)")

def generate_token(data,flag='username'):
    a=100000+secrets.randbelow(899999)
    entry=search_entry(data,flag)
    if entry!=None:
        send_recovery_email(entry.email,a)
        entry.event_type="PASSWUP"
        entry.event_description="Intento de recuperación de contraseña"
        entry.event_value=generate_password_hash(str(a))
        entry.event_init=datetime.now()
        entry.event_end=datetime.now() + timedelta(minutes=10)
        db.session.commit()
        

def delete_user(data,flag='username'):
    a=None
    state=False
    if len(data)>0:
        a=User.query.get(get_user_id(data,flag))
        state=True
    if state==True:
        db.session.delete(a)
        db.session.commit()	
        return True
    return state

def check_login(user,password):
    U=User.query.filter_by(username=user.lower()).first()
    if verify(username=user,password=password):
        if check_password_hash(U.password,password):
            return True
    flash("Usuario o contraseña erroneo",category="login")
    return False

def search_entry(data,flag='username'):
    id=get_user_id(data,flag)
    if id!=None:
        return User.query.get(id)
    return None

def get_user_param(data,flag='username',param_to_search='username'):
    if param_to_search in ['name','id','last_name','birth_date','cellphone','profession','password','username','email','user_active','user_admin']:
        db_info=search_entry(data,flag)
        return getattr(db_info,param_to_search)
    else:
        return None

def modify_user_param(data,flag='username',param_to_modify=None,new_value=None):
    if param_to_modify in ['name','id','last_name','birth_date','cellphone','profession','password','username','email','user_active','user_admin']:
        db_info=search_entry(data,flag)
        if db_info!=None and new_value!=None and verify(**{param_to_modify:new_value}):
            if param_to_modify in ['username','email']:
                lower(new_value)
            setattr(db_info,param_to_modify,new_value)
            db.session.update(db_info)
            db.session,commit()
            return True
        return False
    return False

def save_file(file):
    return False

def get_by_img_id(id):
    return Image.query.get(id)

def get_usr_img():
    if 'username' in session:
        return Image.query.filter(Image.user_id==session['username']).all()
    else:
       return []

def get_all_img():
    if 'username' in session:
        return Image.query.filter(or_(Image.public==1,and_(Image.user_id==session['username'] , Image.public==0))).all()
    return Image.query.filter(Image.public==1).all()

def get_img(data, flag=None):
    if flag!=None and flag in ['user_id','binary','path','ext','name', 'public','description','tags','title','id']:
        return Image.query.filter_by(**{flag:data}).all()

def add_img(title,tags,binary,description,public,user_id):
    state=True
    a=Image()
    if img_verify(title):
        a.title=title
    else:
        state=False
    if img_verify(tags,"tags"):
        a.tags=tags
    else:
        state=False
    a.binary=binary.read()
    a.description=description
    a.public=bool(public)
    a.user_id=user_id
    a.ext=os.path.splitext(binary.filename)[1]
    a.name=os.path.splitext(binary.filename)[0]
    a.path=a.name+a.ext
    a.user_id=user_id
    if state:
        db.session.add(a)
        db.session.commit()
    return state

def search_img(tag):
    if 'username' in session:
        return Image.query.filter(and_(Image.tags.like(f"%{tag}%"), or_(Image.public == 1,and_(Image.user_id==session['username'],Image.public==0)))).all()
    return Image.query.filter(and_(Image.tags.like(f"%{tag}%"),Image.public == 1)).all()



#def add_img(**kwargs):
#def insertar_imagen(link, titulo1, tags1, descripcion1, estado1, ruta1, user_id1): #inserta imagen params(objeto_db, titulo, tags, ..., clave_foranea_usuario) 
#    try:
#        from app import Image
#        newImg = User(titulo = titulo1, tags = tags1, descripcion = descripcion1, estado = estado1, ruta = ruta1, user_id = user_id1)
#        link.session.add(newUser)   
#        link.session.commit()
#    except AssertionError as error:
#        print(error)
#    return True
    
#def insertar_imagen_facil(link, titulo1, otros): #inserta iamgen params(el_objeto_db, el_titulo, un_diccionario_con_los_otros_params)
#    try:
#        from app import Image
#        img = Image(titulo = titulo1)
#        for key, value in otros.items():
#            if (key == 'tags' and (value != None)):
#                img.tags = value
#            if (key == 'descripcion' and (value != None)):
#                img.descripcion = value
#            if (key == 'estado' and (value != None)):
#                img.estado = value
#            if (key == 'ruta' and (value != None)):
#                img.ruta = value
#            if (key == 'user_id' and (value != None)):
#                img.user_id = value
#            if (key == 'binary' and (value != None)):
#                img.binary = value
#        link.session.add(img)   
#        link.session.commit()
#    except AssertionError as error:
#        print(error)
#        return False
#    return True

#def eliminar_imagen(link, id1): #eliminar imagen params(el_objeto_db, el_id_a_eliminar)
#    try:
#        from app import Image
#        who = Image.query.get(id1)
#        link.session.delete(who)
#        link.session.commit()
#    except AssertionError as error:
#        print(error)
#        return False
#    return True
    
#def modificar_imagen(link, id1, otros):
#    try:
#        from app import Image
#        img = Image.query.get(id1)
#        for key, value in otros.items():
#            if (key == 'tags' and (value != None)):
#                img.tags = value
#            if (key == 'descripcion' and (value != None)):
#                img.descripcion = value
#            if (key == 'estado' and (value != None)):
#                img.estado = value
#            if (key == 'ruta' and (value != None)):
#                img.ruta = value
#            if (key == 'user_id' and (value != None)):
#                img.user_id = value
#        link.session.commit()
#    except AssertionError as error:
#        print(error)
#        return False
#    return True