"""Funciones auxiliares de normalización de texto y utilidades varias."""

import re
import unicodedata
from urllib.parse import quote


def quitar_acentos(texto):
    """Convierte 'está', 'qué', 'niño' en 'esta', 'que', 'nino', para que
    el chatbot no falle si el usuario escribe sin tildes."""
    forma_normalizada = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in forma_normalizada if not unicodedata.combining(c))


def normalizar(texto):
    return quitar_acentos(texto.lower())


def extraer_palabras(texto):
    """Extrae solo palabras (sin comas, paréntesis, etc.)."""
    return re.findall(r"\w+", normalizar(texto))


def generar_link_maps(direccion):
    """Genera un link de Google Maps a partir de una dirección, para que
    el usuario pueda ubicar el museo con mayor precisión que con el
    nombre del metro/metrobús más cercano."""
    return f"https://www.google.com/maps/search/?api=1&query={quote(direccion)}"


def contiene_palabra_ninos(texto):
    palabras = set(extraer_palabras(texto))
    return bool(palabras & {"nino", "ninos", "familia", "infantil", "hijos", "hijo", "hija", "peque", "peques"})


def extraer_nombre(texto):
    """Detecta si el usuario se está presentando ('me llamo X' / 'mi
    nombre es X') y devuelve el nombre capitalizado, o None."""
    texto_normalizado = normalizar(texto)
    patrones = [r"me llamo (\w+)", r"mi nombre es (\w+)"]
    for patron in patrones:
        coincidencia = re.search(patron, texto_normalizado)
        if coincidencia:
            return coincidencia.group(1).capitalize()
    return None
