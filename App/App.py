from flask import *

app = Flask(__name__)
   
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/Registrar') #lo del parantesis (sin las comillas) poner en la barra de busqueda
def Registro():
    return render_template('registrar.html')

@app.route('/Saludo') #lo del parantesis (sin las comillas) poner en la barra de busqueda
def Saludo():
    return "Hala, buenos días"


#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)