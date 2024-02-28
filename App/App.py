from flask import * #Flask, render_template
import mysql.connector

app = Flask(__name__)
   
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "",
    database = "personas"
)
   
cursor =  db.cursor()
   
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/Registrar', methods=['POST']) #lo del parantesis (sin las comillas) poner en la barra de busqueda
def Registro():
    Nombres = request.form['User_Name'],
    Apellidos = request.form['User_Lastname'],
    Nickname = request.form['User_Nickname'],
    Password = request.form['User_Password'],
    E_Mail = request.form['User_Email'],
    Adress = request.form['User_Adress'],
    Phone = request.form['User_Adress'],
    
    cursor.execute("Insert Into personas_info (Nombre_Persona, Apellido_Persona, Apodo_Persona, Password_Persona, Email_Persona, Adress_Persona, Phone_Persona) Values (%s, %s, %s, %s, %s, %s, %s)", (Nombres, Apellidos, Nickname, Password, E_Mail, Adress, Phone))
    db.commit()
    
    return redirect(url_for('registrar'))

@app.route('/Saludo') #lo del parantesis (sin las comillas) poner en la barra de busqueda
def Saludo():
    return "Hala, buenos días"


#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True, port=5005)