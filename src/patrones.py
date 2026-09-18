"""
Reconocimiento de intención mediante expresiones regulares.
No usa tokenización de IA: solo re.search sobre patrones definidos en
data/intenciones.json.
"""

import re
from src.conocimiento import INTENCIONES
from src.utilidades import normalizar


def detectar_intencion(texto):
    """Recorre la lista de intenciones y devuelve el id de la primera
    cuyo patrón haga match con el texto del usuario. El texto y los
    patrones se comparan sin acentos, para que 'que' y 'qué' (o 'adios'
    y 'adiós') se reconozcan igual."""
    texto_normalizado = normalizar(texto)
    coincidencias = [
        intento["id"]
        for intento in INTENCIONES
        if any(re.search(normalizar(patron), texto_normalizado) for patron in intento["patrones_regex"])
    ]
    return coincidencias[0] if coincidencias else "desconocido"
