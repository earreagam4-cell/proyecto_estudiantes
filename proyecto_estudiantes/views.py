# Importamos la clase Estudiante y los campos desde nuestro modelo.
from models import Estudiante, CAMPOS_ESTUDIANTE
# Importamos la clase que sabe cómo leer y guardar archivos JSON.
from shared.json_manager import GestorJSON
# Importamos una función de validación de correo.
from shared.herramientas import es_email_valido

# Instanciamos el gestor apuntando a la ruta donde se guardarán los estudiantes.
gestor = GestorJSON("data/estudiantes.json")

# Definimos tuplas para saber qué campos son obligatorios y por cuáles se puede buscar.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """Crea un SET con todos los emails para buscar duplicados súper rápido."""
    # Usamos sintaxis de "Set Comprehension" (como list comprehension pero con {})
    # Recorremos el JSON, sacamos el email, lo pasamos a minúsculas y lo metemos al set.
    # Si pasamos un excepto_id (ej. al actualizar), ignora el email de ese ID.
    return {r["email"].lower() for r in gestor.leer() if r["id"] != excepto_id}

def carnets_registrados(excepto_id=None):
    """Crea un SET con todos los carnets para evitar duplicados."""
    # Igual que arriba, pero pasamos el carnet a mayúsculas para estandarizar.
    return {r["carnet"].upper() for r in gestor.leer() if r["id"] != excepto_id}

def siguiente_id():
    """Calcula cuál será el ID del nuevo estudiante."""
    # Sacamos una lista con todos los IDs actuales.
    ids = [registro["id"] for registro in gestor.leer()]
    # Si hay IDs, buscamos el máximo y le sumamos 1. Si no hay (lista vacía), empezamos en 1.
    return max(ids) + 1 if ids else 1

# ===================== CRUD BÁSICO =====================

def crear_estudiante(datos):
    """Recibe un diccionario con los datos tecleados por el usuario para crear un estudiante."""
    try:
        # Limpiamos los espacios en blanco de todos los campos ingresados.
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        # Buscamos si el usuario dejó algún campo obligatorio vacío.
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            # Retornamos tupla: (Falso, mensaje de error)
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # Validamos el formato del correo.
        if not es_email_valido(valores["email"]):
            return False, "Formato de email inválido"

        # Verificamos que el email no exista ya, buscando en el set de emails.
        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        
        # Verificamos que el carnet no exista ya, buscando en el set de carnets.
        if valores["carnet"].upper() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        # Creamos el objeto Estudiante. El **valores desempaqueta el diccionario como argumentos.
        estudiante = Estudiante(siguiente_id(), **valores)

        # Leemos todos los registros actuales del JSON.
        registros = gestor.leer()
        # Transformamos nuestro objeto a diccionario y lo agregamos a la lista.
        registros.append(estudiante.a_diccionario())
        
        # Intentamos guardar la lista completa en el archivo JSON.
        if not gestor.guardar(registros):
            return False, "Error al guardar en disco"

        # Si todo salió bien, retornamos tupla de éxito.
        return True, f"Estudiante creado con ID {estudiante.id}"
    except Exception as error:
        # Atrapamos cualquier error raro para que el programa no colapse.
        return False, f"Error inesperado: {error}"

def obtener_todos():
    """Lee el JSON y convierte cada diccionario en un objeto Estudiante real."""
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]

def obtener_por_id(id_estudiante):
    """Busca un estudiante por su ID."""
    # Recorremos la lista de objetos estudiante.
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante  # Si lo encuentra, lo devuelve y sale de la función.
    return None  # Si termina el bucle y no lo encontró, devuelve None (nada).

def buscar_estudiantes(termino):
    """Busca texto en varios campos del estudiante."""
    # Limpiamos el texto a buscar y lo pasamos a minúsculas.
    termino = termino.strip().lower()
    if not termino: return [] # Si no escribió nada, devolvemos lista vacía.

    encontrados = []
    # Recorremos el JSON crudo.
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            # Comparamos el término con el valor del campo (todo en minúsculas).
            if termino in str(registro.get(campo, "")).lower():
                # Si hay coincidencia, lo convertimos a objeto y lo guardamos.
                encontrados.append(Estudiante.desde_diccionario(registro))
                break # Rompemos el bucle interno para no meter al mismo estudiante 2 veces.
    return encontrados

def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza datos de un estudiante existente."""
    try:
        # Truco con sets: si los campos que envían menos los campos permitidos deja algo, es que enviaron un campo falso.
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos inválidos: {', '.join(desconocidos)}"

        # Validamos que el nuevo email/carnet no pertenezca a OTRO estudiante.
        if "email" in cambios and cambios["email"].lower() in emails_registrados(id_estudiante):
            return False, "Ese email lo usa otro estudiante"
            
        if "carnet" in cambios and cambios["carnet"].upper() in carnets_registrados(id_estudiante):
            return False, "Ese carnet lo usa otro estudiante"

        registros = gestor.leer()
        # Buscamos en qué posición exacta de la lista está el estudiante.
        posicion = next((i for i, r in enumerate(registros) if r["id"] == id_estudiante), None)
        
        if posicion is None:
            return False, "Estudiante no encontrado"

        # Actualizamos el diccionario en esa posición con los nuevos datos.
        registros[posicion].update(cambios)
        gestor.guardar(registros) # Guardamos en el JSON.
        return True, "Estudiante actualizado"
    except Exception as error:
        return False, f"Error: {error}"

def eliminar_estudiante(id_estudiante):
    """Elimina a un estudiante del JSON."""
    registros = gestor.leer()
    # Creamos una NUEVA lista dejando afuera al estudiante que queremos borrar.
    quedan = [r for r in registros if r["id"] != id_estudiante]

    # Si las dos listas tienen el mismo tamaño, significa que no se borró nada (no existía el ID).
    if len(quedan) == len(registros):
        return False, "Estudiante no encontrado"

    # Guardamos la nueva lista en el JSON, sobreescribiendo el archivo.
    gestor.guardar(quedan)
    return True, "Estudiante eliminado"

# ===================== OPERACIONES NUEVAS =====================

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota, validando que esté entre 0 y 20."""
    try:
        # Intentamos convertir la nota a número decimal.
        nota = float(nota)
        # Validamos el rango de calificación.
        if nota < 0 or nota > 20:
            return False, "La nota debe estar entre 0 y 20"
    except ValueError:
        # Si el usuario escribió letras en vez de números, atrapamos el error.
        return False, "La nota debe ser un número válido"
        
    # Limpiamos el nombre de la materia y la capitalizamos (ej: "matematica" -> "Matematica")
    materia = materia.strip().capitalize()
    registros = gestor.leer()
    
    # Buscamos la posición del estudiante en la lista.
    posicion = next((i for i, r in enumerate(registros) if r["id"] == id_estudiante), None)
    if posicion is None:
        return False, "Estudiante no encontrado"
        
    # Convertimos el diccionario plano a un objeto Estudiante para poder usar sus funciones.
    estudiante = Estudiante.desde_diccionario(registros[posicion])
    # Usamos el método de la clase para agregar la nota y la materia internamente.
    estudiante.agregar_nota(materia, nota)
    
    # Lo volvemos a convertir a diccionario y reemplazamos el registro viejo en la lista.
    registros[posicion] = estudiante.a_diccionario()
    gestor.guardar(registros)
    
    return True, f"Nota de {nota} agregada en {materia}"

def materias_ofertadas():
    """Devuelve un set con TODAS las materias que existen en la base de datos."""
    todas_las_materias = set() # Creamos un conjunto vacío.
    for registro in gestor.leer():
        # .update() agrega múltiples elementos a un set. Si la materia ya estaba, no se duplica.
        todas_las_materias.update(registro.get("materias", []))
    return todas_las_materias

def estudiantes_en_comun(id_a, id_b):
    """Devuelve qué materias ven dos estudiantes al mismo tiempo."""
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)
    
    # Validamos que ambos existan.
    if not estudiante_a or not estudiante_b:
        return False, "Uno o ambos IDs no existen"
        
    # Llamamos al método de intersección de conjuntos que creamos en el modelo.
    materias_compartidas = estudiante_a.materias_en_comun(estudiante_b)
    return True, materias_compartidas