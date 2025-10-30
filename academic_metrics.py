"""
Academic Metrics Module - Proyecto Alpha v4.0
Sistema avanzado de métricas académicas para evaluación educativa.
"""

import time
import statistics
import logging
from datetime import datetime
from collections import defaultdict


class AcademicMetrics:
    """
    Sistema avanzado de métricas académicas para evaluación educativa.

    Proporciona métricas detalladas de rendimiento, análisis de aprendizaje
    y evaluación comprehensiva del progreso estudiantil.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        """Inicializa el sistema de métricas académicas."""
        self.metrics = {
            "total_questions": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "hints_used": 0,
            "retries_used": 0,
            "time_spent": 0,
            "average_time_per_question": 0,
            "streak_current": 0,
            "streak_best": 0,
            "mastery_level": 0.0,
            "difficulty_progression": [],
            "concept_mastery": defaultdict(float),
            "learning_velocity": 0.0,
            "consistency_score": 0.0,
        }
        self.question_history = []
        self.session_start_time = time.time()

    def record_answer(self, mission_id: int, correct: bool, time_taken: float,
                     hints_used: bool = False, retried: bool = False) -> None:
        """
        Registra una respuesta con métricas detalladas.

        Args:
            mission_id: ID de la misión respondida
            correct: True si la respuesta fue correcta
            time_taken: Tiempo empleado en segundos
            hints_used: True si se usaron pistas
            retried: True si fue un reintento
        """
        self.metrics["total_questions"] += 1

        if correct:
            self.metrics["correct_answers"] += 1
            self.metrics["streak_current"] += 1
            if self.metrics["streak_current"] > self.metrics["streak_best"]:
                self.metrics["streak_best"] = self.metrics["streak_current"]
        else:
            self.metrics["incorrect_answers"] += 1
            self.metrics["streak_current"] = 0

        if hints_used:
            self.metrics["hints_used"] += 1
        if retried:
            self.metrics["retries_used"] += 1

        self.metrics["time_spent"] += time_taken

        # Calcular tiempo promedio
        if self.metrics["total_questions"] > 0:
            self.metrics["average_time_per_question"] = (
                self.metrics["time_spent"] / self.metrics["total_questions"]
            )

        # Registrar en historial
        self.question_history.append({
            "mission_id": mission_id,
            "correct": correct,
            "time_taken": time_taken,
            "hints_used": hints_used,
            "retried": retried,
            "timestamp": datetime.now().isoformat()
        })

        # Actualizar métricas derivadas
        self._update_derived_metrics()

    def _update_derived_metrics(self) -> None:
        """Actualiza métricas calculadas automáticamente."""
        total = self.metrics["total_questions"]
        correct = self.metrics["correct_answers"]

        if total > 0:
            accuracy = correct / total
            self.metrics["mastery_level"] = accuracy

            # Calcular consistencia (desviación estándar de respuestas correctas)
            if len(self.question_history) >= 5:
                recent_answers = [1 if q["correct"] else 0 for q in self.question_history[-10:]]
                if len(recent_answers) > 1:
                    self.metrics["consistency_score"] = 1 - (statistics.stdev(recent_answers) / 0.5)

            # Calcular velocidad de aprendizaje
            if len(self.question_history) >= 10:
                first_half = sum(1 for q in self.question_history[:len(self.question_history)//2] if q["correct"])
                second_half = sum(1 for q in self.question_history[len(self.question_history)//2:] if q["correct"])
                if first_half > 0:
                    self.metrics["learning_velocity"] = (second_half - first_half) / first_half

    def get_performance_report(self) -> dict:
        """
        Genera un reporte de rendimiento académico detallado.

        Returns:
            Diccionario con métricas de rendimiento clave
        """
        return {
            "accuracy": self.get_accuracy(),
            "mastery_level": self.metrics["mastery_level"],
            "average_time": self.metrics["average_time_per_question"],
            "streak_best": self.metrics["streak_best"],
            "consistency": self.metrics["consistency_score"],
            "learning_velocity": self.metrics["learning_velocity"],
            "hints_efficiency": self.get_hints_efficiency(),
            "time_efficiency": self.get_time_efficiency(),
        }

    def get_accuracy(self) -> float:
        """
        Calcula precisión general.

        Returns:
            Porcentaje de respuestas correctas (0.0 a 1.0)
        """
        total = self.metrics["total_questions"]
        return self.metrics["correct_answers"] / total if total > 0 else 0

    def get_hints_efficiency(self) -> float:
        """
        Calcula eficiencia en el uso de pistas.

        Returns:
            Eficiencia de pistas (1.0 = sin pistas, 0.0 = muchas pistas)
        """
        hints = self.metrics["hints_used"]
        total = self.metrics["total_questions"]
        if total == 0:
            return 1.0
        return 1 - (hints / total)

    def get_time_efficiency(self) -> float:
        """
        Calcula eficiencia temporal.

        Returns:
            Eficiencia temporal (0.0 a 1.0)
        """
        from config import ACADEMIC_CONFIG  # Import local para evitar circular imports
        avg_time = self.metrics["average_time_per_question"]
        target_time = ACADEMIC_CONFIG["time_limit_per_question"]
        if avg_time <= target_time:
            return 1.0
        return target_time / avg_time

    def reset_session(self) -> None:
        """Reinicia las métricas para una nueva sesión."""
        self.metrics = {
            "total_questions": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "hints_used": 0,
            "retries_used": 0,
            "time_spent": 0,
            "average_time_per_question": 0,
            "streak_current": 0,
            "streak_best": 0,
            "mastery_level": 0.0,
            "difficulty_progression": [],
            "concept_mastery": defaultdict(float),
            "learning_velocity": 0.0,
            "consistency_score": 0.0,
        }
        self.question_history = []
        self.session_start_time = time.time()