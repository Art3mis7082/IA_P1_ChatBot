"""
Motor de recomendaciones. Traduce las reglas descritas en
data/reglas_recomendaciones.json a una función con if/elif (nunca switch),
para no repetir la recomendación de vestimenta en cada museo.
"""

from src.conocimiento import REGLAS


def _buscar_recomendacion(condicion_buscada):
    coincidencia = [
        regla["recomendacion"]
        for regla in REGLAS["reglas_vestimenta"]
        if regla["condicion"] == condicion_buscada
    ]
    return coincidencia[0] if coincidencia else None


def recomendar_vestimenta(museo):
    if museo["al_aire_libre"]:
        return _buscar_recomendacion("al_aire_libre == true")
    elif museo["interactivo"]:
        return _buscar_recomendacion("interactivo == true")
    elif museo["categoria"] == "arte":
        return _buscar_recomendacion("categoria == 'arte'")
    elif museo["categoria"] == "historia":
        return _buscar_recomendacion("categoria == 'historia'")
    elif museo["categoria"] == "tematico":
        return _buscar_recomendacion("categoria == 'tematico'")
    else:
        return _buscar_recomendacion("default")


def restricciones_generales():
    return REGLAS["restricciones_generales"]
