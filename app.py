from flask import Flask, render_template
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template('principal.html')

@app.route("/header.html", methods=['GET'])
def header():
    return render_template('header.html')

@app.route("/footer.html", methods=['GET'])
def footer():
    return render_template('footer.html')

@app.route("/login", methods=['GET'])
def login():
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

@app.route("/vistaImg.html", methods=['GET'])
def vistaImg():
    return render_template('vistaImg.html')