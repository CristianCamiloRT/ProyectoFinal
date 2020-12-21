from Artemisia import app,db

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
	images = db.relationship('Image', backref='user', lazy=True)

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
	
	def __repr__(self):
		return '<Image %r>' % self.titulo

class Filesystem(db.Model):
	file_dir =db.Column(db.Integer, nullable=True)
	dir=db.Column(db.String(255),primary_key=True)