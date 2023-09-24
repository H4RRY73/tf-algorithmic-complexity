
from grafo import Grafo, Usuario

class GrafoUsuarios:
    def __init__(self):
        self.grafo_usuarios = Grafo()

    def agregar_usuario(self, correo, usuario):
        self.grafo_usuarios.agregar_nodo(correo, usuario)

    def agregar_conexion(self, correo1, correo2):
        self.grafo_usuarios.agregar_arista(correo1, correo2)

    def buscar_usuario_por_correo(self, correo):
        return self.grafo_usuarios.obtener_objeto(correo)
    
    def buscar_conexiones(self, usuario):        
        conexiones = self.grafo_usuarios.obtener_vecinos(usuario)        
        return conexiones  

    def recomendar_conexiones(self, correo):
        visitados = set()
        conexiones_directas = self.buscar_conexiones(correo)
        recomendaciones = []

        for conexion_directa in conexiones_directas:
            visitados.add(conexion_directa.correo)  # Agregar el correo a visitados
            self._recomendar_conexiones_backtracking(conexion_directa, correo, visitados, recomendaciones)

        # Eliminar conexiones directas y el propio usuario de las recomendaciones
        recomendaciones = [recomendacion for recomendacion in recomendaciones if recomendacion.correo != correo and recomendacion not in conexiones_directas]

        return recomendaciones

    def _recomendar_conexiones_backtracking(self, conexion, correo, visitados, recomendaciones):
        for siguiente_conexion in self.buscar_conexiones(conexion.correo):
            if siguiente_conexion.correo not in visitados:  # Comprobar el correo en lugar del objeto
                visitados.add(siguiente_conexion.correo)  # Agregar el correo a visitados
                self._recomendar_conexiones_backtracking(siguiente_conexion, correo, visitados, recomendaciones)
                recomendaciones.append(siguiente_conexion)
                if len(recomendaciones) >= 10:  # Limitar el número de recomendaciones
                    return