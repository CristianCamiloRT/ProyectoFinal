MINIMAL_PASSWORD_SIZE=8
MINIMAL_USERNAME_SIZE=2
MINIMAL_CELLPHONE_SIZE=7

import re
int_pattern=re.compile("^[0-9]+$")
num_pattern=re.compile("^[+]?[0-9]+$")
email_pattern=re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
usr_pattern=re.compile("^\w+$")
nam_pattern=re.compile("^[a-zA-Z]+$")
pw_pattern=re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")
fecha_pattern=re.compile("^[-./\:?AMP \d]*$")

from flask import flash

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
    if len(str(a))==0:
        return True
    if a==None and name!=None:
        logic=False
        flash("Nombre invalido, no es alfanumérico el campo",category='err-nam') 
    return logic

def verify_last_name(last_name):
    a=re.match(nam_pattern,last_name)
    logic=True
    if len(str(a))==0:
        return True
    if a==None and last_name!=None:
        logic=False
        flash("Apellido invalido, no es alfanumérico el campo",category='err-la-nam') 
    return logic


def verify_fecha_nacimiento(fecha):
    a=re.match(fecha_pattern,fecha)
    logic=True
    if a==None and fecha!=None:
        logic=False
        flash("Formato de fecha invalido",category='err-date')
    return logic

def verify_profesion(profesion):
    a=re.match(usr_pattern,profesion)
    logic=True
    if len(str(a))==0:
        return True
    if a==None and profesion!=None:
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
        if k=="celular":
            state = state and verify_cellphone(v)
        if k=='profesion':
            state = state and verify_profesion(v)
        if k=='fecha_nacimiento':
            state = state and verify_fecha_nacimiento(v)
        if k=='id':
            state = state and verify_id(v)
    return state