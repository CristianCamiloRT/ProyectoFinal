MINIMAL_PASSWORD_SIZE=8
MINIMAL_USERNAME_SIZE=2
MINIMAL_CELLPHONE_SIZE=7

import re
int_pattern=re.compile("^[0-9]+$")
num_pattern=re.compile("^[+]?[0-9]+$")
email_pattern=re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
usr_pattern=re.compile("^\w+$")
nam_pattern=re.compile("^(?![\s]+$)[a-zA-Z\s]*$")
pw_pattern=re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")
fecha_pattern=re.compile("^[-./\:?AMP \d]*$")
title_img_pattern=re.compile("^(?![\s]+$)[a-zA-Z\s]*$")
tag_img_pattern=re.compile("^(?![\s,]+$)[a-zA-Z\s,]*$")
token_pattern=re.compile("^[0-9]{6}$")
from flask import flash
import datetime

#err-id
def verify_id(id):
    a=re.match(int_pattern,id)
    logic=True
    if a==None:
        logic=False
        flash("Id invalido, no es un entero. No es admitido...",category='err-id')
    return logic 

def verify_name(name):
    a=re.match(nam_pattern,name)
    logic=True
    if len(str(name))==0:
        return True
    if a==None and name!=None:
        logic=False
        flash("Nombre invalido, no es alfanumérico el campo",category='err-nam') 
    return logic

def verify_last_name(last_name):
    a=re.match(nam_pattern,last_name)
    logic=True
    if len(str(last_name))==0:
        return True
    if a==None and last_name!=None:
        logic=False
        flash("Apellido invalido, no es alfanumérico el campo",category='err-la-nam') 
    return logic

def verify_birth_date(fecha):
    a=re.match(fecha_pattern,fecha)
    logic=True
    if a==None and fecha!=None:
        logic=False
        flash("Formato de fecha invalido",category='err-date')
    return logic

def verify_profession(profesion):
    a=re.match(usr_pattern,profesion)
    logic=True
    if len(str(profesion))==0:
        return True
    if a==None and (profesion!=None or profesion!=""):
        logic=False
        flash("Profesión invalida, no es alfanumérico el campo",category='err-prof') 
    return logic

def verify_cellphone(cellphone):
    logic=True
    a=re.match(num_pattern,cellphone)
    if(a==None):
        logic=False
        flash("No es un número de telefono válido, no está compuesto por números")
    if(len(str(cellphone))<MINIMAL_CELLPHONE_SIZE):
        flash(f"No es un número de telefono válido, tiene menos de {MINIMAL_CELLPHONE_SIZE} dígitos",category='err-cellphone')
        logic=False
    return logic

def verify_email(email):
    a=re.match(email_pattern,email)
    if a==None:
        flash("No posee formato de correo válido",category='err-email')
        return False
    return True

def verify_username(username):
    a=re.match(usr_pattern,username)
    logic=True
    if a==None:
        logic=False
        flash("Usuario invalido, no es alfanumérico",category='err-usr')
    if len(str(username))< MINIMAL_USERNAME_SIZE:
        logic=False
        flash(f"Longitud de usuario menor a {MINIMAL_USERNAME_SIZE}",category='err-usr')     
    return logic

def verify_password(password):
    logic=True
    a=re.match(pw_pattern,password)
    if len(str(password))<MINIMAL_PASSWORD_SIZE:
        logic=False
        flash(f"Contraseña de longitud: {len(str(password))} longitud minima aceptable: {MINIMAL_PASSWORD_SIZE}",category="err-pw")
    if a==None:
        logic=False
        flash("La contraseña no cumple con el formato establecido",category='err-pw')
    return logic

def verify(**kwargs):
    state=True
    for k,v in kwargs.items():
        if k=="password":
            state = state and verify_password(v)
        if k=="username":
            state = state and verify_username(v)
        if k=="email":
            state = state and verify_email(v)
        if k=="cellphone":
            state = state and verify_cellphone(v)
        if k=='profession':
            state = state and verify_profession(v)
        if k=='birth_date':
            state = state and verify_birth_date(v)
        if k=='id':
            state = state and verify_id(v)
    return state

def img_verify_title(title):
    if title!=None:
        if re.match(title_img_pattern,title):
            return True
        return False
    return False

def img_verify_tags(tags):
    if tags!=None:
        if re.match(tag_img_pattern,tags):
            return True
        return False
    return False

def img_verify(data,flag="title"):
    state=True
    if flag=='title':
        state = state and img_verify_title(data)
    if flag=='tags':
        state = state and img_verify_tags(data)
    return state

def add_time(timestamp,seconds,minutes=0,hours=0,days=0):
    datetime.datetime=()