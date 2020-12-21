"""
The flask application package.
"""
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import yagmail
yag = yagmail.SMTP('minticprueba1234@gmail.com', 'prueba1234')

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artemisia.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #devuelve un objeto con los manejadores de la base de datos (crea la conexion con la db configurada arriba)

import Artemisia.views
import Artemisia.Class
import Artemisia.database
