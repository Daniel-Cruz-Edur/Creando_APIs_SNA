from flask import Flask, render_template, redirect, request, url_for,flash, session,jsonify, send_file
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
@app.route('/Lista_De_Personas')
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
        print(Password_Now_Encripted)
        #insertar datos a la tabla personas

        cursor.execute("Insert Into personas_info (Nombre_Persona, Apellido_Persona, Apodo_Persona, Password_Persona, Email_Persona, Adress_Persona, Phone_Persona, Rol_Persona) Values (%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (Nombres, Apellidos, Nickname, Password_Now_Encripted, E_Mail, Adress, Phone, User_Rol))
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

    
@app.route('/', methods=['GET', 'POST'])
def Login_User():
    
    if request.method == 'POST':
        
        #Verificar las credenciales del usuario
        Username_Login = request.form.get('Users_Login'); #'User's_Login'
        Password_Login = request.form.get('Users_Password'); #'User's_Password'
        
        cursor = db.cursor()
        Query = "SELECT Apodo_Persona, Password_Persona, Rol_Persona FROM personas_info WHERE Apodo_Persona = %s"
        cursor.execute(Query, (Username_Login,))
        Users = cursor.fetchone()
        
        if Users is None:
            error = 'El usuario no está registrado.'
            print ("El usuario no está registrado. ");
            return render_template ('Login.html', Error=error)
        
        print(Users)
        Password_Uncripted = check_password_hash(Users[1], Password_Login) 
        print(Password_Uncripted)
        
        if Users is not None and check_password_hash(Users[1], Password_Login):

            session['User'] = Username_Login
            session['Type_User'] = Users[2]
            
            if Users[2] == 'Administrador':
                
                return redirect(url_for('Lista_Registros'));
            
            else:
                
                return redirect(url_for('Listando_Las_Canciones'));

        else:
            
            print("Las credenciales ingresadas son invalidas. ");
            Error = 'Credenciales invalidas. Intentelo nuevamente. EROOR OUT BREAK';
            return render_template ('Login.html', Error = Error);
            
    return render_template('Login.html')

@app.route('/Logout')
def Logout():
    
    session.pop('User', None)
    
    print("Sesión eliminada")
    return redirect(url_for('Login_User'))

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
        
        cursor.execute("Insert Into songs (Title_Song, Artist_Song, Gender_Song, Price_Song, Duration_Song, Relase_Date_Song, Cover_Song) Values (%s, %s, %s, %s, %s, %s, %s)", 
                        (Song_Title, Artist_Name, Song_Gender, Song_Price, Song_Duration, Date_Relase, Transformacion_De_Imagen))
        db.commit()
        flash('Cancion guardada correctamente.', 'Sucess!')
        
        print(Transformacion_De_Imagen)
        
        print("Metodo POST")
        
        #redirigimos a la misma pagina cuando el metodo es POST
        return redirect(url_for('Registrando_Las_Canciones'))
    
    #Con get lo envio al doc
    return render_template('Log_Songs_Page.html')

@app.route('/Lista_De_Canciones')
def Listando_Las_Canciones():

    cursor = db.cursor();
    cursor.execute("SELECT ID_Song, Title_Song, Artist_Song, Gender_Song, Price_Song, Duration_Song, Relase_Date_Song, Cover_Song FROM songs")
    Guardado_Datos_Songs = cursor.fetchall()
    
    print("Listando las canciones. ")

    if Guardado_Datos_Songs:

        List_Songs = []

        for Song in Guardado_Datos_Songs:
        
            Image = base64.b64encode(Song[7]).decode('utf-8')
            List_Songs.append({
                'ID_Song': Song[0],
                'Titulo': Song[1],
                'Artista': Song[2],
                'Genero': Song[3],
                'Precio': Song[4],
                'Duracion': Song[5],
                'Lanzamiento': Song[6],
                'Imagen': Image
            })
        return render_template('Songs_List.html', Lista_De_Canciones = List_Songs)    
    
    else:
        
        print("Canciones no registradas. ");
        return "Canciones no registradas. "
    
    #return render_template('Songs_List.html', Lista_De_Canciones = List_Songs)

@app.route('/Editar_Canciones/<int:id>', methods = ['GET','POST'])
def Editar_Cancion(id):
    cursor = db.cursor()
    if request.method == 'POST':
        Title_Song_Modify = request.form.get('Title_Song')
        Artist_Song_Modify = request.form.get('Artist_Song')
        Gender_Song_Modify = request.form.get('Gender_Song')
        Price_Song_Modify = request.form.get('Price_Song')
        Duration_Song_Modify = request.form.get('Duration_Song')
        Relase_Date_Song_Modify = request.form.get('Relase_Date_Song')
        Cover_Song_Modify = request.files['Cover_Song_Update']

        Transformacion_De_Imagen = Cover_Song_Modify.read()

    #sentencia para actualizar los datos
        Update_Data = "UPDATE songs set Title_Song = %s, Artist_Song = %s, Gender_Song = %s, Price_Song = %s, Duration_Song = %s, Relase_Date_Song = %s, Cover_Song = %s Where ID_Song = %s"
        cursor.execute(Update_Data,(Title_Song_Modify, Artist_Song_Modify, Gender_Song_Modify, Price_Song_Modify, Duration_Song_Modify, Relase_Date_Song_Modify, Transformacion_De_Imagen,id))
        db.commit()

        return redirect(url_for('Listando_Las_Canciones'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM songs WHERE ID_Song = %s', (id,))
        data = cursor.fetchall()

        return render_template('Editar_Songs.html', songs = data[0]) #Este personas corresponde al schema

@app.route('/Eliminar_Canciones/<int:id>', methods=['GET'])
def Eliminar_Cancion(id):
    
    cursor = db.cursor();
    cursor.execute('DELETE FROM Songs WHERE ID_Song = %s', (id,))
    db.commit()
    return redirect(url_for('Listando_Las_Canciones'))

@app.route('/Agregar_Al_Carrito', methods = ['POST'])
def Add_To_Cart():
    
    print('Oh, estás en el carrito. ')
    
    
    ID_Song_Py= request.form['ID_Song_LA']
    Title_Song_Py = request.form['Titulo_Song_LA']
    Price_Song_Py = request.form['Precio_Song_LA']

    if 'Cart' not in session:
        session['Cart'] = []
        
    session['Cart'].append({'Id_Song':ID_Song_Py, 'Titulo_Song': Title_Song_Py, 'Precio_Song': float (Price_Song_Py)})
    session.modified = True
    
    #print ('Contenido del carro es:' + session['Cart'])
    
    return jsonify({'message': 'Canción agregada correctamente al carrito. '})
    
@app.route('/Mostrar_El_Carrito', methods = ['GET','POST'])
def Show_Cart():
    
    carro = session.get('Cart',[])
    total = sum(item['Precio_Song'] for item in carro)    
    print ('Hello World...');
    return render_template('Carrito.html', carro=carro, total=total)

@app.route('/Borrar_El_Carrito', methods=['GET','POST'])
def Delete_Cart():
    
    session['Cart'] = []
    session.modified = True
    
@app.route('/Borrar_Item_Carrito', methods=['GET','POST'])
def Delete_Item_Cart():

    return redirect(url_for('Show_Cart'))
#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=Lista_Registros)
    app.run(debug=True, port=5005)
    
#att Yudy uwu