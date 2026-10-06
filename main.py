from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota, 
    materias_ofertadas, estudiantes_en_comun
)

def pausa():
    input("\nPresione Enter para continuar...")

def mostrar_tabla(estudiantes):
    """Imprime una tabla bonita con columnas alineadas."""
    print(f"{'ID':<5}{'CARNET':<15}{'NOMBRE':<25}{'EMAIL':<30}{'PROMEDIO':<10}")
    print("-" * 85) # Imprime una línea separadora
    for est in estudiantes:
        print(f"{est.id:<5}{est.carnet:<15}{est.obtener_nombre_completo():<25}"
              f"{est.email:<30}{est.obtener_promedio():<10}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")

# ---------- OPERACIONES CRUD ----------

def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {} # Diccionario para atrapar lo que teclea el usuario
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")
    
    exito, mensaje = crear_estudiante(datos)
    
    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
    pausa()

def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("No hay estudiantes registrados.")
    else:
        mostrar_tabla(estudiantes) # Enviamos la lista de objetos a la tabla.
    pausa()

def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email o carnet: ")
    encontrados = buscar_estudiantes(termino)
    mostrar_tabla(encontrados) if encontrados else imprimir_info("Sin resultados.")
    pausa()

def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        return imprimir_error("El id debe ser un número"), pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error("No existe el estudiante")
    else:
        for clave, valor in est.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
    pausa()

def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        return imprimir_error("El id debe ser un número"), pausa()

    est = obtener_por_id(id_est)
    if not est:
        return imprimir_error("No existe el estudiante"), pausa()

    print("Deje en blanco para no cambiar el campo.\n")
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(est, campo) # Obtenemos el valor actual del campo para mostrarlo.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
    pausa()

def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        return imprimir_error("El id debe ser un número"), pausa()

    # Preguntamos por seguridad antes de borrar.
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_est)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
    pausa()

# ---------- NUEVAS OPERACIONES ----------

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        return imprimir_error("El id debe ser numérico"), pausa()
        
    materia = input("Materia: ")
    nota = input("Nota (0-20): ")
    
    exito, mensaje = agregar_nota(id_est, materia, nota)
    imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
    pausa()

def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        return imprimir_error("El id debe ser numérico"), pausa()
        
    est = obtener_por_id(id_est)
    if not est:
        imprimir_error("No existe el estudiante")
    else:
        imprimir_exito(f"El promedio de {est.obtener_nombre_completo()} es: {est.obtener_promedio()}")
    pausa()

def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        return imprimir_error("Los IDs deben ser numéricos"), pausa()
        
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    else:
        if not resultado: # Si el set está vacío
            imprimir_info("No tienen materias en común.")
        else:
            imprimir_exito(f"Comparten {len(resultado)} materia(s): {', '.join(resultado)}")
    pausa()

def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS (GLOBAL)")
    materias = materias_ofertadas()
    if not materias: # Si el set está vacío
        imprimir_info("Aún no hay materias registradas.")
    else:
        imprimir_exito(f"Total: {len(materias)} materia(s)")
        for m in sorted(materias):
            print(f"  - {m}")
    pausa()

def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"

OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Ver materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}

def mostrar_menu():
    """Recorre el diccionario OPCIONES e imprime el menú automáticamente."""
    imprimir_titulo("SISTEMA DE ESTUDIANTES")
    for tecla, (texto, _) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()

def main():
    """Bucle principal de la aplicación."""
    while True: # Se repite hasta que hagamos 'break'
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue # Vuelve al inicio del while
        
        _, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break

if __name__ == "__main__":
    try:
        main() # Arrancamos el programa
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")