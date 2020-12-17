"""
The flask application package.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yagmail
yag = yagmail.SMTP('minticprueba1234@gmail.com', 'prueba1234')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = 'static/images/imgUsuarios'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artemisia.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #devuelve un objeto con los manejadores de la base de datos (crea la conexion con la db configurada arriba)

import Artemisia.views
import Artemisia.funciones
import Artemisia.Class
