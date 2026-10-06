import json
import os
class GestorJSON:
    """Clase encargada de manejar la lectura y escritura de archivos JSON."""
    def __init__(self, ruta_archivo):
        self.ruta = ruta_archivo
        
        directorio = os.path.dirname(self.ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

    def leer(self):
        """Lee el archivo JSON y devuelve una lista de diccionarios."""
        try:
            with open(self.ruta, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
                
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:            # Si el archivo existe pero su contenido está corrupto o mal escrito,
            return []

    def guardar(self, datos):
        """Recibe una lista de diccionarios y la guarda en el archivo JSON."""
        try:
            with open(self.ruta, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error al guardar JSON: {e}")
            return False

    def eliminar_estudiante(self, id_estudiante):    
        """Elimina a un estudiante del JSON."""    
        registros = self.leer()     
        quedan = [r for r in registros if str(r["id"]) != str(id_estudiante)]
        if len(quedan) == len(registros):
            return False, "Estudiante no encontrado"            
        if not self.guardar(quedan):               
            return False, "Error al guardar en disco"   
        return True, "Estudiante eliminado exitosamente del archivo JSON"


