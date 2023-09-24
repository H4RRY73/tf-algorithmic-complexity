
from grafo import Usuario, Grafo
from utils import GrafoUsuarios

# Crear una instancia del grafo
grafo = GrafoUsuarios()

# Crear algunos usuarios y agregarlos al grafo
usuario1 = Usuario("usuario1@example.com", "contraseña1", "Juan", "Pérez", 30, "Hombre")
usuario2 = Usuario("usuario2@example.com", "contraseña2", "pedro", "Gómez", 25, "Hombre")
usuario3 = Usuario("usuario3@example.com", "contraseña3", "Zeri", "Valle", 18, "Mujer")

grafo.agregar_usuario(usuario1.correo, usuario1)
grafo.agregar_usuario(usuario2.correo, usuario2)
grafo.agregar_usuario(usuario3.correo, usuario3)

# Conectar usuarios en el grafo (esto es un ejemplo)
grafo.agregar_conexion(usuario1.correo, usuario2.correo)
grafo.agregar_conexion(usuario2.correo, usuario3.correo)

# Supongamos que queremos obtener las conexiones (vecinos) del usuario1
usuario_seleccionado = usuario1
conexiones = grafo.buscar_conexiones(usuario1.correo)
# Ahora conexiones contiene objetos Usuario
for conexion in conexiones:
    print(f"Correo: {conexion.correo}, Nombre: {conexion.nombres}, Apellidos: {conexion.apellidos}")

recomendaciones = grafo.recomendar_conexiones(usuario1.correo)

# Imprimir las recomendaciones
for recomendacion in recomendaciones:
    print(recomendacion.correo)
