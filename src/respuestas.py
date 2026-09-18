"""
Generación de respuestas.
El diccionario ACCIONES sustituye al switch: mapea cada intención a la
función que arma la respuesta correspondiente. Todas las funciones de
ACCIONES reciben (texto, museo, estado) para poder personalizar con el
nombre del usuario cuando aplica.
"""

from src.conocimiento import (
    MUSEOS,
    filtrar_combinado,
    resolver_categoria_desde_texto,
    listar_nombres,
)
from src.recomendaciones import recomendar_vestimenta, restricciones_generales
from src.utilidades import generar_link_maps, contiene_palabra_ninos

MENSAJE_SIN_MUSEO = (
    "¿De qué museo quieres saber eso? Dime el nombre, por ejemplo "
    "\"Museo del Templo Mayor\" o \"MUNAL\"."
)


def responder_horario(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return f"{museo['nombre']} abre: {museo['dias_horario']}."


def responder_precio(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    precio = museo["precio_general"]
    if "general" in precio:
        return f"{museo['nombre']}: entrada general ${precio['general']} {precio['moneda']}."
    return (
        f"{museo['nombre']}: ${precio['nacionales_y_residentes']} {precio['moneda']} para "
        f"mexicanos/residentes y ${precio['extranjeros']} {precio['moneda']} para extranjeros."
    )


def responder_descuento(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return museo["descuento_estudiante"]["detalle"]


def responder_domingo_gratis(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return museo["gratis_domingo_mx"]["detalle"]


def responder_transporte(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    link_mapa = generar_link_maps(museo["direccion"])
    return (
        f"{museo['nombre']} está en {museo['direccion']}. Acceso: {museo['metro_cercano']}. "
        f"Para ubicarlo con precisión: {link_mapa}"
    )


def responder_expo_temporal(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return (
        f"No tengo la cartelera de exposiciones temporales en tiempo real, "
        f"pero puedes consultarla aquí: {museo['expo_temporal_url']}"
    )


def responder_comida(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    opciones = "; ".join(f"{c['nombre']} ({c['precio_aprox']})" for c in museo["comida_cercana"])
    return f"Cerca de {museo['nombre']}: {opciones}."


def responder_actividades(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return (
        f"Actividades registradas en {museo['nombre']}: {', '.join(museo['actividades'])}. "
        f"Para el detalle de salas o funciones vigentes, revisa: {museo['expo_temporal_url']}"
    )


def responder_guias(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return museo["guias_disponibles"]["detalle"]


def responder_duracion(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return f"El recorrido de {museo['nombre']} dura aproximadamente {museo['duracion_estimada']}."


def responder_recomendaciones(museo):
    if museo is None:
        return MENSAJE_SIN_MUSEO
    return recomendar_vestimenta(museo)


def responder_restricciones(museo):
    if museo is None:
        return "En general: " + "; ".join(restricciones_generales())
    return f"En {museo['nombre']} no está permitido: " + "; ".join(museo["restricciones"])


ETIQUETAS_CATEGORIA = {
    "historia": "historia",
    "arte": "arte",
    "ciencia_interactivo": "ciencia e interactivos",
    "tematico": "temáticos",
}


def responder_filtro_categoria(texto):
    categoria = resolver_categoria_desde_texto(texto)
    para_ninos = contiene_palabra_ninos(texto)
    museos_encontrados = filtrar_combinado(categoria=categoria, para_ninos=para_ninos)
    etiqueta = ETIQUETAS_CATEGORIA.get(categoria, "esa temática")
    sufijo_edad = " para niños/familias" if para_ninos else ""
    return f"Museos de {etiqueta}{sufijo_edad}: {listar_nombres(museos_encontrados)}"


def responder_filtro_edad(texto):
    categoria = resolver_categoria_desde_texto(texto)
    museos_encontrados = filtrar_combinado(categoria=categoria, para_ninos=True)
    sufijo_categoria = f" de {ETIQUETAS_CATEGORIA[categoria]}" if categoria else ""
    return f"Museos para niños/familias{sufijo_categoria}: {listar_nombres(museos_encontrados)}"


def responder_pedir_recomendacion(estado):
    nombre = estado.get("nombre") if estado else None
    saludo = f"¡Claro, {nombre}!" if nombre else "¡Claro!"
    return (
        f"{saludo} ¿Tienes alguna idea de qué tipo de museo te gustaría? Podría ser "
        "interactivo, cultural, artístico, científico o de historia, y dime si es "
        "para niños o para todas las edades."
    )


def generar_recomendacion_personalizada(entrada, estado):
    """Se usa cuando el bot ya preguntó la preferencia del usuario y esta
    entrada es la respuesta. Devuelve (mensaje, museo_recomendado)."""
    categoria = resolver_categoria_desde_texto(entrada)
    para_ninos = contiene_palabra_ninos(entrada)
    candidatos = filtrar_combinado(categoria=categoria, para_ninos=para_ninos)

    if not candidatos:
        mensaje = (
            "No encontré un museo que combine exactamente eso. ¿Te muestro opciones "
            "de arte, historia, ciencia interactiva o temáticas?"
        )
        return mensaje, estado.get("museo_actual")

    museo_elegido = candidatos[0]
    nombre = estado.get("nombre")
    saludo = f"Perfecto, {nombre}." if nombre else "Perfecto."
    mensaje = (
        f"{saludo} Te recomiendo el {museo_elegido['nombre']}. ¿Tienes alguna pregunta "
        "sobre este museo? Por ejemplo horario, precio, actividades o cómo llegar."
    )
    return mensaje, museo_elegido


def responder_saludo(estado):
    nombre = estado.get("nombre") if estado else None
    saludo_personal = f"¡Hola, {nombre}!" if nombre else "¡Hola!"
    return (
        f"{saludo_personal} Soy MuseoBot CDMX y te ayudo a elegir tu próximo museo en la "
        "ciudad. Puedes pedirme una recomendación por categoría (arte, historia, ciencia, "
        "interactivo) o preguntarme directamente por horario, precio, transporte, comida "
        "o actividades de alguno de estos museos: "
        + ", ".join(m["nombre"] for m in MUSEOS)
        + "."
    )


def responder_despedida(estado):
    nombre = estado.get("nombre") if estado else None
    return f"¡Que disfrutes tu visita, {nombre}! Hasta luego." if nombre else "¡Que disfrutes tu visita! Hasta luego."


def responder_desconocido(_texto):
    return (
        "No entendí bien. Puedes preguntarme por horario, precio, transporte, comida, "
        "actividades o recomendaciones de un museo, o pedirme que te recomiende uno."
    )


# Diccionario de despacho: sustituye al switch.
# Cada función recibe (texto_usuario, museo_en_contexto, estado).
ACCIONES = {
    "horario": lambda texto, museo, estado: responder_horario(museo),
    "precio": lambda texto, museo, estado: responder_precio(museo),
    "descuento": lambda texto, museo, estado: responder_descuento(museo),
    "domingo_gratis": lambda texto, museo, estado: responder_domingo_gratis(museo),
    "transporte": lambda texto, museo, estado: responder_transporte(museo),
    "expo_temporal": lambda texto, museo, estado: responder_expo_temporal(museo),
    "comida": lambda texto, museo, estado: responder_comida(museo),
    "actividades": lambda texto, museo, estado: responder_actividades(museo),
    "guias": lambda texto, museo, estado: responder_guias(museo),
    "duracion": lambda texto, museo, estado: responder_duracion(museo),
    "recomendaciones": lambda texto, museo, estado: responder_recomendaciones(museo),
    "restricciones": lambda texto, museo, estado: responder_restricciones(museo),
    "filtro_categoria": lambda texto, museo, estado: responder_filtro_categoria(texto),
    "filtro_edad": lambda texto, museo, estado: responder_filtro_edad(texto),
    "pedir_recomendacion": lambda texto, museo, estado: responder_pedir_recomendacion(estado),
    "saludo": lambda texto, museo, estado: responder_saludo(estado),
    "despedida": lambda texto, museo, estado: responder_despedida(estado),
}


def generar_respuesta(intencion, texto, museo, estado):
    accion = ACCIONES.get(intencion)
    if accion is None:
        return responder_desconocido(texto)
    return accion(texto, museo, estado)
