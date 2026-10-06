import json

CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")

class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones exigidas."""
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante         # Asignamos el ID
        self.nombre = nombre            # Asignamos el nombre
        self.apellido = apellido        # Asignamos el apellido
        self.email = email              # Asignamos el email
        self.carnet = carnet            # Asignamos el carnet
        self.notas = notas if notas else {}
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas_las_notas = []
        for lista_notas in self.notas.values():
            todas_las_notas.extend(lista_notas) 
        
        if not todas_las_notas:
            return 0
        return round(sum(todas_las_notas) / len(todas_las_notas), 2)

    def materias_en_comun(self, otro_estudiante):
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
            "materias": sorted(self.materias),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        """Toma un diccionario plano (leído del JSON) y lo convierte en un objeto Estudiante real."""
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"], datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )