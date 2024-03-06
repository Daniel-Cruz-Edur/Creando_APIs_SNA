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
        Phone = request.form.get('User_Adress')
    
        #insertar datos a la tabla personas
    
        cursor.execute("Insert Into persona_info (Nombre_Persona, Apellido_Persona, Apodo_Persona, Password_Persona, Email_Persona, Adress_Persona, Phone_Persona) Values (%s, %s, %s, %s, %s, %s, %s)", (Nombres, Apellidos, Nickname, Password, E_Mail, Adress, Phone))
        db.commit()
        flash('Usuario creado correctamente.', 'Sucess!');
        
        
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
        Nickname_Modify = request.form.get('usuariopersona')
        Password_Modify = request.form.get('contraseñapersona')
        Email_Modify = request.form.get('emailpersona')
        Adress_Modify = request.form.get('direccionpersona')
        Phone_Modify = request.form.get('telefonopersona')

    #sentencia para actualizar los datos
        Update_Data = "UPDATE persona_info set nombreper=%s,apellidoper=%s, usuarioper=%s,contraseña=%s, emailper=%s,direccionper=%s,telefonoper=%s where ID_Persona=%s"
        cursor.execute(Update_Data,(Nombres_Modify, Apellidos_Modify, Nickname_Modify, Password_Modify, Email_Modify, Adress_Modify, Phone_Modify, id))
        db.commit()

        return redirect(url_for('lista'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM persona_info WHERE ID_Persona = %s', (id,))
        data = cursor.fetchall()

        return render_template('Editar.html', personas_info=data[0])

@app.route('/eliminar/<int:id>', methods=['GET'])
def Eliminar_Usuario(id):
    
    return redirect(url_for('Lista_Registros'))



#Aqui ejecutamos la app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=Lista_Registros)
    app.run(debug=True, port=5005)