"""
Ciclo de conversación de MuseoBot.
En vez de un 'while True', la función se vuelve a invocar a sí misma al
final de cada turno que es como usar recursión controlada. 
El progreso de la charla se guarda en un diccionario "estado" 
(nombre del usuario, museo del que se está hablando, última intención 
y si el bot está esperando que el usuario diga su preferencia)
que viaja de llamada en llamada: es una máquina de estados simple,
 sin necesidad de while ni switch.
"""

from src.conocimiento import buscar_museo_por_nombre
from src.patrones import detectar_intencion
from src.respuestas import generar_respuesta, generar_recomendacion_personalizada
from src.utilidades import extraer_nombre

# Intenciones que NO tiene sentido "reutilizar" cuando el usuario solo
# menciona un museo nuevo sin repetir la pregunta (ej. "¿y del Universum?").
INTENCIONES_NO_REUTILIZABLES = {None, "saludo", "despedida", "pedir_recomendacion", "filtro_categoria", "filtro_edad"}


def crear_estado_inicial():
    return {
        "nombre": None,
        "museo_actual": None,
        "ultima_intencion": None,
        "esperando_preferencia": False,
    }


def ciclo_conversacion(estado=None):
    if estado is None:
        estado = crear_estado_inicial()

    entrada = input("Tú: ").strip()

    if entrada == "":
        print("MuseoBot: Escribe una pregunta, o 'adiós' para terminar.")
        return ciclo_conversacion(estado)

    nombre_detectado = extraer_nombre(entrada)
    if nombre_detectado:
        estado["nombre"] = nombre_detectado

    # Caso especial: el bot ya preguntó "¿qué tipo de museo te gustaría?"
    # y esta entrada es la respuesta con la preferencia del usuario.
    if estado["esperando_preferencia"]:
        respuesta, museo_recomendado = generar_recomendacion_personalizada(entrada, estado)
        print("MuseoBot:", respuesta)
        estado["esperando_preferencia"] = False
        estado["museo_actual"] = museo_recomendado
        estado["ultima_intencion"] = None
        return ciclo_conversacion(estado)

    intencion = detectar_intencion(entrada)
    museo_mencionado = buscar_museo_por_nombre(entrada)

    # Si el usuario solo cambia de museo sin repetir la pregunta
    # (ej. "cuánto cuesta el Papalote" -> "¿y del Universum?"), se
    # reutiliza la última intención con el nuevo museo.
    if intencion == "desconocido" and museo_mencionado is not None \
            and estado["ultima_intencion"] not in INTENCIONES_NO_REUTILIZABLES:
        intencion = estado["ultima_intencion"]

    if museo_mencionado is not None:
        estado["museo_actual"] = museo_mencionado

    respuesta = generar_respuesta(intencion, entrada, estado["museo_actual"], estado)
    print("MuseoBot:", respuesta)

    if intencion == "pedir_recomendacion":
        estado["esperando_preferencia"] = True
    elif intencion != "desconocido":
        estado["ultima_intencion"] = intencion

    if intencion == "despedida":
        return

    return ciclo_conversacion(estado)
