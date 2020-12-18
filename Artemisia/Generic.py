MINIMAL_PASSWORD_SIZE=8
MINIMAL_USERNAME_SIZE=2
MINIMAL_CELLPHONE_SIZE=7

import re
int_pattern=re.compile("^[0-9]+$")
num_pattern=re.compile("^[+]?[0-9]+$")
email_pattern=re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
usr_pattern=re.compile("^\w+$")
pw_pattern=re.compile("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")
fecha_pattern=re.compile("^[-./\:?AMP \d]*$")

from flask import flash

def verify_id(id):
    a=re.match(int_pattern,id)
    logic=True
    if a==None:
        logic=False
        flash("Id invalido, no es un entero. No es admitido...")
    return logic

def verify_fecha_nacimiento(fecha):
    a=re.match(fecha_pattern,fecha)
    logic=True
    if a==None:
        logic=False
        flash("Formato de fecha invalido")
    return logic

def verify_profesion(profesion):
    a=re.match(usr_pattern,profesion)
    logic=True
    if len(str(a))==0:
        return True
    if a==None:
        logic=False
        flash("Profesión invalida, no es alfanumérico el campo") 
    return logic

def verify_cellphone(cellphone):
    logic=True
    a=re.match(num_pattern,cellphone)
    if(a==None):
        logic=False
        flash("No es un número de telefono válido, no está compuesto por números")
    if(len(str(cellphone))<MINIMAL_CELLPHONE_SIZE):
        flash(f"No es un número de telefono válido, tiene menos de {MINIMAL_CELLPHONE_SIZE} dígitos")
        logic=False
    return logic

def verify_email(email):
    a=re.match(email_pattern,email)
    if a==None:
        flash("No posee formato de correo válido")
        return False
    return True

def verify_username(username):
    a=re.match(pw_pattern,username)
    logic=True
    if a==None:
        logic=False
        flash("Usuario invalido, no es alfanumérico")
    if len(str(username))< MINIMAL_USERNAME_SIZE:
        logic=False
        flash(f"Longitud de usuario menor a {MINIMAL_USERNAME_SIZE}")     
    return logic

def verify_password(password):
    logic=True
    a=re.match(pw_pattern,password)
    if len(str(password))<MINIMAL_PASSWORD_SIZE:
        logic=False
        flash(f"Contraseña de longitud: {len(str(password))} longitud minima aceptable: {MINIMAL_PASSWORD_SIZE}",category="error-es")
    if a==None:
        logic=False
        flash("La contraseña no cumple con el formato establecido")
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
        if k=="telefono":
            state = state and verify_cellphone(v)
        if k=='profesion':
            state = state and verify_profesion(v)
        if k=='fecha_nacimiento':
            state = state and verify_fecha_nacimiento(v)
        if k=='id':
            state = state and verify_id(v)
    return state