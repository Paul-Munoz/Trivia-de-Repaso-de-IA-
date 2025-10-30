"""
Learning Manager Module - Proyecto Alpha v4.0
Gestor de modos de aprendizaje adaptativos.
"""

from typing import Dict, Any


class LearningModeManager:
    """
    Gestor de modos de aprendizaje adaptativos.

    Adapta la dificultad, contenido y retroalimentación basado en el rendimiento
    del estudiante para optimizar el aprendizaje.
    """

    def __init__(self):
        """Inicializa el gestor de aprendizaje."""
        self.current_mode = "adaptive"
        self.difficulty_level = "normal"
        self.adaptive_parameters = {
            "performance_threshold": 0.7,
            "difficulty_adjustment_rate": 0.1,
            "hint_availability": True,
            "time_limits": True,
            "explanation_detail": "normal",
            "adaptive_difficulty": True,
            "feedback_intensity": "normal",
            "question_order": "sequential",
            "retry_policy": "allowed",
            "progress_tracking": True
        }

    def adapt_difficulty(self, metrics) -> None:
        """
        Adapta la dificultad basado en el rendimiento del estudiante.

        Args:
            metrics: Instancia de AcademicMetrics
        """
        if not self.adaptive_parameters["adaptive_difficulty"]:
            return

        accuracy = metrics.get_accuracy()

        if accuracy >= 0.85:
            self.difficulty_level = "dificil"
            self._apply_difficulty_settings("hard")
        elif accuracy >= 0.7:
            self.difficulty_level = "normal"
            self._apply_difficulty_settings("normal")
        else:
            self.difficulty_level = "facil"
            self._apply_difficulty_settings("easy")

    def _apply_difficulty_settings(self, level: str) -> None:
        """
        Aplica configuraciones específicas para cada nivel de dificultad.

        Args:
            level: Nivel de dificultad ("easy", "normal", "hard")
        """
        if level == "easy":
            self.adaptive_parameters.update({
                "hint_availability": True,
                "time_limits": False,
                "explanation_detail": "detailed",
                "feedback_intensity": "high",
                "retry_policy": "unlimited"
            })
        elif level == "normal":
            self.adaptive_parameters.update({
                "hint_availability": True,
                "time_limits": True,
                "explanation_detail": "normal",
                "feedback_intensity": "normal",
                "retry_policy": "allowed"
            })
        elif level == "hard":
            self.adaptive_parameters.update({
                "hint_availability": False,
                "time_limits": True,
                "explanation_detail": "minimal",
                "feedback_intensity": "low",
                "retry_policy": "limited"
            })

    def set_mode(self, mode: str) -> None:
        """
        Cambia el modo de aprendizaje (alias para set_learning_mode).

        Args:
            mode: Modo deseado ("adaptive", "quiz", "study", "review")
        """
        self.set_learning_mode(mode)

    def set_learning_mode(self, mode: str) -> None:
        """
        Cambia el modo de aprendizaje.

        Args:
            mode: Modo deseado ("adaptive", "quiz", "study", "review")
        """
        self.current_mode = mode

        # Configuraciones específicas por modo
        mode_configs = {
            "adaptive": {
                "adaptive_difficulty": True,
                "hint_availability": True,
                "time_limits": True,
                "explanation_detail": "normal",
                "question_order": "adaptive",
                "progress_tracking": True
            },
            "quiz": {
                "adaptive_difficulty": False,
                "hint_availability": False,
                "time_limits": True,
                "explanation_detail": "minimal",
                "question_order": "random",
                "progress_tracking": True
            },
            "study": {
                "adaptive_difficulty": False,
                "hint_availability": True,
                "time_limits": False,
                "explanation_detail": "detailed",
                "question_order": "sequential",
                "progress_tracking": True
            },
            "review": {
                "adaptive_difficulty": True,
                "hint_availability": True,
                "time_limits": False,
                "explanation_detail": "detailed",
                "question_order": "weakest_first",
                "progress_tracking": True
            }
        }

        if mode in mode_configs:
            self.adaptive_parameters.update(mode_configs[mode])

    def get_mode_settings(self) -> Dict[str, Any]:
        """
        Obtiene configuración actual del modo de aprendizaje.

        Returns:
            Diccionario con configuración actual
        """
        return {
            "mode": self.current_mode,
            "difficulty": self.difficulty_level,
            "parameters": self.adaptive_parameters.copy()
        }

    def should_show_hint(self, mission_id: int, metrics) -> bool:
        """
        Determina si se debe mostrar una pista para una misión.

        Args:
            mission_id: ID de la misión
            metrics: Instancia de AcademicMetrics

        Returns:
            True si se debe mostrar pista
        """
        if not self.adaptive_parameters["hint_availability"]:
            return False

        # Lógica adaptativa para pistas
        if self.current_mode == "study":
            return True  # Siempre mostrar en modo estudio
        elif self.current_mode == "quiz":
            return False  # Nunca mostrar en modo quiz
        else:
            # Modo adaptativo: mostrar basado en rendimiento
            accuracy = metrics.get_accuracy()
            return accuracy < 0.6  # Mostrar pistas si precisión baja

    def get_explanation_level(self, mission_id: int, metrics) -> str:
        """
        Determina el nivel de detalle de las explicaciones.

        Args:
            mission_id: ID de la misión
            metrics: Instancia de AcademicMetrics

        Returns:
            Nivel de explicación ("minimal", "normal", "detailed")
        """
        base_level = self.adaptive_parameters["explanation_detail"]

        if self.current_mode == "study":
            return "detailed"
        elif self.current_mode == "quiz":
            return "minimal"
        elif self.current_mode == "adaptive":
            # Adaptar basado en rendimiento
            accuracy = metrics.get_accuracy()
            if accuracy < 0.5:
                return "detailed"
            elif accuracy < 0.8:
                return "normal"
            else:
                return "minimal"

        return base_level

    def should_allow_retry(self, mission_id: int, current_retries: int, metrics) -> bool:
        """
        Determina si se permite reintentar una misión.

        Args:
            mission_id: ID de la misión
            current_retries: Número actual de reintentos
            metrics: Instancia de AcademicMetrics

        Returns:
            True si se permite reintento
        """
        policy = self.adaptive_parameters["retry_policy"]

        if policy == "unlimited":
            return True
        elif policy == "none":
            return False
        elif policy == "limited":
            return current_retries < 2  # Máximo 2 reintentos
        else:  # "allowed"
            return current_retries < 1  # Máximo 1 reintento

    def get_question_order(self, available_missions: list) -> list:
        """
        Determina el orden de presentación de las preguntas.

        Args:
            available_missions: Lista de IDs de misiones disponibles

        Returns:
            Lista ordenada de IDs de misiones
        """
        order_type = self.adaptive_parameters["question_order"]

        if order_type == "sequential":
            return sorted(available_missions)
        elif order_type == "random":
            import random
            missions_copy = available_missions.copy()
            random.shuffle(missions_copy)
            return missions_copy
        elif order_type == "weakest_first":
            # Ordenar por conceptos más débiles (simplificado)
            return sorted(available_missions)  # TODO: Implementar lógica real
        else:
            return available_missions

    def get_feedback_intensity(self, metrics) -> str:
        """
        Determina la intensidad de la retroalimentación.

        Args:
            metrics: Instancia de AcademicMetrics

        Returns:
            Intensidad de feedback ("low", "normal", "high")
        """
        base_intensity = self.adaptive_parameters["feedback_intensity"]

        if self.current_mode == "adaptive":
            accuracy = metrics.get_accuracy()
            if accuracy < 0.4:
                return "high"
            elif accuracy < 0.7:
                return "normal"
            else:
                return "low"

        return base_intensity

    def reset_adaptation(self) -> None:
        """Reinicia la adaptación para una nueva sesión."""
        self.difficulty_level = "normal"
        self.adaptive_parameters = {
            "performance_threshold": 0.7,
            "difficulty_adjustment_rate": 0.1,
            "hint_availability": True,
            "time_limits": True,
            "explanation_detail": "normal",
            "adaptive_difficulty": True,
            "feedback_intensity": "normal",
            "question_order": "sequential",
            "retry_policy": "allowed",
            "progress_tracking": True
        }