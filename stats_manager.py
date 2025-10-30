import json
import os
from datetime import datetime
import logging

class StatsManager:
    """Maneja estadísticas y persistencia de datos del juego"""
    
    def __init__(self, stats_file="game_stats.json"):
        self.stats_file = stats_file
        self.logger = self._setup_logger()
        self.stats = self._load_stats()
    
    def _setup_logger(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('quiz_game.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_stats(self):
        """Carga estadísticas desde archivo"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return self._create_default_stats()
        except Exception as e:
            self.logger.error(f"Error cargando estadísticas: {e}")
            return self._create_default_stats()
    
    def _create_default_stats(self):
        """Crea estructura de estadísticas por defecto"""
        return {
            "total_games": 0,
            "total_questions_answered": 0,
            "total_correct": 0,
            "best_score": 0,
            "sessions": [],
            "category_stats": {}
        }
    
    def save_session(self, score, errors, total_questions, category_filter=None):
        """Guarda una sesión de juego"""
        try:
            session = {
                "date": datetime.now().isoformat(),
                "score": score,
                "errors": errors,
                "total": total_questions,
                "percentage": (score / total_questions * 100) if total_questions > 0 else 0,
                "category": category_filter
            }
            
            self.stats["sessions"].append(session)
            self.stats["total_games"] += 1
            self.stats["total_questions_answered"] += total_questions
            self.stats["total_correct"] += score
            
            if score > self.stats["best_score"]:
                self.stats["best_score"] = score
            
            self._save_stats()
            self.logger.info(f"Sesión guardada: {score}/{total_questions}")
            
        except Exception as e:
            self.logger.error(f"Error guardando sesión: {e}")
    
    def _save_stats(self):
        """Guarda estadísticas a archivo"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error guardando estadísticas: {e}")
    
    def get_stats_summary(self):
        """Retorna resumen de estadísticas"""
        if self.stats["total_games"] == 0:
            return "No hay estadísticas disponibles"
        
        avg_score = self.stats["total_correct"] / self.stats["total_games"]
        avg_percentage = (self.stats["total_correct"] / self.stats["total_questions_answered"] * 100) if self.stats["total_questions_answered"] > 0 else 0
        
        return {
            "total_games": self.stats["total_games"],
            "best_score": self.stats["best_score"],
            "average_score": round(avg_score, 1),
            "average_percentage": round(avg_percentage, 1),
            "total_questions": self.stats["total_questions_answered"]
        }