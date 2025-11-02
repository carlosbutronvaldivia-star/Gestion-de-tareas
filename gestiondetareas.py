import json
from datetime import datetime

#Class tarea
class Tarea:
    def __init__(self, título, descripcion, fecha_vencimiento):
        self.título = título
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completado = False #Hasta que nosotros no le demos una indicación de que ya está completado, debe mantenerse
# en False (sin completar)

def marcar_completada(self):
    self.completado = True

def editar1_tarea(self, nuevo_título, nueva_descripción, nueva_fecha):
    self.título = nuevo_título
    self.descripcion = nueva_descripción
    self.fecha_vencimiento = nueva_fecha