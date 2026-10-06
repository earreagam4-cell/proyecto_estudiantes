import re

def es_email_valido(email):
    """Verifica si un texto tiene formato de correo electrónico."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    return bool(re.match(patron, email))

# ===================== FUNCIONES DE CONSOLA (DISEÑO) =====================

def imprimir_titulo(texto):
    """Imprime un texto en color CYAN (azul claro) con saltos de línea."""
    print(f"\n\033[96m--- {texto} ---\033[0m")

def imprimir_exito(texto):
    """Imprime mensajes positivos en color VERDE."""
    print(f"\033[92m✔ Éxito: {texto}\033[0m")

def imprimir_error(texto):
    """Imprime mensajes de error en color ROJO."""
    print(f"\033[91m✖ Error: {texto}\033[0m")

def imprimir_info(texto):
    """Imprime mensajes informativos en color AMARILLO."""
    print(f"\033[93mℹ {texto}\033[0m")

def confirmar(mensaje):
    """Hace una pregunta de Sí/No y devuelve True o False."""
    while True:
        respuesta = input(f"\033[93m? {mensaje} (s/n): \033[0m").strip().lower()
        
        if respuesta == 's':
            return True
        elif respuesta == 'n':
            return False
        # Si escribe cualquier otra cosa, el bucle vuelve a empezar.