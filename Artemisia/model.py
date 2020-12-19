from flask_sqlalchemy import SQLAlchemy #base de datos (es la libreria SQLalchemy de python totalmente compatible con flask)
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash #hashes criptograficamente seguros
from Artemisia import Class
from Artemisia import Generic
from Artemisia import db

class Database:
    def __init__(self):
        self.database = db
        self.z = 0
    
class Validations:
    MINIMAL_PASSWORD_SIZE=8
    MINIMAL_USERNAME_SIZE=2
    MINIMAL_CELLPHONE_SIZE=7

    def __init__(self):
        self.x=0



