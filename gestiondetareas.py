import json
from datetime import datetime

#Clase tarea
class Tarea:
    def __init__(self, título, descripcion, fecha_vencimiento):
        self.título = título
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completado = False #Hasta que nosotros no le demos una indicación de que ya está completado, debe mantenerse
# en False (sin completar)

    def marcar_completada(self):
        self.completado = True

    def editar(self, nuevo_título, nueva_descripcion, nueva_fecha):
        self.título = nuevo_título
        self.descripcion = nueva_descripcion
        self.fecha_vencimiento = nueva_fecha

class Usuario:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contraseña = contraseña
        self.tareas = []

    def agregar_tarea(self, tarea: Tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, título_tarea):
        self.tareas = [tarea for tarea in self.tareas if tarea.título != título_tarea]
        # Recorre toda la lista de tareas hasta llegar a la tarea que tenga el titulo igual al ingresado.
    
    def obtener_tareas(self):
        return self.tareas
#Clase sistema de Gestion de Tareas

class SistemaGesionTareas:
    #inicialización del sistema de gestión de un archivo
    def __init__(self, archivo_datos = "datos_usuario.json"):
        self.usuarios = {}
        self.archivo_datos = archivo_datos
        self.cargar_datos()
    
    def cargar_datos (self):
        #cargar datos de los usuarios en JSON
        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as archivo:
                try:
                    datos = json.load(archivo)
                except json.JSONDecodeError:
                    print("El archivo de datos está vacío o corrupto. Se iniciará vacío.")
                datos = {}
                for nombre_usuario, info in datos.items():
                    # Crea un objeto usuario para cda usuario en los datos
                    usuario = Usuario(nombre_usuario, info.get["contraseña", ""])
                    for tarea_info in info.get("tareas", []):
                        #Crea un objeto tareas para cada tarea del usuario
                        tarea = Tarea(tarea_info["título"], tarea_info["descripcion"], tarea_info["fecha_vencimiento"])
                        tarea.completado= tarea_info["completado", False]
                        usuario.agregar_tarea(tarea)
                    self.usuarios[nombre_usuario] = usuario
        except FileNotFoundError: #manejo de excepciones
            print("Archivo de datos no encontrado, se creará uno nuevo al guardar")

    def guardar_datos(self):
        # Guardar datos de los usuarios en el archivo
        datos = {} #Este es el diccionario de datos
        for nombre_usuario, usuario in self.usuarios.items():
            # Organiza las tareas y la información del usuario en un diccionario
            datos[nombre_usuario] = {
                "contraseña": usuario.contraseña, 
                "tareas": [
                    {
                        "título": tarea.título, "descripcion": tarea.descripcion, "fecha_vencimiento": tarea.fecha_vencimiento, "completado": tarea.completado
                    }
                    for tarea in usuario.tareas]}
        with open(self.archivo_datos, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent = 2, ensure_ascii=False)

    def registrar_usuario(self, nombre_usuario, contraseña):
        # Registrar un nuevo usuario si el nombre de usuario no existe

        if nombre_usuario in self.usuarios:
            print("El nombre de usuario ya existe")
            return False
        else:
            self.usuarios[nombre_usuario] = Usuario(nombre_usuario, contraseña)
            self.guardar_datos()
            print("Usuario registrado con éxito")
            return True
    
    def iniciar_sesion(self, nombre_usuario, contraseña):
        usuario = self.usuarios.get(nombre_usuario)
        if usuario and usuario.contraseña == contraseña:
            print("Inicio de sesión exitoso.")
            return usuario
        else:
            print("Usuario o contraseña incorrectos.")
            return None
        
    def menu_usuario(self, usuario):
        while True:
            print("\n1. Crear tarea")
            print("2. Ver tareas")
            print("3. Editar tarea")
            print("4. Completar tarea")
            print("5. Eliminar tarea")
            print("Cerrar sesión")

            opcion = input("Selecciona una opción")

            if opcion == "1":
                título = input("título de la tarea: ")
                descripcion = input("Ingresa la descripcion: ")
                fecha_vencimiento = input("Fecha de vencimiento (YYY-MM-DD): ")
                tarea = Tarea(título, descripcion, fecha_vencimiento)
                usuario.agregar_tarea(tarea)
                self.guardar_datos()
                print("Tarea creada con exito")

            elif opcion == "2":
                tareas = usuario.obtener_tareas()
                if not tareas:
                    print("No tienes tareas")
                for idx, tarea in enumerate(tareas, start=1):
                    estado = "Completado" if tarea.completado else "pendiente"
                    print(f"{idx}. {tarea.título} - {estado} (Vence: {tarea.fecha_vencimiento})")
            
            elif opcion == "3":
                título_tarea = input("título de la tarea a editar: ")
                tarea = next((t for t in usuario.tareas if t.título == título_tarea), None)
                if tarea:
                    nuevo_título = input("Nueva descripcion: ")
                    nueva_descripcion = input("Nueva descripcion: ")
                    nueva_fecha = input ("Nueva fecha de vencimiento (YYY-MM-DD): ")
                    tarea.editar_tarea(nuevo_título, nueva_descripcion, nueva_fecha)
                    self.guardar_datos()
                    print("Tarea actualizada con exito")
                else:
                    print ("Tarea no encontrada")

            elif opcion == "4":
                título_tarea = input("Título de la tarea a completar: ").strip()
                tarea = next((t for t in usuario.tareas if t.título == título_tarea), None)
                if tarea:
                    tarea.marcar_completada()
                    self.guardar_datos()
                    print("Tarea marcada como completada")
                else:
                    print("Tarea no encontrada")

            elif opcion == "5":
                título_tarea = input("Título de la tarea a eliminar: ").strip()
                usuario.eliminar_tarea(título_tarea)
                self.guardar_datos()
                print("Tarea eliminada (si existía)")

            elif opcion == "6":
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida. Inténtelo de nuevo.")
#Ejecucion del sistema
if __name__ =="__main__":
    sistema = SistemaGesionTareas()
    while True:
        print("\n---- Sistema de Gestion de Tareas ----")
        print("1. Registrar usuario")
        print("2. Iniciar sesion")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_usuario = input("Ingrese nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            sistema.registrar_usuario(nombre_usuario, contraseña)

        elif opcion == "2":
            nombre_usuario = input("Ingrese nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            usuario= sistema.iniciar_sesion(nombre_usuario, contraseña)
            if usuario:
                sistema.menu_usuario(usuario)
        
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

