from flask_sqlalchemy import SQLAlchemy #base de datos (es la libreria SQLalchemy de python totalmente compatible con flask)
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash #hashes criptograficamente seguros
from Artemisia import Class
from Artemisia import Generic
from Artemisia import db

def search_user_info(**kwargs):
	data=None
	if len(kwargs)!=0 and( kwargs.get('id')!=None or kwargs.get('username')!=None or kwargs.get('email')!=None):
		if kwargs.get('id')!=None:
			if verify(id=kwargs.get('id')):
				data = User.query.get(kwargs.get('id'))
			else:
				return None
		elif kwargs.get('username')!=None:
			if verify(username=kwargs.get('username')):
				data = User.query.filter_by(username=kwargs.get('username')).first()
			else:
				return None
		elif kwargs.get('email')!=None:
			if verify(email=kwargs.get('email')):
				data = User.query.filter_by(email=kwargs.get('email')).first()
			else:
				return None
		else:
			flash('Error indefinido, contactar al administrador E0000')
			return None
	
		if data!=None and kwargs.get('search')!=None:
			a=kwargs.get('search')
		else:
			flash(f'No hay parametro de busqueda, usuario existente')
			return None
	else:
		return None


def add_user(Usuario,Contraseña,Email,**kwargs):
	state=True
	U=User()
	if verify(usuario=Usuario,email=Email,contraseña=Contraseña):
		if User.query.filter_by(username=Usuario).first()==None:
			flash("Usuario ya registrado, elige otro usuario por favor.")
			state=False
		else:
			U.username=Usuario
		if User.query.filter_by(email=Email).first()==None:
			flash("Email ya registrado, elige otro email por favor.")
			state=False
		else:
			U.email=Email
		U.contraseña=generate_password_hash(Contraseña)
	for k,v in kwargs.items():
		if k=='telefono':
			if verify(telefono=v):
				U.telefono=v
		if k=='profesion':
			if verify(profesion=v):
				U.profesion=v
		if k=='fecha_nacimiento':
			if verify(fecha_nacimiento=v):
				U.fecha_nacimiento=v
		U.user_active=True
		U.user_admin=False

		try:
			db.session.add(U)
			db.session.commit()
		except Exception as e:
			print(e.message)

	return state

def delete_user(*args,**kwargs):
	a=None
	state=False
	try:
		if len(kwargs)>0:
			for k,v in kwargs.items():
				if k=='id':
					a = User.query.get(v)
					state=True
		elif len(args)>0:	
			a = User.query.filter_by(username=args[0]).first()
			state=True
		if state==True:
			db.session.delete(a)
			db.session.commit()	
			return True
	except Exception as e:
		print(e.message)
		return False
	
def modify_user(*args,**kwargs):
	state=False
	a=None
	try:
		if len(kwargs)>0 and len(args)==0:
			for k,v in kwargs.items():
				if k=='id':
					a = User.query.get(v)
					state = (a!=None)
		elif len(args)>0:	
			a = User.query.filter_by(username=args[0]).first()
			state=(a!=None)

		if state==True:
			for k,v in kwargs.items():
				if k=='username' and verify(username=v):
					a.username=v
				if k=='contraseña' and verify(contraseña=v):
					a.contraseña=generate_password_hash(v)
				if k=='nombre' and verify(nombre=v):
					a.nombre=v
				if k=='apellido' and verify(apellido=v):
					a.apellido=v
				if k=='email' and verify(email=v):
					a.email=v
				if k=='celular' and verify(celular=v):
					a.celular=v
				if k=='fecha_nacimiento' and verify(fecha_nacimiento=v):
					a.fecha_nacimiento=v
				if k=='user_active':
					a.user_active=bool(v)
				if k=='user_admin':
					a.user_admin=bool(v)
			db.session.commit()	
			return True
			
def add_img(**kwargs):
	


def insertar_imagen(link, titulo1, tags1, descripcion1, estado1, ruta1, user_id1): #inserta imagen params(objeto_db, titulo, tags, ..., clave_foranea_usuario) 
	try:
		from app import Image
		newImg = User(titulo = titulo1, tags = tags1, descripcion = descripcion1, estado = estado1, ruta = ruta1, user_id = user_id1)
		link.session.add(newUser)   
		link.session.commit()
	except AssertionError as error:
		print(error)
	return True
	
def insertar_imagen_facil(link, titulo1, otros): #inserta iamgen params(el_objeto_db, el_titulo, un_diccionario_con_los_otros_params)
	try:
		from app import Image
		img = Image(titulo = titulo1)
		for key, value in otros.items():
			if (key == 'tags' and (value != None)):
				img.tags = value
			if (key == 'descripcion' and (value != None)):
				img.descripcion = value
			if (key == 'estado' and (value != None)):
				img.estado = value
			if (key == 'ruta' and (value != None)):
				img.ruta = value
			if (key == 'user_id' and (value != None)):
				img.user_id = value
			if (key == 'binary' and (value != None)):
				img.binary = value
		link.session.add(img)   
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True

def eliminar_imagen(link, id1): #eliminar imagen params(el_objeto_db, el_id_a_eliminar)
	try:
		from app import Image
		who = Image.query.get(id1)
		link.session.delete(who)
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True
	
def modificar_imagen(link, id1, otros):
	try:
		from app import Image
		img = Image.query.get(id1)
		for key, value in otros.items():
			if (key == 'tags' and (value != None)):
				img.tags = value
			if (key == 'descripcion' and (value != None)):
				img.descripcion = value
			if (key == 'estado' and (value != None)):
				img.estado = value
			if (key == 'ruta' and (value != None)):
				img.ruta = value
			if (key == 'user_id' and (value != None)):
				img.user_id = value
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True
	
def check_login(user,password):
	U=User.query.filter_by(username=user).first()
	if verify(username=user,contraseña=password):
		if check_password_hash(U.contraseña,password):
			return True
	return False