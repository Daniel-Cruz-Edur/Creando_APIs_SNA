from flask import Flask, render_template, redirect, request, url_for,flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Dani_Server';
   
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "",
    database = "personas"
)
   
cursor =  db.cursor()
   
@app.route('/')
def Lista_Registros():
    
    cursor = db.cursor();
    cursor.execute('SELECT * FROM personas_info');
    Guardado_Datos_Personas =  cursor.fetchall();
    
    return render_template('index.html', personas = Guardado_Datos_Personas);



@app.route('/Registrar', methods=['GET','POST']) #lo del parantesis (sin las comillas) poner en la barra de busqueda
def Registro():
    
    if request.method == 'POST':
    
        Nombres = request.form.get('User_Name')
        Apellidos = request.form.get('User_Lastname')
        Nickname = request.form.get('User_Nickname')
        Password = request.form.get('User_Password')
        E_Mail = request.form.get('User_Email')
        Adress = request.form.get('User_Adress')
        Phone = request.form.get('User_Adress')
    
        cursor.execute("Insert Into personas_info (Nombre_Persona, Apellido_Persona, Apodo_Persona, Password_Persona, Email_Persona, Adress_Persona, Phone_Persona) Values (%s, %s, %s, %s, %s, %s, %s)", (Nombres, Apellidos, Nickname, Password, E_Mail, Adress, Phone))
        db.commit()
        flash('Usuario creado correctamente.', 'Sucess!');
        #redirigimos a la misma pagina cuando el metodo es POST
        return redirect(url_for('Registro'))
    
    #Con get lo envio al doc
    return render_template('registrar.html')

@app.route('/Saludo') #lo del parantesis (sin las comillas) poner en la barra de busqueda
def Saludo():
    return "Hala, buenos días"


#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=Lista_Registros)
    app.run(debug=True, port=5005)