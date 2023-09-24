from flask import Flask, render_template, request, redirect, url_for, session
from grafo import Usuario
from utils import GrafoUsuarios

app = Flask(__name__)
app.secret_key = 'clave_secreta'

grafo_usuarios = GrafoUsuarios()

usuario1 = Usuario("usuario1@example.com", "contraseña1", "Juan", "Pérez", 30, "Hombre")
usuario1.agregar_interes("artes")
usuario1.agregar_interes("moda")
usuario2 = Usuario("usuario2@example.com", "contraseña2", "María", "Gómez", 25, "Mujer")
usuario3 = Usuario("usuario3@example.com", "contraseña3", "Carlos", "López", 28, "Hombre")
grafo_usuarios.agregar_usuario(usuario1.correo, usuario1)
grafo_usuarios.agregar_usuario(usuario2.correo, usuario2)
grafo_usuarios.agregar_usuario(usuario3.correo, usuario3)

# Conectar usuarios en el grafo (esto es un ejemplo)
grafo_usuarios.agregar_conexion(usuario1.correo, usuario2.correo)
grafo_usuarios.agregar_conexion(usuario2.correo, usuario3.correo)
@app.route('/')
def wellcome():
    return render_template('wellcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['username']
        contraseña = request.form['password']
        global usuario_verificado
        usuario = grafo_usuarios.buscar_usuario_por_correo(correo)
        if usuario and usuario.contraseña == contraseña:
            usuario_verificado = usuario            
            return redirect(url_for('index'))
        else:
            error = 'Correo o contraseña incorrectos. Inténtalo de nuevo.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Obtiene los datos del formulario
        username = request.form['username']
        password = request.form['password']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        edad = request.form['edad']
        genero = request.form['genero']
        intereses = request.form.getlist('intereses[]')

        if grafo_usuarios.buscar_usuario_por_correo(username):
            error = 'El correo electrónico ya está registrado.'
            return render_template('signin.html', error=error)
            
        nuevo_usuario = Usuario(username, password, nombres, apellidos, edad, genero)
        nuevo_usuario.intereses= intereses
        grafo_usuarios.agregar_usuario(nuevo_usuario.correo,nuevo_usuario)     
                
        return redirect(url_for('login'))
    
    return render_template('signin.html')

@app.route('/index')
def index():   
    conexiones = grafo_usuarios.buscar_conexiones(usuario_verificado.correo)          
    recomendaciones = grafo_usuarios.recomendar_conexiones(usuario_verificado.correo)    
    return render_template('index.html', user=usuario_verificado, conexiones=conexiones, recomendaciones=recomendaciones)

@app.route('/agregar_amigo/<string:correo_recomendado>', methods=['POST'])
def agregar_amigo(correo_recomendado):

    # Encuentra al usuario recomendado por su correo
    usuario_recomendado = grafo_usuarios.buscar_usuario_por_correo(correo_recomendado)

    if usuario_verificado and usuario_recomendado:
        # Agrega una relación de "amigo" entre los dos usuarios
        grafo_usuarios.agregar_relacion_amigo(usuario_verificado.correo, usuario_recomendado.correo)
        return redirect(url_for('index'))
    else:
        return "Error: No se pudo agregar como amigo."


if __name__ == '__main__':
    app.run(debug=True)