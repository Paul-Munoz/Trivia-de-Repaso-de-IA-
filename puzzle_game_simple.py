"""
Juego de Puzzles Mentales - Versión Simple y Funcional
Sistema de desafíos cognitivos integrado con la UI existente.
"""

import tkinter as tk
from tkinter import messagebox
import random
import time
from typing import Dict, List

class PuzzleGame:
    """Juego de puzzles mentales simple."""
    
    def __init__(self, ui_manager):
        self.ui_manager = ui_manager
        self.current_puzzle = None
        self.puzzle_score = 0
        self.puzzles_completed = 0
        self.start_time = None
        
        # Puzzles predefinidos
        self.puzzles = self._create_puzzles()
    
    def _create_puzzles(self) -> List[Dict]:
        """Crea la lista de puzzles."""
        return [
            {
                "title": "🧠 Test de Memoria: Conceptos IA",
                "story": "MEMORIZA (10 segundos):\n\n📌 Machine Learning = Algoritmos que aprenden automáticamente\n📌 Deep Learning = Redes neuronales profundas\n📌 Big Data = Conjuntos de datos masivos\n📌 Overfitting = Memorizar en lugar de generalizar\n\n⏰ ¿Qué es Deep Learning?",
                "options": {
                    "Algoritmos que aprenden automáticamente": "Eso es Machine Learning",
                    "Redes neuronales profundas": "¡Correcto! Deep Learning usa redes neuronales con múltiples capas",
                    "Conjuntos de datos masivos": "Eso es Big Data",
                    "Memorizar en lugar de generalizar": "Eso es Overfitting"
                },
                "answer": "Redes neuronales profundas",
                "type": "memory"
            },
            {
                "title": "🧩 Rompecabezas: Flujo de IA",
                "story": "🔗 CONECTA EN ORDEN CORRECTO:\n\nElementos de un sistema de IA:\n• Datos de entrada\n• Algoritmo de procesamiento\n• Modelo entrenado\n• Predicción de salida\n\n¿Cuál es el flujo correcto?",
                "options": {
                    "Datos → Algoritmo → Modelo → Predicción": "¡Perfecto! Este es el flujo lógico de la IA",
                    "Algoritmo → Datos → Predicción → Modelo": "No, los datos van primero",
                    "Modelo → Predicción → Datos → Algoritmo": "No, el modelo se crea después",
                    "Predicción → Modelo → Algoritmo → Datos": "No, la predicción es el resultado final"
                },
                "answer": "Datos → Algoritmo → Modelo → Predicción",
                "type": "logic"
            },
            {
                "title": "🎭 Adivinanza: ¿Qué soy?",
                "story": "🤔 RESUELVE EL ACERTIJO:\n\n'Aprendo de la experiencia sin programación directa,\nmejoro mi rendimiento con más datos,\npuedo predecir el futuro basándome en el pasado,\ny soy la base de la inteligencia artificial moderna.'\n\n¿Qué soy?",
                "options": {
                    "Una base de datos": "No, solo almacena información",
                    "Machine Learning": "¡Correcto! El ML aprende de datos automáticamente",
                    "Un programa normal": "No, los programas siguen reglas fijas",
                    "Internet": "No, es una red de comunicación"
                },
                "answer": "Machine Learning",
                "type": "riddle"
            },
            {
                "title": "🔍 Patrón: Complejidad Algorítmica",
                "story": "📈 COMPLETA LA SECUENCIA:\n\nComplejidad computacional:\nO(1) → O(log n) → O(n) → O(n log n) → ?\n\n¿Qué sigue en esta progresión?",
                "options": {
                    "O(n²)": "¡Correcto! Sigue: constante, log, lineal, n log n, cuadrática",
                    "O(2n)": "No, O(2n) = O(n), no es el siguiente",
                    "O(n!)": "No, factorial es mucho más complejo",
                    "O(n³)": "No, cúbica viene después de cuadrática"
                },
                "answer": "O(n²)",
                "type": "pattern"
            },
            {
                "title": "🧠 Memoria: Secuencia de Datos",
                "story": "ESTUDIA esta secuencia:\n\n1️⃣ Recolección\n2️⃣ Limpieza\n3️⃣ Análisis\n4️⃣ Entrenamiento\n5️⃣ Validación\n6️⃣ Implementación\n\n❓ ¿Qué viene después de 'Análisis'?",
                "options": {
                    "Limpieza": "No, eso es el paso 2",
                    "Entrenamiento": "¡Correcto! Después del análisis viene el entrenamiento",
                    "Validación": "No, eso es el paso 5",
                    "Recolección": "No, eso es el primer paso"
                },
                "answer": "Entrenamiento",
                "type": "memory"
            },
            {
                "title": "🕸️ Lógica: Red Neuronal",
                "story": "🧠 ARQUITECTURA NEURONAL:\n\nCapas de una red neuronal:\n• Entrada (Input)\n• Oculta 1\n• Oculta 2\n• Salida (Output)\n\n¿Cómo fluye la información?",
                "options": {
                    "Input → Oculta1 → Oculta2 → Output": "¡Excelente! Flujo hacia adelante capa por capa",
                    "Output → Oculta2 → Oculta1 → Input": "No, eso sería flujo inverso",
                    "Input → Output → Oculta1 → Oculta2": "No, las ocultas procesan antes",
                    "Todas conectadas entre sí": "No, el flujo es secuencial"
                },
                "answer": "Input → Oculta1 → Oculta2 → Output",
                "type": "logic"
            },
            {
                "title": "🎭 Acertijo: Cerebro Artificial",
                "story": "🤖 ADIVINANZA NEURONAL:\n\n'Tengo capas como una cebolla,\nneuronas como un cerebro,\npero soy completamente artificial.\nProceso en paralelo y aprendo ajustando conexiones.'\n\n¿Qué soy?",
                "options": {
                    "Una computadora": "No, las computadoras no tienen 'neuronas'",
                    "Red neuronal artificial": "¡Perfecto! Imita el cerebro con capas de neuronas",
                    "Un algoritmo simple": "No, no tiene estructura neuronal",
                    "Un robot": "No, eso es hardware físico"
                },
                "answer": "Red neuronal artificial",
                "type": "riddle"
            },
            {
                "title": "🔍 Patrón: Pipeline de Datos",
                "story": "🌊 FLUJO DE PROCESAMIENTO:\n\nPipeline típico:\nInput → Preprocessing → Feature Extraction → ?\n\n¿Cuál es el siguiente paso lógico?",
                "options": {
                    "Model Training": "¡Excelente! Después de extraer características viene entrenamiento",
                    "Data Storage": "No, almacenamiento no es procesamiento",
                    "User Interface": "No, UI es para mostrar resultados",
                    "Error Handling": "No, eso es transversal"
                },
                "answer": "Model Training",
                "type": "pattern"
            }
        ]
    
    def get_puzzle(self, puzzle_num: int) -> Dict:
        """Obtiene un puzzle específico."""
        return self.puzzles[puzzle_num % len(self.puzzles)]
    
    def start_puzzle(self, puzzle_num: int):
        """Inicia un puzzle."""
        self.current_puzzle = self.get_puzzle(puzzle_num)
        self.start_time = time.time()
        
        # Actualizar UI
        self.ui_manager.mission_title_label.config(text=self.current_puzzle["title"])
        self.ui_manager.story_text_var.set(self.current_puzzle["story"])
        
        # Crear opciones
        self.ui_manager.clear_options()
        fake_mission = {
            "options": self.current_puzzle["options"],
            "answer": self.current_puzzle["answer"]
        }
        self.ui_manager.create_option_buttons(fake_mission, self.handle_answer)
        
        # Feedback inicial
        puzzle_type = self.current_puzzle["type"].title()
        self.ui_manager.feedback_text_var.set(f"🧠 Desafío Mental: {puzzle_type}\nUsa tu lógica para resolver este puzzle.")
    
    def handle_answer(self, selected_option: str, option_widget):
        """Maneja la respuesta del puzzle."""
        is_correct = selected_option == self.current_puzzle["answer"]
        time_taken = time.time() - self.start_time if self.start_time else 0
        
        if is_correct:
            self.puzzle_score += 10
            self.puzzles_completed += 1
            
            feedback = f"✅ ¡EXCELENTE! Respuesta correcta.\n\n"
            feedback += f"🎯 {self.current_puzzle['options'][selected_option]}\n\n"
            feedback += f"🧠 Tipo: {self.current_puzzle['type'].title()}\n"
            feedback += f"⏱️ Tiempo: {time_taken:.1f}s\n"
            feedback += f"🏆 Puntuación: +10 puntos"
            
        else:
            feedback = f"❌ No es correcto, ¡pero sigue intentando!\n\n"
            feedback += f"🔴 Tu respuesta: {selected_option}\n"
            feedback += f"✅ Respuesta correcta: {self.current_puzzle['answer']}\n\n"
            feedback += f"💡 {self.current_puzzle['options'][self.current_puzzle['answer']]}\n\n"
            feedback += "💪 ¡Los puzzles requieren práctica!"
        
        self.ui_manager.feedback_text_var.set(feedback)
        return is_correct
    
    def get_hint(self) -> str:
        """Obtiene una pista para el puzzle actual."""
        if not self.current_puzzle:
            return "💡 No hay puzzle activo"
        
        puzzle_type = self.current_puzzle["type"]
        hints = {
            "memory": "🧠 Trata de recordar las definiciones que memorizaste",
            "logic": "🔗 Piensa en el orden lógico de los procesos",
            "riddle": "🤔 Lee la descripción cuidadosamente, la respuesta está ahí",
            "pattern": "📈 Observa cómo aumenta la complejidad en la secuencia"
        }
        return hints.get(puzzle_type, "💡 Piensa en los conceptos básicos de IA")
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del juego."""
        return {
            "score": self.puzzle_score,
            "completed": self.puzzles_completed,
            "total": len(self.puzzles)
        }