# Importamos la tupla de campos del modelo.
from models import CAMPOS_ESTUDIANTE
# Importamos nuestras funciones para imprimir bonito por consola.
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# Importamos TODAS las funciones que devuelve resultados desde la vista (Controlador).
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota, 
    materias_ofertadas, estudiantes_en_comun
)

def pausa():
    # Detiene la consola para que el usuario pueda leer los mensajes antes de limpiar la pantalla.
    input("\nPresione Enter para continuar...")

def mostrar_tabla(estudiantes):
    """Imprime una tabla bonita con columnas alineadas."""
    # <5 significa: alinea a la izquierda ocupando 5 espacios.
    print(f"{'ID':<5}{'CARNET':<15}{'NOMBRE':<25}{'EMAIL':<30}{'PROMEDIO':<10}")
    print("-" * 85) # Imprime una línea separadora
    for est in estudiantes:
        # Llamamos a los métodos del objeto para llenar la tabla
        print(f"{est.id:<5}{est.carnet:<15}{est.obtener_nombre_completo():<25}"
              f"{est.email:<30}{est.obtener_promedio():<10}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")

# ---------- OPERACIONES CRUD ----------

def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {} # Diccionario para atrapar lo que teclea el usuario
    for campo in CAMPOS_ESTUDIANTE:
        # Pedimos el input dinámicamente según la tupla (nombre, apellido, email, carnet)
        datos[campo] = input(f"{campo.capitalize()}: ")
    
    # Enviamos a la vista y recibimos la tupla (Booleano, String)
    exito, mensaje = crear_estudiante(datos)
    
    # if ternario: si éxito es True, imprime verde, si no, rojo.
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
    # Si la lista "encontrados" tiene datos, muestra la tabla. Si está vacía, muestra mensaje.
    mostrar_tabla(encontrados) if encontrados else imprimir_info("Sin resultados.")
    pausa()

def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        # Si teclean letras, marcamos error y retornamos para salir de la función.
        return imprimir_error("El id debe ser un número"), pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error("No existe el estudiante")
    else:
        # Convertimos el objeto a diccionario para imprimir clave-valor de forma limpia.
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
    # Solo agregamos al diccionario 'cambios' las cosas que el usuario haya escrito.
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
        # Calculamos el promedio en vivo ejecutando el método de la clase
        imprimir_exito(f"El promedio de {est.obtener_nombre_completo()} es: {est.obtener_promedio()}")
    pausa()

def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        return imprimir_error("Los IDs deben ser numéricos"), pausa()
        
    # 'resultado' puede ser un mensaje de error o un SET con las materias compartidas.
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    else:
        if not resultado: # Si el set está vacío
            imprimir_info("No tienen materias en común.")
        else:
            # Imprimimos el contenido del set separando las materias por comas.
            imprimir_exito(f"Comparten {len(resultado)} materia(s): {', '.join(resultado)}")
    pausa()

def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS (GLOBAL)")
    # Trae el set con todas las materias de toda la universidad.
    materias = materias_ofertadas()
    if not materias: # Si el set está vacío
        imprimir_info("Aún no hay materias registradas.")
    else:
        imprimir_exito(f"Total: {len(materias)} materia(s)")
        # Imprimimos el set ordenado alfabéticamente
        for m in sorted(materias):
            print(f"  - {m}")
    pausa()

def salir():
    imprimir_info("¡Hasta luego! 👋")
    # Retornamos la palabra 'salir' para que el bucle principal sepa que debe cerrarse.
    return "salir"

# Este DICCIONARIO es el corazón del menú. Evita hacer 11 "if / elif" seguidos.
# Asocia la "tecla" con una tupla: (Nombre_a_mostrar, función_a_ejecutar)
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
    # _ es una convención de Python para decir "no me importa usar esta variable (la función)"
    for tecla, (texto, _) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()

def main():
    """Bucle principal de la aplicación."""
    while True: # Se repite hasta que hagamos 'break'
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()
        
        # Validación instantánea gracias al diccionario (busca en sus llaves)
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue # Vuelve al inicio del while
        
        # Desempaquetamos la tupla. Solo necesitamos la función para ejecutarla.
        _, funcion = OPCIONES[tecla]
        # Ejecutamos la función. Si esa función retorna "salir", rompemos el bucle.
        if funcion() == "salir":
            break

# Este bloque verifica si el archivo se está ejecutando directamente desde la terminal
if __name__ == "__main__":
    try:
        main() # Arrancamos el programa
    except KeyboardInterrupt:
        # Si el usuario presiona "Ctrl+C", atrapamos el error feo y mostramos esto:
        print("\nPrograma interrumpido por el usuario.")