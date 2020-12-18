from flask_sqlalchemy import SQLAlchemy #base de datos (es la libreria SQLalchemy de python totalmente compatible con flask)
from sqlalchemy import and_ 
from werkzeug.security import generate_password_hash, check_password_hash #hashes criptograficamente seguros
from flask import session

def insertar_usuario(link, us, co, no, ap, em, ce, pr, fe, uact, uadm): #inserta un usuario params(el_objeto_db, username, nombre, ..., user_admin)
	try:
		from app import User
		if co != None:
			co =  generate_password_hash(co)
		newUser = User(username = us, contrasena = co, nombre = no, apellido = ap,  email = em, celular = ce, profesion = pr, fecha_nacimiento = fe, user_active = uact, user_admin = uadm)
		link.session.add(newUser)   
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True
	
def insertar_usuario_facil(link, username1, otros):#inserta un usuario params(el_objeto_db, username, un_diccionario_con_los_otros_params)
	try:
		from app import User
		usuario = User(username = username1)
		for key, value in otros.items():
			if (key == 'contrasena' and (value != None)):
				passwd = generate_password_hash(value)
				usuario.contrasena = passwd
			if (key == 'nombre' and (value != None)):
				usuario.nombre = value
			if (key == 'apellido' and (value != None)):
				usuario.apellido = value
			if (key == 'email' and (value != None)):
				usuario.email = value
			if (key == 'celular' and (value != None)):
				usuario.celular = value
			if (key == 'profesion' and (value != None)):
				usuario.profesion = value
			if (key == 'fecha_nacimiento' and (value != None)):
				usuario.fecha_nacimiento = value
			if (key == 'user_active' and (value != None)):
				usuario.user_active = value
			if (key == 'user_admin' and (value != None)):
				usuario.user_admin = value
		link.session.add(usuario)   
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True

def eliminar_usuario(link, id1): #eliminar usuario params(el_objeto_db, el_id_a_eliminar)
	try:
		from app import User
		who = User.query.get(id1)
		link.session.delete(who)
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True
	
def modificar_usuario(link, id1, pars): #update usuario params(el_objeto_db, el_id, un_diccionario_con_los_otros_params_a_modificar)
	try:
		from app import User
		usuario = User.query.get(id1)
		for key, value in pars.items():
			if (key == 'username' and (value != None)):
				usuario.username = value
			if (key == 'contrasena' and (value != None)):
				passwd = generate_password_hash(value)
				usuario.contrasena = passwd
			if (key == 'nombre' and (value != None)):
				usuario.nombre = value
			if (key == 'apellido' and (value != None)):
				usuario.apellido = value
			if (key == 'email' and (value != None)):
				usuario.email = value
			if (key == 'celular' and (value != None)):
				usuario.celular = value
			if (key == 'profesion' and (value != None)):
				usuario.profesion = value
			if (key == 'fecha_nacimiento' and (value != None)):
				usuario.fecha_nacimiento = value
			if (key == 'user_active' and (value != None)):
				usuario.user_active = value
			if (key == 'user_admin' and (value != None)):
				usuario.user_admin = value	
		link.session.commit()
	except AssertionError as error:
		print(error)
		return False
	return True
			
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
	
def validar_login(username1, passwd):
	try: 
		from app import User
		usuario = User.query.filter_by(username=username1).first()
		if usuario != None:
			if check_password_hash(usuario.contrasena, passwd):
				session["id"]=usuario.id
				session["username"]=usuario.username
				session["admin"]=usuario.user_admin
				session["correo"]=usuario.email	
				return True
	except:
		return False
	return False

def obtenerImagenes():
	try: 
		from app import Image
		imagenes = Image.query.filter_by(estado=1).all()
		# imagenes = Image.query.count()
		if imagenes != None:
				return imagenes
	except Exception as e:
		return str(e)
	return False

def obtenerMisImagenes():
	try: 
		from app import Image
		imagenes = Image.query.filter_by(user_id=session["id"]).all()
		# imagenes = Image.query.count()
		if imagenes != None:
				return imagenes
	except Exception as e:
		return str(e)
	return False

def obtenerPorId(idGet):
	try: 
		from app import Image
		imagenes = Image.query.filter_by(id=idGet).all()
		# imagenes = Image.query.count()
		if imagenes != None:
				return imagenes
	except Exception as e:
		return str(e)
	return False

def buscarImagenes(tag):
	try: 
		from app import Image
		search = "%{}%".format(tag)
		imagenes = Image.query.filter(and_(Image.tags.like(search),Image.estado==1)).all()
		if imagenes != None:
			return imagenes
	except Exception as e:
		return str(e)
	return False
	