from flask import Flask, render_template, flash, request, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
            error = "Usuario o contraseña incorrecto"
            print(error)
            flash(error)  
            return render_template('login.html')        
    except Exception as e:
        print(e)
        return render_template('login.html')
    return render_template('login.html')

@app.route("/recuperarContraseña", methods=['GET'])
def recuperarContra():
    return render_template('recuperarContra.html')

@app.route("/registro", methods=['GET'])
def registro():
    return render_template('registro.html')


@app.route("/subirImagen", methods=['GET'])
def subirImg():
    return render_template('subirImg.html')

@app.route("/verImagen", methods=['GET'])
def vistaImg(titulo='Esto es un titulo de prueba', descripcion = 'Vacaciones en la playa con mi familia y amigos, celebramos año nuevo con muchos fuegos artificiales. Una de las mejores experiencias en mi vida.'):
    return render_template('vistaImg.html', titulo=titulo, descripcion=descripcion)