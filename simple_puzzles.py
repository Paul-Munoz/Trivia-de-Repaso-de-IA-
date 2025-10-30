"""
Simple Puzzles - Versión simplificada de juegos mentales
Integración directa con el sistema existente.
"""

import random
from typing import Dict, List, Any

class SimplePuzzle:
    """Puzzle simple que funciona con la UI existente."""
    
    def __init__(self, title: str, story: str, options: Dict[str, str], answer: str, 
                 puzzle_type: str = "riddle", hints: List[str] = None):
        self.title = title
        self.story = story
        self.options = options
        self.answer = answer
        self.puzzle_type = puzzle_type
        self.hints = hints or ["💡 Piensa en los conceptos básicos de IA"]

def create_memory_puzzle(mission_num: int) -> SimplePuzzle:
    """Crea un puzzle de memoria."""
    memory_puzzles = [
        {
            "title": "🧠 Test de Memoria: Definiciones de IA",
            "story": "FASE DE ESTUDIO (10 segundos):\n\n📌 Machine Learning: Algoritmos que mejoran automáticamente con la experiencia\n📌 Deep Learning: Redes neuronales con múltiples capas ocultas\n📌 Overfitting: Cuando el modelo memoriza en lugar de generalizar\n📌 Big Data: Conjuntos de datos extremadamente grandes y complejos\n\n⏰ Tiempo terminado. ¿Qué definición corresponde a 'Deep Learning'?",
            "options": {
                "Algoritmos que mejoran automáticamente": "Esto es Machine Learning, no Deep Learning",
                "Redes neuronales con múltiples capas": "¡Correcto! Deep Learning usa redes neuronales profundas",
                "Cuando el modelo memoriza datos": "Esto describe el Overfitting",
                "Conjuntos de datos muy grandes": "Esto es Big Data"
            },
            "answer": "Redes neuronales con múltiples capas"
        },
        {
            "title": "🧠 Secuencia de Procesamiento de Datos",
            "story": "MEMORIZA esta secuencia de procesamiento:\n\n1️⃣ Recolección de datos\n2️⃣ Limpieza de datos\n3️⃣ Análisis exploratorio\n4️⃣ Entrenamiento del modelo\n5️⃣ Validación\n6️⃣ Implementación\n\n❓ ¿Qué paso viene DESPUÉS de 'Análisis exploratorio'?",
            "options": {
                "Limpieza de datos": "No, eso viene antes del análisis",
                "Entrenamiento del modelo": "¡Correcto! Después del análisis viene el entrenamiento",
                "Validación": "No, la validación viene después del entrenamiento",
                "Recolección de datos": "No, eso es el primer paso"
            },
            "answer": "Entrenamiento del modelo"
        }
    ]
    
    puzzle_data = memory_puzzles[mission_num % len(memory_puzzles)]
    return SimplePuzzle(
        title=puzzle_data["title"],
        story=puzzle_data["story"],
        options=puzzle_data["options"],
        answer=puzzle_data["answer"],
        puzzle_type="memory"
    )

def create_logic_puzzle(mission_num: int) -> SimplePuzzle:
    """Crea un puzzle de lógica."""
    logic_puzzles = [
        {
            "title": "🧩 Rompecabezas: Conecta los Conceptos",
            "story": "🔗 DESAFÍO DE LÓGICA:\n\nTienes estos elementos de un sistema de IA:\n• Datos de entrada\n• Algoritmo de procesamiento  \n• Modelo entrenado\n• Predicción de salida\n\n🤔 ¿Cuál es el ORDEN CORRECTO del flujo de información?",
            "options": {
                "Datos → Algoritmo → Modelo → Predicción": "¡Perfecto! Este es el flujo lógico correcto de la IA",
                "Algoritmo → Datos → Predicción → Modelo": "No, los datos deben procesarse antes de generar predicciones",
                "Modelo → Datos → Algoritmo → Predicción": "No, el modelo se crea después de procesar los datos",
                "Predicción → Modelo → Datos → Algoritmo": "No, las predicciones son el resultado final"
            },
            "answer": "Datos → Algoritmo → Modelo → Predicción"
        },
        {
            "title": "🕸️ Red Neuronal: Conecta las Capas",
            "story": "🧠 PUZZLE DE ARQUITECTURA:\n\nUna red neuronal tiene estas capas:\n• Capa de entrada (Input)\n• Capa oculta 1\n• Capa oculta 2  \n• Capa de salida (Output)\n\n⚡ ¿Cómo fluye la información en una red neuronal?",
            "options": {
                "Input → Oculta1 → Oculta2 → Output": "¡Excelente! La información fluye hacia adelante capa por capa",
                "Output → Oculta2 → Oculta1 → Input": "No, esto sería flujo hacia atrás (backpropagation)",
                "Input → Output → Oculta1 → Oculta2": "No, las capas ocultas procesan antes de la salida",
                "Todas las capas se conectan entre sí": "No, en redes feedforward el flujo es secuencial"
            },
            "answer": "Input → Oculta1 → Oculta2 → Output"
        }
    ]
    
    puzzle_data = logic_puzzles[mission_num % len(logic_puzzles)]
    return SimplePuzzle(
        title=puzzle_data["title"],
        story=puzzle_data["story"],
        options=puzzle_data["options"],
        answer=puzzle_data["answer"],
        puzzle_type="logic"
    )

def create_riddle_puzzle(mission_num: int) -> SimplePuzzle:
    """Crea un acertijo."""
    riddles = [
        {
            "title": "🎭 Acertijo: ¿Qué soy?",
            "story": "🤔 ADIVINANZA DE IA:\n\n'Soy un proceso que aprende de la experiencia,\nno me programan directamente con reglas,\nmejoro mi rendimiento con más datos,\ny puedo hacer predicciones sobre el futuro.\n\n¿Qué soy?'",
            "options": {
                "Una base de datos": "No, las bases de datos solo almacenan información",
                "Machine Learning": "¡Correcto! El ML aprende de datos sin programación explícita",
                "Un programa tradicional": "No, los programas tradicionales siguen reglas fijas",
                "Internet": "No, Internet es una red de comunicación"
            },
            "answer": "Machine Learning"
        },
        {
            "title": "🎭 Acertijo: El Cerebro Artificial",
            "story": "🧠 ADIVINANZA NEURONAL:\n\n'Tengo capas como una cebolla,\nneuronas como un cerebro,\npero soy completamente artificial.\nProceso información en paralelo,\ny aprendo ajustando mis conexiones.\n\n¿Qué soy?'",
            "options": {
                "Una computadora normal": "No, las computadoras normales no tienen 'neuronas'",
                "Una red neuronal artificial": "¡Perfecto! Las redes neuronales imitan el cerebro con capas",
                "Un algoritmo simple": "No, los algoritmos simples no tienen estructura neuronal",
                "Un robot": "No, un robot es el hardware, no la arquitectura de procesamiento"
            },
            "answer": "Una red neuronal artificial"
        }
    ]
    
    riddle_data = riddles[mission_num % len(riddles)]
    return SimplePuzzle(
        title=riddle_data["title"],
        story=riddle_data["story"],
        options=riddle_data["options"],
        answer=riddle_data["answer"],
        puzzle_type="riddle"
    )

def create_pattern_puzzle(mission_num: int) -> SimplePuzzle:
    """Crea un puzzle de patrones."""
    patterns = [
        {
            "title": "🔍 Patrón: Complejidad Algorítmica",
            "story": "📈 SECUENCIA DE COMPLEJIDAD:\n\nObserva esta secuencia de eficiencia algorítmica:\nO(1) → O(log n) → O(n) → O(n log n) → ?\n\n🧮 ¿Qué sigue en el patrón de complejidad computacional?",
            "options": {
                "O(n²)": "¡Correcto! Sigue la progresión: constante, log, lineal, n log n, cuadrática",
                "O(2n)": "No, O(2n) es equivalente a O(n), no sigue la progresión",
                "O(n!)": "No, factorial es mucho más complejo, no el siguiente paso",
                "O(n³)": "No, cúbica viene después de cuadrática"
            },
            "answer": "O(n²)"
        },
        {
            "title": "🌊 Patrón: Flujo de Datos",
            "story": "🔄 PIPELINE DE PROCESAMIENTO:\n\nSigue este flujo típico de datos en IA:\nInput → Preprocessing → Feature Extraction → ?\n\n🎯 ¿Cuál es el siguiente paso lógico en el pipeline?",
            "options": {
                "Model Training": "¡Excelente! Después de extraer características viene el entrenamiento",
                "Data Storage": "No, el almacenamiento no es el siguiente paso del procesamiento",
                "User Interface": "No, la interfaz es para mostrar resultados finales",
                "Error Handling": "No, el manejo de errores es transversal, no un paso específico"
            },
            "answer": "Model Training"
        }
    ]
    
    pattern_data = patterns[mission_num % len(patterns)]
    return SimplePuzzle(
        title=pattern_data["title"],
        story=pattern_data["story"],
        options=pattern_data["options"],
        answer=pattern_data["answer"],
        puzzle_type="pattern"
    )

def get_random_puzzle(mission_num: int) -> SimplePuzzle:
    """Obtiene un puzzle aleatorio."""
    puzzle_types = [
        create_memory_puzzle,
        create_logic_puzzle, 
        create_riddle_puzzle,
        create_pattern_puzzle
    ]
    
    # Usar el número de misión para determinismo pero con variedad
    puzzle_creator = puzzle_types[mission_num % len(puzzle_types)]
    return puzzle_creator(mission_num)

def validate_puzzle_answer(puzzle: SimplePuzzle, user_answer: str) -> tuple[bool, str]:
    """Valida la respuesta del puzzle."""
    is_correct = user_answer == puzzle.answer
    
    if is_correct:
        feedback = f"✅ ¡EXCELENTE! Respuesta correcta.\n\n"
        feedback += f"🎯 {puzzle.options[user_answer]}\n\n"
        feedback += f"🧠 Tipo de desafío: {puzzle.puzzle_type.title()}\n"
        feedback += "¡Sigue así, tu mente está trabajando genial!"
    else:
        feedback = f"❌ No es correcto, pero ¡sigue intentando!\n\n"
        feedback += f"🔴 Tu respuesta: {user_answer}\n"
        feedback += f"✅ Respuesta correcta: {puzzle.answer}\n\n"
        feedback += f"💡 Explicación: {puzzle.options[puzzle.answer]}\n\n"
        feedback += "💪 ¡Los puzzles mentales requieren práctica!"
    
    return is_correct, feedback