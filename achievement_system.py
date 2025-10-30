"""
Achievement System Module - Proyecto Alpha v4.0
Sistema avanzado de logros y gamificación educativa.
"""

from typing import List, Dict, Callable, Any


class AchievementSystem:
    """
    Sistema avanzado de logros y gamificación educativa.

    Gestiona logros desbloqueables, verifica condiciones de cumplimiento
    y proporciona retroalimentación motivacional al estudiante.
    """

    def __init__(self):
        """Inicializa el sistema de logros."""
        self.achievements = []
        self.unlocked_achievements = set()
        self.achievement_definitions = self._define_achievements()

    def _define_achievements(self) -> Dict[str, Dict[str, Any]]:
        """
        Define todos los logros disponibles en el sistema.

        Returns:
            Diccionario con definiciones de logros
        """
        return {
            "first_victory": {
                "name": "🏆 Primera Victoria",
                "description": "Has completado tu primera misión correctamente",
                "condition": lambda metrics: metrics.metrics["correct_answers"] >= 1,
                "rarity": "common",
                "points": 10
            },
            "accuracy_master": {
                "name": "🎯 Maestro de Precisión",
                "description": "Has alcanzado 90% de precisión en las últimas 10 preguntas",
                "condition": lambda metrics: self._check_recent_accuracy(metrics, 10, 0.9),
                "rarity": "rare",
                "points": 50
            },
            "speed_demon": {
                "name": "⚡ Demonio de la Velocidad",
                "description": "Has respondido correctamente en menos de 10 segundos",
                "condition": lambda metrics: any(q["time_taken"] < 10 and q["correct"] for q in metrics.question_history[-5:]),
                "rarity": "epic",
                "points": 75
            },
            "streak_master": {
                "name": "🔥 Maestro de Rachas",
                "description": "Has mantenido una racha de 15 respuestas correctas",
                "condition": lambda metrics: metrics.metrics["streak_best"] >= 15,
                "rarity": "legendary",
                "points": 100
            },
            "perfectionist": {
                "name": "💎 Perfeccionista",
                "description": "Has completado 10 misiones sin usar pistas ni reintentos",
                "condition": lambda metrics: self._check_perfect_run(metrics, 10),
                "rarity": "mythic",
                "points": 150
            },
            "scholar": {
                "name": "🎓 Erudito",
                "description": "Has alcanzado maestría en todos los temas principales",
                "condition": lambda metrics: metrics.metrics["mastery_level"] >= 0.95,
                "rarity": "ultimate",
                "points": 200
            },
            "persistent": {
                "name": "💪 Persistente",
                "description": "Has reintentado misiones 5 veces y aprendido de tus errores",
                "condition": lambda metrics: metrics.metrics["retries_used"] >= 5,
                "rarity": "common",
                "points": 25
            },
            "efficient": {
                "name": "⏱️ Eficiente",
                "description": "Has completado todas las misiones en menos de 30 minutos",
                "condition": lambda metrics: metrics.metrics["time_spent"] < 1800,  # 30 minutos
                "rarity": "rare",
                "points": 60
            },
            "explorer": {
                "name": "🗺️ Explorador",
                "description": "Has usado pistas en al menos 5 misiones diferentes",
                "condition": lambda metrics: metrics.metrics["hints_used"] >= 5,
                "rarity": "uncommon",
                "points": 30
            },
            "consistent": {
                "name": "📊 Consistente",
                "description": "Has mantenido una consistencia del 80% en tus respuestas",
                "condition": lambda metrics: metrics.metrics["consistency_score"] >= 0.8,
                "rarity": "rare",
                "points": 70
            }
        }

    def check_achievements(self, metrics) -> List[Dict[str, Any]]:
        """
        Verifica qué logros se han desbloqueado.

        Args:
            metrics: Instancia de AcademicMetrics

        Returns:
            Lista de logros recién desbloqueados
        """
        new_achievements = []

        for achievement_id, definition in self.achievement_definitions.items():
            if achievement_id not in self.unlocked_achievements:
                if definition["condition"](metrics):
                    self.unlocked_achievements.add(achievement_id)
                    new_achievements.append(definition)

        return new_achievements

    def _check_recent_accuracy(self, metrics, window_size: int, threshold: float) -> bool:
        """
        Verifica precisión en ventana reciente.

        Args:
            metrics: Instancia de AcademicMetrics
            window_size: Tamaño de la ventana a verificar
            threshold: Umbral de precisión requerido

        Returns:
            True si se cumple la condición
        """
        if len(metrics.question_history) < window_size:
            return False

        recent = metrics.question_history[-window_size:]
        correct = sum(1 for q in recent if q["correct"])
        return (correct / window_size) >= threshold

    def _check_perfect_run(self, metrics, min_questions: int) -> bool:
        """
        Verifica si hay una racha perfecta sin ayuda.

        Args:
            metrics: Instancia de AcademicMetrics
            min_questions: Número mínimo de preguntas perfectas

        Returns:
            True si se cumple la condición
        """
        if len(metrics.question_history) < min_questions:
            return False

        recent = metrics.question_history[-min_questions:]
        return all(q["correct"] and not q["hints_used"] and not q["retried"] for q in recent)

    def get_achievement_progress(self, achievement_id: str, metrics) -> Dict[str, Any]:
        """
        Obtiene el progreso hacia un logro específico.

        Args:
            achievement_id: ID del logro
            metrics: Instancia de AcademicMetrics

        Returns:
            Diccionario con información de progreso
        """
        if achievement_id not in self.achievement_definitions:
            return {"unlocked": False, "progress": 0, "required": 1}

        definition = self.achievement_definitions[achievement_id]
        unlocked = achievement_id in self.unlocked_achievements

        # Calcular progreso específico para cada logro
        if achievement_id == "first_victory":
            progress = min(metrics.metrics["correct_answers"], 1)
            required = 1
        elif achievement_id == "accuracy_master":
            if len(metrics.question_history) >= 10:
                recent = metrics.question_history[-10:]
                correct = sum(1 for q in recent if q["correct"])
                progress = correct / 10
            else:
                progress = 0
            required = 0.9
        elif achievement_id == "streak_master":
            progress = min(metrics.metrics["streak_best"] / 15, 1)
            required = 1
        elif achievement_id == "perfectionist":
            if len(metrics.question_history) >= 10:
                recent = metrics.question_history[-10:]
                perfect_count = sum(1 for q in recent if q["correct"] and not q["hints_used"] and not q["retried"])
                progress = perfect_count / 10
            else:
                progress = 0
            required = 1
        elif achievement_id == "scholar":
            progress = min(metrics.metrics["mastery_level"] / 0.95, 1)
            required = 1
        else:
            progress = 1 if unlocked else 0
            required = 1

        return {
            "unlocked": unlocked,
            "progress": progress,
            "required": required,
            "name": definition["name"],
            "description": definition["description"],
            "rarity": definition["rarity"],
            "points": definition.get("points", 0)
        }

    def get_total_points(self) -> int:
        """
        Calcula el total de puntos obtenidos por logros.

        Returns:
            Total de puntos acumulados
        """
        total_points = 0
        for achievement_id in self.unlocked_achievements:
            if achievement_id in self.achievement_definitions:
                total_points += self.achievement_definitions[achievement_id].get("points", 0)
        return total_points

    def get_earned_achievements(self) -> List[str]:
        """
        Obtiene la lista de logros obtenidos.

        Returns:
            Lista de nombres de logros obtenidos
        """
        earned = []
        for achievement_id in self.unlocked_achievements:
            if achievement_id in self.achievement_definitions:
                earned.append(self.achievement_definitions[achievement_id]["name"])
        return earned

    def reset_achievements(self) -> None:
        """Reinicia todos los logros (para nueva sesión)."""
        self.achievements = []
        self.unlocked_achievements = set()