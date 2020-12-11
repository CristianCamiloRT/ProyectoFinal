from flask import Flask, render_template, flash, request, redirect, url_for
import re
import yagmail

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

@app.route("/recuperarContra", methods=['POST','GET'])
def recuperarContra():
    if (request.method == 'GET'):
        return render_template('recuperarContra.html')
    elif (request.method == 'POST'):
        try:
            correo = None
            correo = request.form['emailRecuperar']

            if(correo != None):

                r = re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', correo)
                if( r != None):
                    flash("Token enviado")
                    return render_template('recuperarContra.html')
                else:
                    flash("Correo no valido")
                    return render_template('recuperarContra.html')
            else:
                flash("Correo vacio")
                return render_template('recuperarContra.html')
        except Exception as e:
            print(e)
            flash("Error en el envio de token")
            return render_template('recuperarContra.html')







    
    # yagmail.SMTP('minticprueba1234@gmail.com', 'Prueba1234')

    # contents = [
    #     "This is the body, and here is just text http://somedomain/image.png",
    #     "You can find an audio file attached.", '/local/path/to/song.mp3'
    # ]
    # yag.send('to@someone.com', 'subject', contents)




@app.route("/registro", methods=['POST','GET'])
def registro():
    if (request.method == 'GET'):
        return render_template('registro.html')
    elif (request.method == 'POST'):
        try:
            passwd = str(request.form.get('passWd'))
            passco = str(request.form.get('passConf'))
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
                flash("Las contraseñas no coinciden ")
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
