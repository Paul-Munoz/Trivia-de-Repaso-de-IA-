"""
Puzzle Games Module - Juegos Mentales para Proyecto Alpha
Diferentes tipos de desafíos cognitivos para hacer pensar al jugador.
"""

import random
import time
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class PuzzleChallenge:
    """Estructura para un desafío de puzzle."""
    type: str
    title: str
    description: str
    content: Any
    solution: Any
    hints: List[str]
    difficulty: str
    time_limit: int = 60

class PuzzleGameManager:
    """Gestor de juegos mentales y rompecabezas."""
    
    def __init__(self):
        self.current_puzzle = None
        self.puzzle_history = []
        self.score_multiplier = {"easy": 1, "medium": 1.5, "hard": 2}
        
    def create_logic_puzzle(self, concept: str, difficulty: str = "medium") -> PuzzleChallenge:
        """Crea un rompecabezas de lógica basado en conceptos de IA."""
        puzzles = {
            "machine_learning": {
                "title": "🧩 El Laberinto del Aprendizaje",
                "description": "Conecta los conceptos en el orden correcto para que la máquina aprenda:",
                "sequence": ["Datos", "Algoritmo", "Entrenamiento", "Modelo", "Predicción"],
                "scrambled": ["Predicción", "Datos", "Modelo", "Algoritmo", "Entrenamiento"],
                "hints": [
                    "💡 Primero necesitas algo para alimentar al sistema...",
                    "🔍 Luego necesitas un método para procesar esa información...",
                    "⚡ El proceso de aprender requiere práctica..."
                ]
            },
            "neural_networks": {
                "title": "🕸️ La Red Neuronal Perdida",
                "description": "Reconstruye la red neuronal conectando las capas correctamente:",
                "pattern": ["Entrada", "Capa Oculta 1", "Capa Oculta 2", "Salida"],
                "connections": [(0,1), (1,2), (2,3)],
                "hints": [
                    "🧠 Las neuronas se conectan en capas...",
                    "➡️ La información fluye en una dirección...",
                    "🎯 La última capa da el resultado final..."
                ]
            }
        }
        
        puzzle_data = puzzles.get(concept, puzzles["machine_learning"])
        
        return PuzzleChallenge(
            type="logic_puzzle",
            title=puzzle_data["title"],
            description=puzzle_data["description"],
            content=puzzle_data,
            solution=puzzle_data.get("sequence", puzzle_data.get("pattern")),
            hints=puzzle_data["hints"],
            difficulty=difficulty,
            time_limit=90 if difficulty == "hard" else 60
        )
    
    def create_memory_test(self, concept: str, difficulty: str = "medium") -> PuzzleChallenge:
        """Crea un test de memoria sobre conceptos de IA."""
        memory_challenges = {
            "ai_definitions": {
                "title": "🧠 Memoria de Conceptos IA",
                "description": "Memoriza estas definiciones por 10 segundos, luego responde:",
                "items": [
                    ("Algoritmo", "Conjunto de reglas para resolver un problema"),
                    ("Big Data", "Grandes volúmenes de datos complejos"),
                    ("Deep Learning", "Aprendizaje con redes neuronales profundas"),
                    ("Overfitting", "Cuando el modelo memoriza en lugar de aprender")
                ],
                "questions": [
                    "¿Qué es un algoritmo?",
                    "¿Cómo se define Big Data?",
                    "¿Qué significa Deep Learning?",
                    "¿Qué es el Overfitting?"
                ]
            },
            "sequence_memory": {
                "title": "🔢 Secuencia de Procesamiento",
                "description": "Memoriza el orden de estos pasos de procesamiento de datos:",
                "sequence": ["Recolección", "Limpieza", "Análisis", "Modelado", "Validación", "Implementación"],
                "study_time": 15,
                "questions": ["¿Cuál es el paso después de 'Limpieza'?", "¿Qué viene antes de 'Implementación'?"]
            }
        }
        
        challenge_data = memory_challenges.get(concept, memory_challenges["ai_definitions"])
        
        return PuzzleChallenge(
            type="memory_test",
            title=challenge_data["title"],
            description=challenge_data["description"],
            content=challenge_data,
            solution=challenge_data.get("items", challenge_data.get("sequence")),
            hints=["🧠 Trata de crear asociaciones mentales", "🔄 Repite mentalmente la información"],
            difficulty=difficulty,
            time_limit=challenge_data.get("study_time", 10)
        )
    
    def create_riddle_challenge(self, concept: str, difficulty: str = "medium") -> PuzzleChallenge:
        """Crea adivinanzas y acertijos sobre IA."""
        riddles = {
            "machine_learning": [
                {
                    "riddle": "🤔 Soy un proceso que mejora con la experiencia, aprendo de los errores sin que me enseñen directamente. ¿Qué soy?",
                    "answer": "machine learning",
                    "options": ["Programación", "Machine Learning", "Base de datos", "Internet"],
                    "explanation": "El Machine Learning es exactamente eso: un sistema que mejora automáticamente con la experiencia."
                },
                {
                    "riddle": "🧩 Tengo capas como una cebolla, neuronas como un cerebro, pero soy artificial. ¿Qué soy?",
                    "answer": "red neuronal",
                    "options": ["Computadora", "Red Neuronal", "Algoritmo", "Programa"],
                    "explanation": "Las redes neuronales artificiales imitan la estructura del cerebro humano con capas de neuronas."
                }
            ],
            "data_science": [
                {
                    "riddle": "📊 Soy invisible pero valioso, me recolectan constantemente, sin mí la IA no puede funcionar. ¿Qué soy?",
                    "answer": "datos",
                    "options": ["Electricidad", "Datos", "Código", "Hardware"],
                    "explanation": "Los datos son el combustible de la inteligencia artificial."
                }
            ]
        }
        
        concept_riddles = riddles.get(concept, riddles["machine_learning"])
        selected_riddle = random.choice(concept_riddles)
        
        return PuzzleChallenge(
            type="riddle",
            title="🎭 Acertijo de IA",
            description="Resuelve este acertijo:",
            content=selected_riddle,
            solution=selected_riddle["answer"],
            hints=["🤔 Piensa en los conceptos básicos de IA", "💡 La respuesta está relacionada con el aprendizaje automático"],
            difficulty=difficulty
        )
    
    def create_pattern_puzzle(self, concept: str, difficulty: str = "medium") -> PuzzleChallenge:
        """Crea puzzles de patrones y secuencias."""
        patterns = {
            "algorithms": {
                "title": "🔍 Patrón de Algoritmos",
                "description": "Completa la secuencia de eficiencia algorítmica:",
                "sequence": ["O(1)", "O(log n)", "O(n)", "O(n log n)", "?"],
                "answer": "O(n²)",
                "options": ["O(n²)", "O(2n)", "O(n³)", "O(n!)"],
                "explanation": "La secuencia sigue la complejidad computacional común: constante, logarítmica, lineal, n log n, cuadrática."
            },
            "data_flow": {
                "title": "🌊 Flujo de Datos",
                "description": "¿Qué sigue en este flujo de procesamiento?",
                "sequence": ["Input → Preprocessing → Feature Extraction → ?"],
                "answer": "Model Training",
                "options": ["Model Training", "Data Storage", "User Interface", "Error Handling"],
                "explanation": "Después de extraer características, el siguiente paso lógico es entrenar el modelo."
            }
        }
        
        pattern_data = patterns.get(concept, patterns["algorithms"])
        
        return PuzzleChallenge(
            type="pattern_puzzle",
            title=pattern_data["title"],
            description=pattern_data["description"],
            content=pattern_data,
            solution=pattern_data["answer"],
            hints=["🔄 Busca la lógica en la progresión", "📈 Piensa en cómo aumenta la complejidad"],
            difficulty=difficulty
        )
    
    def get_random_puzzle(self, concept: str, difficulty: str = "medium") -> PuzzleChallenge:
        """Obtiene un puzzle aleatorio del tipo especificado."""
        puzzle_types = [
            self.create_logic_puzzle,
            self.create_memory_test,
            self.create_riddle_challenge,
            self.create_pattern_puzzle
        ]
        
        puzzle_creator = random.choice(puzzle_types)
        return puzzle_creator(concept, difficulty)
    
    def validate_solution(self, puzzle: PuzzleChallenge, user_answer: Any) -> Tuple[bool, str]:
        """Valida la solución del usuario."""
        if puzzle.type == "logic_puzzle":
            return self._validate_logic_puzzle(puzzle, user_answer)
        elif puzzle.type == "memory_test":
            return self._validate_memory_test(puzzle, user_answer)
        elif puzzle.type == "riddle":
            return self._validate_riddle(puzzle, user_answer)
        elif puzzle.type == "pattern_puzzle":
            return self._validate_pattern_puzzle(puzzle, user_answer)
        
        return False, "Tipo de puzzle no reconocido"
    
    def _validate_logic_puzzle(self, puzzle: PuzzleChallenge, user_answer: List) -> Tuple[bool, str]:
        """Valida un puzzle de lógica."""
        correct_sequence = puzzle.solution
        if user_answer == correct_sequence:
            return True, "¡Excelente! Has conectado los conceptos correctamente."
        else:
            return False, f"No es correcto. La secuencia correcta es: {' → '.join(correct_sequence)}"
    
    def _validate_memory_test(self, puzzle: PuzzleChallenge, user_answer: Dict) -> Tuple[bool, str]:
        """Valida un test de memoria."""
        correct_answers = puzzle.solution
        score = 0
        total = len(user_answer)
        
        for question, answer in user_answer.items():
            if any(answer.lower() in item[1].lower() for item in correct_answers):
                score += 1
        
        percentage = (score / total) * 100 if total > 0 else 0
        
        if percentage >= 70:
            return True, f"¡Muy bien! Recordaste correctamente {score}/{total} conceptos ({percentage:.0f}%)"
        else:
            return False, f"Necesitas recordar mejor. Solo {score}/{total} correctas ({percentage:.0f}%)"
    
    def _validate_riddle(self, puzzle: PuzzleChallenge, user_answer: str) -> Tuple[bool, str]:
        """Valida una adivinanza."""
        correct_answer = puzzle.solution.lower()
        user_answer_clean = user_answer.lower().strip()
        
        if correct_answer in user_answer_clean or user_answer_clean in correct_answer:
            return True, f"¡Correcto! {puzzle.content['explanation']}"
        else:
            return False, f"No es correcto. {puzzle.content['explanation']}"
    
    def _validate_pattern_puzzle(self, puzzle: PuzzleChallenge, user_answer: str) -> Tuple[bool, str]:
        """Valida un puzzle de patrones."""
        if user_answer.strip() == puzzle.solution:
            return True, f"¡Excelente! {puzzle.content['explanation']}"
        else:
            return False, f"Incorrecto. {puzzle.content['explanation']}"
    
    def get_hint(self, puzzle: PuzzleChallenge, hint_level: int = 0) -> str:
        """Obtiene una pista para el puzzle actual."""
        if hint_level < len(puzzle.hints):
            return puzzle.hints[hint_level]
        else:
            return "💡 ¡Ya has usado todas las pistas disponibles! Confía en tu conocimiento."
    
    def calculate_score(self, puzzle: PuzzleChallenge, time_taken: float, hints_used: int) -> int:
        """Calcula la puntuación basada en dificultad, tiempo y pistas usadas."""
        base_score = 100
        difficulty_multiplier = self.score_multiplier[puzzle.difficulty]
        
        # Penalización por tiempo (máximo 50% de reducción)
        time_penalty = min(0.5, time_taken / puzzle.time_limit)
        
        # Penalización por pistas (10% por pista)
        hint_penalty = hints_used * 0.1
        
        final_score = base_score * difficulty_multiplier * (1 - time_penalty - hint_penalty)
        return max(10, int(final_score))  # Mínimo 10 puntos

# Conceptos de IA para generar puzzles
AI_CONCEPTS = [
    "machine_learning", "neural_networks", "deep_learning", "algorithms",
    "data_science", "natural_language_processing", "computer_vision",
    "reinforcement_learning", "supervised_learning", "unsupervised_learning"
]

def get_concept_for_mission(mission_number: int) -> str:
    """Obtiene el concepto de IA correspondiente a una misión."""
    return AI_CONCEPTS[mission_number % len(AI_CONCEPTS)]