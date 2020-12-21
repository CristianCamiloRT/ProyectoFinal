from flask_wtf import FlaskForm
from Artemisia.Generic import *
from flask_wtf import file
from wtforms import StringField
from wtforms import TextField 
from wtforms.validators import *
from wtforms import BooleanField

class RegisterForm(FlaskForm):
    username=StringField('Nombre de Usuario',validators=[DataRequired(),Regexp(usr_pattern,message="El usuario no puede contener simbolos. "),Length(min=MINIMAL_USERNAME_SIZE,message="La longitud debe ser mayor. ")])
    password = StringField('Contraseña',validators=[DataRequired("Es obligatorio asignar una contraseña a la cuenta. "),Regexp(pw_pattern,message="Contraseña no válida. ")])
    password_conf = StringField('Confirmar contraseña',validators=[DataRequired("Es obligatorio repetir una contraseña valida. "),Regexp(pw_pattern,message="Contraseña no válida. "),EqualTo('password',"Las contraseñas no coinciden. ")])
    email = StringField('Email',validators=[DataRequired("El correo es un campo obligatorio. "),Regexp(email_pattern,message="El correo no posee formato válido. ")])
    cellphone = StringField('Celular',validators=[DataRequired("El celular es un campo obligatorio"),Regexp(num_pattern,message="El correo solo debe contener numeros. "),Length(min=7,message=f"El numero de telefono no alcanza la longitud minima {MINIMAL_CELLPHONE_SIZE}. ")])
    name = StringField('Nombre', validators=[Optional(),Regexp(nam_pattern,message="El nombre debe contener unicamente letras. ")])
    last_name = StringField('Apellido', validators=[Optional(),Regexp(nam_pattern,message="El apellido debe contener unicamente letras. ")])
    profesion = StringField('Profesion',validators=[Optional(),Regexp(nam_pattern,message="La profesion debe contener unicamente letras. ")])
    date = StringField('Fecha de nacimiento',validators=[Optional(),Regexp(fecha_pattern,message="El formato de fecha no es valido. ")])