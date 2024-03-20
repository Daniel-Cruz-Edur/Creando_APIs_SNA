from flask import Flask, render_template, redirect, request, url_for,flash, session
import mysql.connector, base64
from werkzeug.security import generate_password_hash, check_password_hash
#import bcrypt

app = Flask(__name__)
app.secret_key = 'Dani_Server';

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "",
    database = "usuarios"
)

cursor =  db.cursor()

#Definir rutas
@app.route('/')
def Lista_Registros():
    
    cursor = db.cursor();
    cursor.execute('SELECT * FROM personas_info');
    Guardado_Datos_Personas = cursor.fetchall();
    
    return render_template('index.html', Mi_Base_De_Datos = Guardado_Datos_Personas);
    
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
        User_Rol = request.form.get('User_Rol')
        
        Password_Now_Encripted = generate_password_hash(Password)
        
        #insertar datos a la tabla personas

        cursor.execute("Insert Into personas_info (Nombre_Persona, Apellido_Persona, Apodo_Persona, Password_Persona, Email_Persona, Adress_Persona, Phone_Persona, Rol_Persona) Values (%s, %s, %s, %s, %s, %s, %s)", 
                        (Nombres, Apellidos, Nickname, Password_Now_Encripted, E_Mail, Adress, Phone, User_Rol))
        db.commit()
        flash('Usuario creado correctamente.', 'Sucess!')
        
        
        #redirigimos a la misma pagina cuando el metodo es POST
        return redirect(url_for('Registro'))
    
    #Con get lo envio al doc
    return render_template('registrar.html')

@app.route('/Password/<Encript_Password>')
def Encriptacion_Password(Encript_Password):
    
    #Generamos un has de la contraseña
    #Encriptar = bcrypt.hashpw(Encript_Password.encode('utf-8'), bcrypt.gensalt());
    
    Encriptar = generate_password_hash(Encript_Password)
    Value_Check = check_password_hash(Encriptar, Encript_Password)
    
    #return "Encriptado: {0} | coincide: {1}".format(Encriptar, Value_Check)
    return Value_Check;

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
        User_Rol_Modify = request.form.get('User_Rol_Edit')

    #sentencia para actualizar los datos
        Update_Data = "UPDATE personas_info set Nombre_Persona = %s, Apellido_Persona = %s, Password_Persona = %s, Email_Persona = %s, Adress_Persona = %s, Phone_Persona = %s, Rol_Persona = %s Where ID_Persona = %s"
        cursor.execute(Update_Data,(Nombres_Modify, Apellidos_Modify, Password_Modify, Email_Modify, Adress_Modify, Phone_Modify, User_Rol_Modify,id))
        db.commit()

        return redirect(url_for('Lista_Registros'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas_info WHERE ID_Persona = %s', (id,))
        data = cursor.fetchall()

        return render_template('Editar.html', personas = data[0]) #Este personas corresponde al schema

@app.route('/Eliminar/<int:id>', methods=['GET'])
def Eliminar_Usuario(id):
    
    cursor = db.cursor();
    cursor.execute('DELETE FROM personas_info WHERE ID_Persona = %s', (id,))
    db.commit()
    return redirect(url_for('Lista_Registros'))

    
@app.route('/Login', methods=['GET', 'POST'])
def Login_User():
    
    if request.method == 'POST':
        
        #Verificar las credenciales del usuario
        Username_Login = request.form.get('Users_Login'); #'User's_Login'
        Password_Login = request.form.get('Users_Password'); #'User's_Password'
        
        cursor = db.cursor();
        SQL = "SELECT Apodo_Persona, Password_Persona, Rol_Persona FROM personas_info Where Apodo_Persona = %s";
        cursor.execute(SQL, (Username_Login))
        Users = cursor.fetchone();
        
        if Users and check_password_hash(Users['Password_Persona'], Password_Login):

            session['User'] = Users['Apodo_Persona'];
            session['Type_User'] = Users['Rol_Persona'];
            
            if Users['Type_User'] == 'Administrador':
                
                return redirect(url_for('Lista_Registros'));
            
            else:
                
                return redirect(url_for('Lista_De_Canciones'));
        
        else:
            
            print("Las credenciales, ingresadas son invalidas. ");
            Error = 'Credenciales invalidas. Intentelo nuevamente. ';
            return render_template ('Login.html', Error = Error);
            
    return render_template('Login.html')

@app.route('/Logout')
def Logout():
    
    session.pop('User', None)
    
    print("Sesión eliminada")
    return redirect/url_for(('Login_User'))

# Desde quí realizo las rutos pertinentes para las conciones
# 1) Registro
# 2) Actualización
# 3) Eliminación
# 4) Lista

@app.route('/Registro_De_Canciones', methods=['GET', 'POST'])
def Registrando_Las_Canciones():
    
    if request.method == 'POST':
    
        print("Hola acá esta creando la ruta de registro de canciones")
        
        Song_Title = request.form.get('Songs_Title')
        Artist_Name = request.form.get('Artist_Song')
        Song_Gender = request.form.get('Gender_Song')
        Song_Price = request.form.get('Price_Song')
        Song_Duration = request.form.get('Duration_Song')
        Date_Relase = request.form.get('Relase_Song')
        Song_Cover = request.files['Cover_Song']
        
        Transformacion_De_Imagen = Song_Cover.read()
        
        cursor.execute("Insert Into songs (Title_Song, Artist_Song, Gender_Song, Price_Song, Durantion_Song, Relase_Date_Song, Cover_Song) Values (%s, %s, %s, %s, %s, %s, %s)", 
                        (Song_Title, Artist_Name, Song_Gender, Song_Price, Song_Duration, Date_Relase, Transformacion_De_Imagen))
        db.commit()
        flash('Cancion guardada correctamente.', 'Sucess!')
        
        print(Transformacion_De_Imagen)
        
        print("Metodo POST")
        
        #redirigimos a la misma pagina cuando el metodo es POST
        return redirect(url_for('Listando_Las_Canciones'))
    
    #Con get lo envio al doc
    return render_template('Log_Songs_Page.html')

@app.route('/Lista_De_Canciones')
def Listando_Las_Canciones():

    cursor = db.cursor();
    cursor.execute("SELECT Title_Song, Artist_Song, Gender_Song, Price_Song, Durantion_Song, Relase_Date_Song, Cover_Song FROM songs")
    Guardado_Datos_Songs = cursor.fetchall()
    
    print("Listando las canciones. ")

    if Guardado_Datos_Songs:

        List_Songs = []

        for Song in Guardado_Datos_Songs:
        
            Image = base64.b64encode(Song[6]).decode('utf-8')
            List_Songs.append({
                'Titulo': Song[0],
                'Artista': Song[1],
                'Genero': Song[2],
                'Precio': Song[3],
                'Duracion': Song[4],
                'Lanzamiento': Song[5],
                'Imagen': Image
            })
        return render_template('Songs_List.html', Lista_De_Canciones = List_Songs)    
    
    else:
        
        return print("Canciones no encontradas. ");
    
    #return render_template('Songs_List.html', Lista_De_Canciones = List_Songs)
    
    
#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=Lista_Registros)
    app.run(debug=True, port=5005)
    
