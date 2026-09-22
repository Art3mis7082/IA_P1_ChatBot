"""
Para ejecutar el chatbot, usa el comando: python main.py
"""

from src.chatbot import ciclo_conversacion

if __name__ == "__main__":
    print(
        "MuseoBot: ¡Hola! Soy MuseoBot. Estoy aquí para ayudarte a elegir el próximo museo que podras visitar en la "
        "Ciudad de México. Puedes pedirme una recomendación por categoría o temática "
        "(arte, historia, ciencia, interactivo), o preguntarme directamente por el "
        "horario, precio, transporte, comida o actividades de un museo. Escribe "
        "'adiós' para salir.\n"
    )
    ciclo_conversacion()
