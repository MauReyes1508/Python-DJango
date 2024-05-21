from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature


app = Flask(__name__)
#Configurar la conexión de base de datos
app.config['SECRET_KEY'] = '15'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY']) #De esta manera se asegura de que el token no pueda ser manipulado
db= mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "GestionTareas"
)

##########################################################################################################################################################################################################################################################################################################
####################################//FUNCION PARA INICIAR SESION\\######################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/', methods = ['GET' , 'POST'])
def Login():
    usuario = request.form.get('Usuario')
    contra = request.form.get('Contraseña')
    
    cursor = db.cursor(dictionary=True)
    query = "SELECT Nombre, Apellido, User, Contraseña, ROL, Genero FROM usuario WHERE User = %s"
    cursor.execute(query,(usuario,))
    usuarios = cursor.fetchone()

    if(usuarios and check_password_hash(usuarios['Contraseña'],contra)): #Entre comillas simple va el nombre del campo de la base de datos
        #Crear la sesion
        session['usuario'] = usuarios ['User'] #<-- Tal como en la base de datos en la segunda llave
        session['Rol'] = usuarios ['ROL']
        session['Nombre_usuario'] = usuarios ['Nombre']
        session['Apellido_usuario'] = usuarios ['Apellido']
        session['Genero_usuario'] = usuarios['Genero']


        if usuarios['ROL'] == 'admin':
            return render_template('PrincipalAdmin.html', nombre_usuario=usuarios['Nombre'], Apellido_usuario=usuarios['Apellido'], user=usuarios['User'], Genero_usuario=usuarios['Genero'])
        else:
            return render_template('PrincipalUser.html', nombre_usuario=usuarios['Nombre'], Apellido_usuario=usuarios['Apellido'], user=usuarios['User'], Genero_usuario=usuarios['Genero'])

    
    return render_template('index.html')

##########################################################################################################################################################################################################################################################################################################
##################################################// RECUPERAR CONTRASEÑA \\########################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

cursor = db.cursor()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'negrohamazuka@gmail.com'
app.config['MAIL_PASSWORD'] = 'sbyb ufvp tofp dswd'
app.config['MAIL_USE_TLS'] = False #Este funciona para bloquear los posibles ataques
app.config['MAIL_USE_SSL'] = True #Este funciona de igual manera, el cual permite el envio del correo
app.config['MAIL_DEFAULT_SENDER'] = ('Servicio Nacional de Aprendizaje - Cenigraf Por Mau Reyes ADSO', 'negrohamazuka@gmail.com')
mail = Mail(app)

def enviar_correo(email):
    # Aqui se genera un token para el correo
    token = serializer.dumps(email, salt='Restablecimiento de Contraseña ') # Esto sirve para el restableciimiento de contraseña
    # Se crea la url
    enlace = url_for('restablecer_contraseña', token = token, _external = True)
    # Se crea el mensaje
    mensaje = Message(subject='Restablecimiento de Contraseña', recipients=[email], body = f'Para Restablecer Contraseña Click En El Enlace:{enlace}') # En este caso se envia el correo con el enlace para restablecer la contraseña
    
    mail.send(mensaje)

@app.route('/restablecer-contraseña/<token>', methods = ['GET' , 'POST'])
def restablecer_contraseña(token):
    
    if request.method == 'POST':
        nueva_contra = request.form['Nueva_Contraseña']
        confirmar_contra = request.form['Confirmar_Contraseña']

        # MEtodo para verificar si la contraseña coincide
        if nueva_contra != confirmar_contra:
            return print('Las contraseñas no coinciden')
        passwordNuevo = generate_password_hash(nueva_contra)
        #Verificar el token
        try:
            email = serializer.loads(token, salt='Restablecimiento de Contraseña', max_age=50000)
        
        except BadSignature:
            return print('El tiempo a expirado :(')
        
        # Actualizar en la base de datos
        cursor = db.cursor()
        consulta = "UPDATE usuario SET Contraseña = %s WHERE Email = %s"
        cursor.execute(consulta,(passwordNuevo,email))
        db.commit()
        
        return redirect(url_for('Login'))

    return render_template('recuperar_Contra.html')

@app.route('/recuperar-contraseña', methods = ['GET' , 'POST'])
def recuperar_contraseña():
    if request.method == 'POST':
        email = request.form.get('email')
        enviar_correo(email)
        
        return redirect(url_for('Login'))


    return render_template('RestablecerConEmail.html')  

##########################################################################################################################################################################################################################################################################################################
#############################################//FUNCION PARA CERRAR SESION\\#############################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/salir')
def salir():
    session.pop('usuario', None)
    return redirect(url_for('Login'))

@app.after_request   #Funcion para no almacenar el cache de la página
def add_header(response):
    response.headers['Cache-Contrl'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0

    return response

##########################################################################################################################################################################################################################################################################################################
############################################//FUNCION PARA GUARDAR USUARIOS\\###################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/RegistroUsuarios', methods=['GET' , 'POST'])

def RegistroUsuarios():
    if request.method == 'POST':
        NombreUsuario = request.form.get('Nombre')
        ApellidoUsuario = request.form.get('Apellido')
        Usuario = request.form.get('Usuario')
        EmailUser = request.form.get('Email')
        ContraseñaUser = request.form.get('Contraseña')
        RolUser = request.form.get('Rol')
        Genero_user = request.form.get('Genero')
        EncriptarPass = generate_password_hash(ContraseñaUser) #Metodo para encriptar la contraseña

        #Verificar usuario y email si ya existe
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE user = %s OR email = %s",(Usuario,EmailUser))
        resultado = cursor.fetchone()

        if resultado:
            print("Usuario o Email Ya Registrado!")
            render_template('RegistroUsuario.html')
            #Insertar los usuarios
        else:
            cursor.execute("INSERT INTO Usuario(Nombre, Apellido, User, Email, Contraseña, ROL, Genero) VALUES(%s,%s,%s,%s,%s,%s,%s)",(NombreUsuario,ApellidoUsuario,Usuario,EmailUser,EncriptarPass,RolUser,Genero_user))

            db.commit()
            print("Usuario Registrado")
            return redirect(url_for('/'))

    return render_template('RegistroUsuario.html')
##########################################################################################################################################################################################################################################################################################################
""" @app.route('/RegistrarUsuario', methods=['GET' , 'POST'])

def RegistroUsuarios():
    if request.method == 'POST':
        NombreUsuario = request.form.get('Nombre')
        ApellidoUsuario = request.form.get('Apellido')
        Usuario = request.form.get('Usuario')
        EmailUser = request.form.get('Email')
        ContraseñaUser = request.form.get('Contraseña')
        RolUser = request.form.get('Rol')
        Genero_user = request.form.get('Genero')
        EncriptarPass = generate_password_hash(ContraseñaUser) #Metodo para encriptar la contraseña

        #Verificar usuario y email si ya existe
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE user = %s OR email = %s",(Usuario,EmailUser))
        resultado = cursor.fetchone()

        if resultado:
            print("Usuario o Email Ya Registrado!")
            render_template('RegistroUsuario.html')
            #Insertar los usuarios
        else:
            cursor.execute("INSERT INTO Usuario(Nombre, Apellido, User, Email, Contraseña, ROL, Genero) VALUES(%s,%s,%s,%s,%s,%s,%s)",(NombreUsuario,ApellidoUsuario,Usuario,EmailUser,EncriptarPass,RolUser,Genero_user))

            db.commit()
            print("Usuario Registrado")
            return redirect(url_for('lista'))

    return render_template('RegistroUsuario.html') """

##########################################################################################################################################################################################################################################################################################################
#########################//FUNCION PARA MOSTRAR LISTA DE USUARIOS REGISTRADOS EN ROL ADMINISTRADOR\\######################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/lista', methods=['GET', 'POST'])
def lista():
    cursor = db.cursor(dictionary=True)  # Use dictionary=True para obtener los resultados como diccionarios
    cursor.execute("SELECT * FROM usuario")
    users = cursor.fetchall()

    return render_template('Principaladmin.html', users = users, visualizar_usuario=True, user = session['usuario'])

##########################################################################################################################################################################################################################################################################################################
############################//FUNCION PARA ELIMINAR USUARIO EN ROL ADMINISTRADOR\\##############################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/eliminar-usuario/<int:id>', methods = ['GET' , 'POST'])
def eliminar_usuario(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM usuario WHERE id_user = %s',(id,))
    db.commit()
    print("Usuario Eliminado")

    return redirect(url_for('lista'))

##########################################################################################################################################################################################################################################################################################################
#########################// FUNCION PARA ACTUALIZAR USUARIO EN ROL ADMINISTRADOR \\#########################################################################################################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/editar_usuario/<int:id>', methods = ['GET' , 'POST'])
def editar_usuario(id):

    return redirect(url_for('lista'))

##########################################################################################################################################################################################################################################################################################################
#################################################// FUNCION PARA ELIMINAR TAREAS EN ADMINISTRADOR \\#########################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/eliminar-tarea/<int:id>', methods = ['GET' , 'POST'])
def eliminar_tarea(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM tareas WHERE id_Tareas = %s',(id,))
    db.commit()
    print("Tarea Eliminada Con Exito")

    return redirect(url_for('tareas'))

##########################################################################################################################################################################################################################################################################################################
#########################// FUNCION PARA BUSCAR TAREAS \\#########################################################################################################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/buscar-tarea', methods = ['POST'])
def buscar_tarea():
    Busqueda = request.form.get('busqueda')

    cursor = db.cursor(dictionary=True)
    consulta = "SELECT * FROM tareas WHERE id_Tareas = %s OR Nombre LIKE %s"
    cursor.execute(consulta, (Busqueda, "%"+Busqueda+"%"))
    tareas = cursor.fetchall()
    db.commit()

    return render_template('BusquedaResultado.html', tareas = tareas, Busqueda = Busqueda)

##########################################################################################################################################################################################################################################################################################################
#############################################// FUNCION PARA EDITAR TAREAS EN ADMINISTRADOR \\#############################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/editar_tarea/<int:id>', methods = ['GET' , 'POST'])
def editar_tarea(id):

    if request.method == 'POST':
        #codigotar = request.form['codigo']
        nombretar = request.form['nombreTar']
        fechaInicio = request.form['finicio']
        fechaFinal = request.form['ffinal']
        estadoTar = request.form['estadotar']

        #Obtener los datos de la tarea
        cursor = db.cursor()
        sql = "UPDATE tareas SET Nombre = %s, Fecha_Inicio = %s, Fecha_Final = %s, Estado = %s WHERE id_Tareas = %s"
        cursor.execute(sql,(nombretar, fechaInicio,fechaFinal,estadoTar,id))
        db.commit()
        return redirect(url_for('tareas'))
    
    else:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tareas WHERE id_Tareas = %s', (id,))
        data = cursor.fetchall()
        cursor.close()
        
        

    return render_template('Modaltareas.html', tareas = data[0])

##########################################################################################################################################################################################################################################################################################################
###########################//Mostrar Tareas En El Administrador\\#########################################################################################################################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/tareas', methods=['GET', 'POST'])
def tareas():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()

    return render_template('Principaladmin.html', tareas=tareas, visualizar_tareas=True, user=session['usuario'])



##########################################################################################################################################################################################################################################################################################################
################################//GUARDAR TAREAS\\#################################################################################################################################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################

@app.route('/Registrotarea', methods=['GET' , 'POST'])
def RegistrarTarea():
    if request.method == 'POST':
        NombreTarea = request.form.get('Nom_Tarea')
        FechaInicio = request.form.get('FechaInicio')
        FechaFinal = request.form.get('FechaFinal')
        Estadotar = request.form.get('Estado')
        cursor = db.cursor()
        #Verificar el nombre de la tarea que se va a registrar

        cursor.execute("SELECT * FROM tareas WHERE Nombre = %s ", (NombreTarea,))
        print("Nombre de la tarea ya registrado")
        
        Existe = cursor.fetchone() # Metodo para verificar si los datos existen
        if Existe:
            print("La tarea ya existe")
            return render_template('RegistroTareas.html') #Metodo que carga una vista de tipo HTML

        #Insertar datos en la base de datos (tabla tareas)
        else:
            cursor.execute("INSERT INTO tareas(Nombre, Fecha_Inicio, Fecha_Final, Estado) VALUES (%s, %s, %s, %s)", (NombreTarea, FechaInicio, FechaFinal, Estadotar))
            db.commit()
            print("Tarea Registrada")
            return redirect(url_for('tareas'))
        
    return render_template('RegistroTareas.html')

##########################################################################################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################################################################################




if __name__== '__main__':
    app.run(debug=True)
    app.add_url_rule('/',view_func=RegistrarTarea) 