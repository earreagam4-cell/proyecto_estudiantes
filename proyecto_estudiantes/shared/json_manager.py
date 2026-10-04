# Importamos la librería nativa json para poder leer y escribir archivos .json
import json
# Importamos 'os' para poder crear carpetas y verificar si los archivos existen en el sistema.
import os

class GestorJSON:
    """Clase encargada de manejar la lectura y escritura de archivos JSON."""

    def __init__(self, ruta_archivo):
        # Al instanciar la clase, guardamos la ruta donde estará el archivo (ej. 'data/estudiantes.json')
        self.ruta = ruta_archivo
        
        # os.path.dirname saca solo el nombre de la carpeta de la ruta (en este caso 'data')
        directorio = os.path.dirname(self.ruta)
        
        # Si la ruta tiene una carpeta (no está vacía) y esa carpeta NO existe en la computadora...
        if directorio and not os.path.exists(directorio):
            # ...entonces creamos la carpeta automáticamente para que no dé error al guardar.
            os.makedirs(directorio)

    def leer(self):
        """Lee el archivo JSON y devuelve una lista de diccionarios."""
        try:
            # Abrimos el archivo en modo lectura ('r') con codificación utf-8 (para aceptar tildes y ñ).
            # Usamos 'with' para asegurarnos de que el archivo se cierre automáticamente al terminar.
            with open(self.ruta, 'r', encoding='utf-8') as archivo:
                # json.load agarra el texto del archivo y lo convierte en una lista/diccionario de Python.
                return json.load(archivo)
                
        except FileNotFoundError:
            # Si el archivo no existe (por ejemplo, la primera vez que se ejecuta el programa),
            # no hacemos que el programa explote, simplemente devolvemos una lista vacía.
            return []
            
        except json.JSONDecodeError:
            # Si el archivo existe pero su contenido está corrupto o mal escrito,
            # devolvemos una lista vacía para empezar de cero.
            return []

    def guardar(self, datos):
        """Recibe una lista de diccionarios y la guarda en el archivo JSON."""
        try:
            # Abrimos el archivo en modo escritura ('w'). Si no existe, se crea. Si existe, se sobreescribe.
            with open(self.ruta, 'w', encoding='utf-8') as archivo:
                # json.dump toma los 'datos' (la lista) y la escribe dentro del 'archivo'.
                # indent=4 le da formato bonito (saltos de línea y tabulaciones) para que sea leíble por humanos.
                # ensure_ascii=False permite que las tildes y ñ se guarden correctamente, no como símbolos raros.
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
            # Si llegó hasta aquí sin errores, devolvemos True (guardado exitoso).
            return True
            
        except Exception as e:
            # Si ocurre cualquier error extraño (ej. el disco está lleno o no hay permisos),
            # imprimimos el error en consola para que el programador lo vea, y devolvemos False.
            print(f"Error al guardar JSON: {e}")
            return False