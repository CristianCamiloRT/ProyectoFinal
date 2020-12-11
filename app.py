from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
    return render_template('principal.html')


@app.route("/header.html", methods=['GET'])
def header():
    return render_template('header.html')

@app.route("/footer.html", methods=['GET'])
def footer():
    return render_template('footer.html')

@app.route("/login", methods=['POST','GET'])
def login():
    try:
        error = None
        print(request.method)
        if request.method == 'POST':
            username = request.form['usuario']
            password = request.form['password']
        else:
            username = request.args.get['usuario']
            password = request.args.get['password']

        if(username == "Prueba" and password == "Prueba123"):
            return redirect('/')
        else:
            if(username == None and password == None): 
                error = "Escriba usuario y contraseña"
                flash(error)
                return render_template('login.html')
            else:
                error = "Usuario o contraseña incorrecto"
                flash(error)
                return render_template('login.html')     
    except:
        return render_template('login.html')
    return render_template('login.html')

@app.route("/recuperarContraseña", methods=['GET'])
def recuperarContra():
    return render_template('recuperarContra.html')

@app.route("/registro", methods=['POST','GET'])
def registro():
    if (request.method == 'GET'):
        return render_template('registro.html')
    elif (request.method == 'POST'):
        try:
            passwd = request.form.get('passWd')
            passco = request.form.get('passConf')
            emailv = str(request.form.get('emailv'))

            if(passwd == passco):
                m = re.search('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$', passwd)
                if(m != None ):
                    r = re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', emailv)
                    if( r != None):
                        flash("registro correcto!")
                        return render_template('principal.html')
                    else:
                        flash("El correo no es correcto")
                        return render_template('registro.html')
                else:
                    flash("La contraseña no cumple con los requisitos exigidos")
                    return render_template('registro.html')
            else:
                flash("Las contraseñas no coinciden")
                return render_template('registro.html')
        except:
            flash("Error en el registro")
            return render_template('registro.html')


@app.route("/subirImagen", methods=['GET'])
def subirImg():
    return render_template('subirImg.html')

@app.route("/verImagen", methods=['GET'])
def vistaImg(titulo='Esto es un titulo de prueba', descripcion = 'Vacaciones en la playa con mi familia y amigos, celebramos año nuevo con muchos fuegos artificiales. Una de las mejores experiencias en mi vida.'):
    return render_template('vistaImg.html', titulo=titulo, descripcion=descripcion)
