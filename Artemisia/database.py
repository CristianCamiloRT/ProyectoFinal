from flask_sqlalchemy import SQLAlchemy #base de datos (es la libreria SQLalchemy de python totalmente compatible con flask)
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash #hashes criptograficamente seguros
from Artemisia import Class
from Artemisia import Generic
from Artemisia import db
from Artemisia.Class import *
from Artemisia.Generic import *

def fakeobj():
    return 'dummy obj'

def search_user_register_info(**kwargs):
    if len(kwargs)!=0 and( kwargs.get('id')!=None or kwargs.get('username')!=None or kwargs.get('email')!=None):
        for k,v in kwargs.items():
            if not verify(**{k:v}):
                flash(f'Parametro {k} con formato inválido')
                return None
            for i in ['id','username','email']:
                if kwargs.get(i)!=None:
                    return User.query.filter_by(**{i:v}).first()
    else:
        flash('No se ingresó un parámetro valido de busqueda...')
        return None

def search_user_params(**kwargs):
    data=None
    if len(kwargs)!=0 and( kwargs.get('id')!=None or kwargs.get('username')!=None or kwargs.get('email')!=None):
        type_lookup=None
        res_lookup=None
        for k,v in kwargs.items():
            if not verify(**{k:v}):
                return None
        for i in ['id','username','email']:
            if kwargs.get(i)!=None:
                res_lookup=kwargs.get(i)
                type_lookup=i
                data=User.query.filter_by(**{i:v}).first()
        if data==None:
            flash(f'No existe un usuario con el parametro {type_lookup} : {res_lookup} ingresado')
            return None
        if data!=None and kwargs.get('search')!=None:
            res = dict()
            for e in kwargs.get('search'): 
                if e in ['id','username','email','nombre','apellido','telefono','profesion','fecha_nacimiento','user_active','user_admin']:
                   return getattr(data,e)
        else:
            flash(f'No hay parametro a buscar...')
            return None
    else:
        return None

def add_user(Usuario,Contraseña,Email,Celular,**kwargs):
    state=True
    U=User()
    if verify(username=Usuario,email=Email,password=Contraseña,celular=Celular):
        if User.query.filter_by(username=Usuario).first()!=None:
            flash("Usuario ya registrado, elige otro usuario por favor.")
            state=False
        else:
            U.username=Usuario
        if User.query.filter_by(email=Email).first()!=None:
            flash("Email ya registrado, elige otro email por favor.")
            state=False
        else:
            U.email=Email
        U.contrasena=generate_password_hash(Contraseña)
        U.celular=Celular
    else:
        state=False
    for k,v in kwargs.items():
            if k in ['nombre','apellido','profesion','fecha_nacimiento']:
                if verify(**{k:v}):
                    setattr(U,k,v)
                else:
                    state=False
    if state:
        db.session.add(U)
        db.session.commit()
    return state
 

def delete_user(*args,**kwargs):
    a=None
    state=False
    try:
        if len(kwargs)>0:
            for k,v in kwargs.items():
                if k=='id':
                    a = User.query.get(v)
                    state=True
        elif len(args)>0:	
            a = User.query.filter_by(username=args[0]).first()
            state=True
        if state==True:
            db.session.delete(a)
            db.session.commit()	
            return True
    except Exception as e:
        print(e.message)
        return False

def modify_user(**kwargs):
    data=None
    if len(kwargs)!=0 and( kwargs.get('id')!=None or kwargs.get('username')!=None or kwargs.get('email')!=None):
        type_lookup=None
        res_lookup=None
        for k,v in kwargs.items():
            if not verify(**{k:v}):
                flash(f'Formato del dato {k}:{v} erroneo')
                return None
        for i in ['id','username','email']:
            if kwargs.get(i)!=None:
                res_lookup=kwargs.get(i)
                type_lookup=i
                data=User.query.filter_by(**{i:v}).first()
        if data==None:
            flash(f'No existe un usuario en el sistema con los parametros {type_lookup} : {res_lookup}')
        if data!=None and kwargs.get('modify')!=None:
            for e in kwargs.get('modify'):
                if e[0] in ['id','username','email','nombre','apellido','telefono','profesion','fecha_nacimiento','user_active','user_admin']:
                   return setattr(data,e[0],e[1])
                else:
                    flash(f'No hay parametro a buscar, usuario inexistente')
                    return None
            else:
                return None

def modify_user(*args,**kwargs):
    state=False
    a=None
    if len(kwargs)>0 and len(args)==0:
        for k,v in kwargs.items():
            if k=='id':
                a = User.query.get(v)
                state = (a!=None)
    elif len(args)>0:	
        a = User.query.filter_by(username=args[0]).first()
        state=(a!=None)

    if state==True:
        for k,v in kwargs.items():
            if k=='username' and verify(username=v):
                a.username=v
            if k=='contraseña' and verify(contraseña=v):
                a.contraseña=generate_password_hash(v)
            if k=='nombre' and verify(nombre=v):
                a.nombre=v
            if k=='apellido' and verify(apellido=v):
                a.apellido=v
            if k=='email' and verify(email=v):
                a.email=v
            if k=='celular' and verify(celular=v):
                a.celular=v
            if k=='fecha_nacimiento' and verify(fecha_nacimiento=v):
                a.fecha_nacimiento=v
            if k=='user_active':
                a.user_active=bool(v)
            if k=='user_admin':
                a.user_admin=bool(v)
        db.session.commit()	
        return True
      
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
    
#def check_login(user,password):
#    U=User.query.filter_by(username=user).first()
#    if verify(username=user,contraseña=password):
#        if check_password_hash(U.contraseña,password):
#            return True
#    return False