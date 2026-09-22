"""
Módulo de base de conocimiento.
Carga los archivos JSON (museos, reglas y patrones de intención) y expone
funciones de consulta/filtrado. No usa while ni switch: los filtros se
resuelven con comprensión de listas y las búsquedas con funciones puras.
"""

import json
import os

from src.utilidades import extraer_palabras, normalizar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def cargar_json(nombre_archivo):
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


# Se cargan una sola vez al importar el módulo.
MUSEOS = cargar_json("museos.json")["museos"]
REGLAS = cargar_json("reglas_recomendaciones.json")
INTENCIONES = cargar_json("intenciones.json")["intenciones"]


def _palabras_significativas(nombre):
    """Devuelve las palabras de más de 3 letras del nombre de un museo
    (sin acentos ni signos de puntuación), ignorando conectores como
    'de', 'del', 'la', etc."""
    return [p for p in extraer_palabras(nombre) if len(p) > 3]


def buscar_museo_por_nombre(texto):
    """Busca, dentro del texto del usuario, coincidencias con el nombre
    de algún museo del catálogo. Devuelve el primer museo que coincide
    o None si no encuentra ninguno."""
    palabras_texto = set(extraer_palabras(texto))
    coincidencias = [
        museo
        for museo in MUSEOS
        if palabras_texto & set(_palabras_significativas(museo["nombre"]))
    ]
    return coincidencias[0] if coincidencias else None


def filtrar_por_categoria(categoria):
    return [m for m in MUSEOS if m["categoria"] == categoria]


def filtrar_interactivos():
    return [m for m in MUSEOS if m["interactivo"]]


def filtrar_para_ninos():
    palabras_clave_edad = ("nino", "ninos", "familia", "infantil")
    return [
        m for m in MUSEOS
        if any(palabra in normalizar(m["edad_recomendada"]) for palabra in palabras_clave_edad)
        or m["interactivo"]
    ]


# Alias en lenguaje natural -> categoría real usada en museos.json.
# Así "cultura", "ciencias" o "artístico" se resuelven a la categoría
# correcta sin necesidad de if/elif repetidos por cada sinónimo.
CATEGORIA_ALIASES = {
    "historia": "historia",
    "arqueologia": "historia",
    "arqueologico": "historia",
    "prehispanico": "historia",
    "arte": "arte",
    "artistico": "arte",
    "pintura": "arte",
    "ciencia": "ciencia_interactivo",
    "ciencias": "ciencia_interactivo",
    "cientifico": "ciencia_interactivo",
    "cientificos": "ciencia_interactivo",
    "tecnologia": "ciencia_interactivo",
    "interactivo": "ciencia_interactivo",
    "interactivos": "ciencia_interactivo",
    "tematico": "tematico",
    "tematicos": "tematico",
    "cultura": "tematico",
    "cultural": "tematico",
    "especializado": "tematico",
}


def resolver_categoria_desde_texto(texto):
    """Busca en el texto alguna palabra que sea alias de una categoría
    (ej. 'cultura' -> 'tematico', 'ciencias' -> 'ciencia_interactivo')."""
    palabras = set(extraer_palabras(texto))
    coincidencias = [categoria for alias, categoria in CATEGORIA_ALIASES.items() if alias in palabras]
    return coincidencias[0] if coincidencias else None


def filtrar_combinado(categoria=None, para_ninos=False):
    """Filtra el catálogo por categoría y/o edad (niños), combinando
    ambos criterios con comprensión de listas en vez de bucles anidados."""
    resultado = MUSEOS
    if categoria:
        resultado = [m for m in resultado if m["categoria"] == categoria]
    if para_ninos:
        palabras_clave_edad = ("nino", "ninos", "familia", "infantil")
        resultado = [
            m for m in resultado
            if m["interactivo"] or any(p in normalizar(m["edad_recomendada"]) for p in palabras_clave_edad)
        ]
    return resultado


def listar_nombres(museos):
    return ", ".join(m["nombre"] for m in museos) if museos else "no encontré museos con ese filtro"
