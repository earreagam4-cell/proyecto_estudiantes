# Importamos la librería 're' (Expresiones Regulares) para validar patrones de texto complejos.
import re

def es_email_valido(email):
    """Verifica si un texto tiene formato de correo electrónico."""
    # Definimos un patrón: letras/números + @ + letras/números + . + letras (2 a 4 caracteres)
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
    # re.match compara el email ingresado con el patrón. 
    # Devuelve True si coincide (es válido) o False si no tiene forma de correo.
    return bool(re.match(patron, email))

# ===================== FUNCIONES DE CONSOLA (DISEÑO) =====================
# Usamos códigos ANSI para darle color al texto en la terminal.
# \033[ es el inicio del código, el número es el color, m cierra el código, y \033[0m resetea el color.

def imprimir_titulo(texto):
    """Imprime un texto en color CYAN (azul claro) con saltos de línea."""
    # \n hace un salto de línea antes del título.
    # \033[96m pone el texto cyan, y \033[0m lo devuelve a la normalidad.
    print(f"\n\033[96m--- {texto} ---\033[0m")

def imprimir_exito(texto):
    """Imprime mensajes positivos en color VERDE."""
    # \033[92m es el código para verde brillante. ✔ es un adorno.
    print(f"\033[92m✔ Éxito: {texto}\033[0m")

def imprimir_error(texto):
    """Imprime mensajes de error en color ROJO."""
    # \033[91m es el código para rojo brillante. ✖ es un adorno.
    print(f"\033[91m✖ Error: {texto}\033[0m")

def imprimir_info(texto):
    """Imprime mensajes informativos en color AMARILLO."""
    # \033[93m es el código para amarillo. ℹ es un adorno.
    print(f"\033[93mℹ {texto}\033[0m")

def confirmar(mensaje):
    """Hace una pregunta de Sí/No y devuelve True o False."""
    # Se repite infinitamente hasta que el usuario responda bien.
    while True:
        # Pedimos el input, quitamos espacios (.strip()) y lo pasamos a minúsculas (.lower())
        respuesta = input(f"\033[93m? {mensaje} (s/n): \033[0m").strip().lower()
        
        # Si la respuesta es 's', devolvemos True (Confirmado)
        if respuesta == 's':
            return True
        # Si la respuesta es 'n', devolvemos False (Cancelado)
        elif respuesta == 'n':
            return False
        # Si escribe cualquier otra cosa, el bucle vuelve a empezar.