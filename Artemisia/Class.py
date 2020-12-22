from Artemisia import app,db
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)
	name = db.Column(db.String(200), nullable=True)
	last_name = db.Column(db.String(200), nullable=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	cellphone = db.Column(db.String(20), nullable=False)
	profession = db.Column(db.String(100), nullable=True)
	birth_date = db.Column(db.String(20), nullable=True)
	user_active = db.Column(db.Boolean, nullable=False, default=True)
	user_admin = db.Column(db.Boolean, nullable=False, default=False)
	event_init=db.Column(DateTime(timezone=True))
	event_end=db.Column(DateTime(timezone=True))
	event_type=db.Column(db.String(6),nullable=True)
	event_description=db.Column(db.String(200),nullable=True)
	event_value=db.Column(db.String(10),nullable=True)
	images = db.relationship('Image', backref='user', lazy=True)
	user_creation_date=db.Column(DateTime(timezone=True),server_default=func.now())

	def __repr__(self):
		return '<User %r>' % self.username

class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	tags = db.Column(db.String(200), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	public = db.Column(db.Boolean, nullable=False)
	name = db.Column(db.String(100), nullable=False)
	ext =db.Column(db.String(4),nullable=False)
	path =db.Column(db.String(255),nullable=False)
	binary = db.Column(db.Binary, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	upload_date=db.Column(DateTime(timezone=True),server_default=func.now())
	
	def __repr__(self):
		return '<Image %r>' % self.titulo

class Logsystem(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	user_id=db.Column(db.String(200),nullable=False)
	event_date=db.Column(DateTime(timezone=True),server_default=func.now())
	event_description=db.Column(db.String(200),nullable=True)
	event_type=db.Column(db.String(6),nullable=False)