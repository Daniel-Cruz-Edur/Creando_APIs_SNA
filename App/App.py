from flask import Flask, render_template, redirect, request, url_for,flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
#import bcrypt

app = Flask(__name__)
app.secret_key = 'Dani_Server';
   
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "",
    database = "personas"
)
   
cursor =  db.cursor()

@app.route('/Password/<Encript_Password>')
def Encriptacion_Password(Encript_Password):
    
    #Generamos un has de la contraseña
    #Encriptar = bcrypt.hashpw(Encript_Password.encode('utf-8'), bcrypt.gensalt());
    Encriptar = generate_password_hash(Encript_Password)
    Value_Check = check_password_hash(Encriptar, Encript_Password)
    return "Encriptado: {0} | coincide: {1}".format(Encriptar, Value_Check)
    
@app.route('/Login', methods=['GET', 'POST'])
def Login_User():
    
    if request.method == 'POST':
        
        #Verificar las credenciales del usuario
        Username = request.form.get('Users_Login'); #'User's_Login'
        Password = request.form.get('Users_Password'); #'User's_Password'
        
        cursor = db.cursor();
        cursor.execute("SELECT Apodo_Persona, Password_Persona FROM persona_info Where Apodo_Persona = %s", (Username,))
        Users = cursor.fetchone();
        
        if Users or Encriptacion_Password(Password) == Users[1]:
            session['User'] = Username;
            return redirect(url_for('Lista_Registros'))
 
        else:
            Error = 'Credenciales invalidas. Intentelo nuevamente.';      
            return render_template('Login.html', Error);

    return render_template('Login.html')

#Definir rutas
@app.route('/')
def Lista_Registros():
    
    cursor = db.cursor();
    cursor.execute('SELECT * FROM persona_info');
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
        Phone = request.form.get('User_Phone')

        Password_Now_Encripted = Encriptacion_Password(Password)
        
        #insertar datos a la tabla personas
    
        cursor.execute("Insert Into persona_info (Nombre_Persona, Apellido_Persona, Apodo_Persona, Password_Persona, Email_Persona, Adress_Persona, Phone_Persona) Values (%s, %s, %s, %s, %s, %s, %s)", (Nombres, Apellidos, Nickname, Password_Now_Encripted, E_Mail, Adress, Phone))
        db.commit()
        flash('Usuario creado correctamente.', 'Sucess!')
        
        
        #redirigimos a la misma pagina cuando el metodo es POST
        return redirect(url_for('Registro'))
    
    #Con get lo envio al doc
    return render_template('registrar.html')

@app.route('/Editar/<int:id>', methods = ['GET','POST'])
def Editar_Usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        Nombres_Modify = request.form.get('nombrepersona')
        Apellidos_Modify = request.form.get('apellidopersona')
        Password_Modify = request.form.get('contraseñapersona')
        Email_Modify = request.form.get('emailpersona')
        Adress_Modify = request.form.get('direccionpersona')
        Phone_Modify = request.form.get('telefonopersona')

    #sentencia para actualizar los datos
        Update_Data = "UPDATE persona_info set Nombre_Persona = %s, Apellido_Persona = %s, Password_Persona = %s, Email_Persona = %s, Adress_Persona = %s, Phone_Persona = %s Where ID_Persona = %s"
        cursor.execute(Update_Data,(Nombres_Modify, Apellidos_Modify, Password_Modify, Email_Modify, Adress_Modify, Phone_Modify, id))
        db.commit()

        return redirect(url_for('Lista_Registros'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM persona_info WHERE ID_Persona = %s', (id,))
        data = cursor.fetchall()

        return render_template('Editar.html', personas = data[0]) #Este personas corresponde al schema

@app.route('/Eliminar/<int:id>', methods=['GET'])
def Eliminar_Usuario(id):
    
    cursor = db.cursor();
    cursor.execute('DELETE FROM persona_info WHERE ID_Persona = %s', (id,))
    db.commit()
    return redirect(url_for('Lista_Registros'))


#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=Lista_Registros)
    app.run(debug=True, port=5005)