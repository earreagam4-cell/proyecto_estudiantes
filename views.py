from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")

# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """Crea un SET con todos los emails para buscar duplicados súper rápido."""
    return {r["email"].lower() for r in gestor.leer() if r["id"] != excepto_id}

def carnets_registrados(excepto_id=None):
    """Crea un SET con todos los carnets para evitar duplicados."""
    return {r["carnet"].upper() for r in gestor.leer() if r["id"] != excepto_id}

def siguiente_id():
    """Calcula cuál será el ID del nuevo estudiante."""
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1

# ===================== CRUD BÁSICO =====================

def crear_estudiante(datos):
    """Recibe un diccionario con los datos tecleados por el usuario para crear un estudiante."""
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, "Formato de email inválido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"
        
        if valores["carnet"].upper() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        
        if not gestor.guardar(registros):
            return False, "Error al guardar en disco"

        return True, f"Estudiante creado con ID {estudiante.id}"
    except Exception as error:
        return False, f"Error inesperado: {error}"

def obtener_todos():
    """Lee el JSON y convierte cada diccionario en un objeto Estudiante real."""
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]

def obtener_por_id(id_estudiante):
    """Busca un estudiante por su ID."""
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante  # Si lo encuentra, lo devuelve y sale de la función.
    return None  # Si termina el bucle y no lo encontró, devuelve None (nada).

def buscar_estudiantes(termino):
    """Busca texto en varios campos del estudiante."""
    termino = termino.strip().lower()
    if not termino: return [] # Si no escribió nada, devolvemos lista vacía.

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break # Rompemos el bucle interno para no meter al mismo estudiante 2 veces.
    return encontrados

def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza datos de un estudiante existente."""
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos inválidos: {', '.join(desconocidos)}"

        if "email" in cambios and cambios["email"].lower() in emails_registrados(id_estudiante):
            return False, "Ese email lo usa otro estudiante"
            
        if "carnet" in cambios and cambios["carnet"].upper() in carnets_registrados(id_estudiante):
            return False, "Ese carnet lo usa otro estudiante"

        registros = gestor.leer()
        posicion = next((i for i, r in enumerate(registros) if r["id"] == id_estudiante), None)
        
        if posicion is None:
            return False, "Estudiante no encontrado"

        registros[posicion].update(cambios)
        gestor.guardar(registros) # Guardamos en el JSON.
        return True, "Estudiante actualizado"
    except Exception as error:
        return False, f"Error: {error}"

def eliminar_estudiante(id_estudiante):
    """Elimina a un estudiante del JSON y del archivo de texto."""
    gestor.eliminar_estudiante(id_estudiante)
    return True, "Estudiante eliminado" 

# ===================== OPERACIONES NUEVAS =====================

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota, validando que esté entre 0 y 20."""
    try:
        nota = float(nota)
        if nota < 0 or nota > 20:
            return False, "La nota debe estar entre 0 y 20"
    except ValueError:
        return False, "La nota debe ser un número válido"
        
    materia = materia.strip().capitalize()
    registros = gestor.leer()
    
    posicion = next((i for i, r in enumerate(registros) if r["id"] == id_estudiante), None)
    if posicion is None:
        return False, "Estudiante no encontrado"
        
    estudiante = Estudiante.desde_diccionario(registros[posicion])
    estudiante.agregar_nota(materia, nota)
    
    registros[posicion] = estudiante.a_diccionario()
    gestor.guardar(registros)
    
    return True, f"Nota de {nota} agregada en {materia}"

def materias_ofertadas():
    """Devuelve un set con TODAS las materias que existen en la base de datos."""
    todas_las_materias = set() # Creamos un conjunto vacío.
    for registro in gestor.leer():
        todas_las_materias.update(registro.get("materias", []))
    return todas_las_materias

def estudiantes_en_comun(id_a, id_b):
    """Devuelve qué materias ven dos estudiantes al mismo tiempo."""
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)
    
    if not estudiante_a or not estudiante_b:
        return False, "Uno o ambos IDs no existen"
        
    materias_compartidas = estudiante_a.materias_en_comun(estudiante_b)
    return True, materias_compartidas