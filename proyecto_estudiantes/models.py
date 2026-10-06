# Importamos la librería json, aunque en esta clase no la usamos directamente, 
# a veces es útil tenerla a mano para depurar.
import json

# Definimos una TUPLA con los campos básicos que el usuario deberá escribir.
# Usamos una tupla (paréntesis) porque estos campos no van a cambiar en la ejecución.
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")

class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones exigidas."""

    # El método __init__ es el constructor. Se ejecuta cada vez que creamos un nuevo Estudiante.
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante         # Asignamos el ID
        self.nombre = nombre            # Asignamos el nombre
        self.apellido = apellido        # Asignamos el apellido
        self.email = email              # Asignamos el email
        self.carnet = carnet            # Asignamos el carnet
        
        # COLECCIÓN 1 y 2: DICCIONARIO de LISTAS para las notas. 
        # Si no nos pasan notas al crearlo, inicializamos un diccionario vacío {}.
        self.notas = notas if notas else {}
        
        # COLECCIÓN 3: CONJUNTO (set) para las materias. 
        # Los sets son perfectos aquí porque no permiten elementos duplicados.
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        # Retorna un string formateado uniendo nombre y apellido.
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        # Agregamos la materia al set. Si ya existía, el set simplemente lo ignora (no duplica).
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        # Primero nos aseguramos de que el estudiante esté inscrito en esa materia.
        self.inscribir_materia(materia)
        # setdefault busca si la materia ya existe en el diccionario.
        # Si NO existe, crea una lista vacía []. Luego, hace el append() de la nota a esa lista.
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        # Creamos una lista vacía para juntar absolutamente todas las notas.
        todas_las_notas = []
        # .values() saca solo las listas de notas (ignorando los nombres de las materias)
        for lista_notas in self.notas.values():
            # extend() agarra los elementos de la lista y los une a nuestra lista principal
            todas_las_notas.extend(lista_notas) 
        
        # Si la lista está vacía (no hay notas), el promedio es 0 para evitar error de división por cero.
        if not todas_las_notas:
            return 0
        # Sumamos todas las notas, las dividimos por la cantidad total y redondeamos a 2 decimales.
        return round(sum(todas_las_notas) / len(todas_las_notas), 2)

    def materias_en_comun(self, otro_estudiante):
        # El operador '&' realiza una INTERSECCIÓN matemática entre dos sets.
        # Devuelve un nuevo set solo con las materias que ambos estudiantes tienen.
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        """Prepara el objeto para ser guardado en el archivo JSON."""
        return {
            "id": self.id,                  # Guardamos el ID
            "nombre": self.nombre,          # Guardamos el nombre
            "apellido": self.apellido,      # Guardamos el apellido
            "email": self.email,            # Guardamos el email
            "carnet": self.carnet,          # Guardamos el carnet
            "notas": self.notas,            # Guardamos el diccionario de notas
            # OJO: JSON no entiende qué es un "set". 
            # Por eso, usamos sorted() para convertir el set en una lista ordenada antes de guardar.
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Toma un diccionario plano (leído del JSON) y lo convierte en un objeto Estudiante real."""
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"], datos["carnet"],
            # Usamos .get() por si acaso el diccionario antiguo no tenía notas (evita errores)
            notas=datos.get("notas", {}),
            # Al leer del JSON (que viene como lista), lo volvemos a convertir a un set (conjunto)
            materias=set(datos.get("materias", [])),
        )