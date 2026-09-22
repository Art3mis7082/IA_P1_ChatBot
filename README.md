
# IA_P1_ChatBot
Práctica 1 para la clase de Inteligencia Artificial del semestre 2027-1.

Tema: Introducción a los agentes conversacionales: ELIZA

Profesor: Dr. José Fidel Urquiza Yllescas

- Lugar y fecha:
21 de septiembre de 2026

- Integrantes del equipo:

Almaraz García Beatriz
Castañeda Luna Valeria
Galicia Barragan Edson
Ordóñez Figueroa María Fernanda
Raya Ramírez Angel Adrián

# MuseoBot CDMX

Chatbot de línea de comandos, basado en reglas y expresiones regulares (sin IA generativa)sobre 8 museos de la Ciudad de México.

## Requisitos

- Python 3.9 o superior

## Instalación y uso

```bash
git clone <repositorio por ssh o https>
cd museobot_cdmx
python main.py
```

Escribe tus preguntas en lenguaje natural, por ejemplo:

- "¿Qué horario tiene el Museo del Templo Mayor?"
- "¿Cuánto cuesta el Papalote?"
- "¿Cómo llego a Universum?"
- "¿Qué me pongo para ir al Templo Mayor?"
- "Museos de arte"

Escribe "adiós" para terminar la conversación.

## Estructura del proyecto

```
museobot_cdmx/
├── data/
│   ├── museos.json #catálogo de 8 museos (base de conocimiento)
│   ├── reglas_recomendaciones.json #reglas de vestimenta y restricciones generales
│   └── intenciones.json #patrones regex para detectar la intención
├── src/
│   ├── utilidades.py #normalización de texto (quitar acentos)
│   ├── conocimiento.py #carga de JSON y funciones de búsqueda/filtrado
│   ├── patrones.py #detección de intención con expresiones regulares
│   ├── recomendaciones.py #motor de reglas (if/elif) para vestimenta
│   ├── respuestas.py #una función por intención + diccionario de despacho
│   └── chatbot.py #ciclo de conversación (recursión, no while)
├── main.py
└── README.md
```

## Enfoque técnico

- **Sin tokens de IA generativa:** el reconocimiento de intención usa
  expresiones regulares y coincidencia de palabras clave, no modelos
  de lenguaje.
- **Sin `switch`:** el diccionario `ACCIONES` en `respuestas.py` mapea
  cada intención a la función que la resuelve.
- **Sin `while`:** el ciclo de conversación en `chatbot.py` usa
  recursión controlada; termina al detectar la intención "despedida".
- **Sin bucles `for` explícitos para filtrar:** los filtros de museos
  usan comprensión de listas sobre el catálogo cargado desde JSON.

## Estado actual (primer avance)

Implementado: carga de datos, detección de intención, respuestas para
horario, precio, descuento, domingo gratis, transporte, exposición
temporal, comida, actividades, guías, duración, recomendaciones,
restricciones y filtros por categoría/edad.

Pendiente para siguientes entregas: más museos, manejo de errores de
entrada más robusto, mejorar estados de ultima entrada como memoria



