from Artemisia import app,db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	contrasena = db.Column(db.String(200), nullable=False)
	nombre = db.Column(db.String(200), nullable=False)
	apellido = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	celular = db.Column(db.String(20), nullable=False)
	profesion = db.Column(db.String(100), nullable=True)
	fecha_nacimiento = db.Column(db.String(20), nullable=True)
	user_active = db.Column(db.Boolean, nullable=False)
	user_admin = db.Column(db.Boolean, nullable=False)
	images = db.relationship('Image', backref='user', lazy=True)
	def __repr__(self):
		return '<User %r>' % self.username

class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String(200), nullable=False)
	tags = db.Column(db.String(200), nullable=False)
	descripcion = db.Column(db.String(200), nullable=False)
	estado = db.Column(db.Boolean, nullable=False)
	ruta = db.Column(db.String(250), nullable=False)
	binary = db.Column(db.Binary, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	def __repr__(self):
		return '<Image %r>' % self.titulo