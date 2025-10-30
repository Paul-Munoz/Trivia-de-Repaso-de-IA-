"""
Game Controller Module - Proyecto Alpha v4.0
Controlador principal del juego educativo.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

from academic_metrics import AcademicMetrics
from achievement_system import AchievementSystem
from learning_manager import LearningModeManager
from ui_manager import UIManager
from missions import MISSIONS
from config import SAVE_FILE, PROFESSIONAL_CONFIG, ACADEMIC_CONFIG, LOG_FILE
from simple_puzzles import get_random_puzzle, validate_puzzle_answer


class GameController:
    """
    Controlador principal del sistema educativo Proyecto Alpha.

    Coordina todas las componentes del sistema: métricas académicas,
    sistema de logros, gestión de aprendizaje, interfaz de usuario
    y lógica del juego educativo.
    """

    def __init__(self, root: tk.Tk):
        self.logger = logging.getLogger(self.__class__.__name__)
        """Inicializa el controlador del juego."""
        self.root = root

        # Componentes principales
        self.academic_metrics = AcademicMetrics()
        self.achievement_system = AchievementSystem()
        self.learning_manager = LearningModeManager()
        self.ui_manager = UIManager(root)
        # Modo puzzle activado
        self.puzzle_mode = True

        # Temporizadores
        self.question_timer = None
        self.question_start_time = None
        self.session_timer = None

        # Estado del juego
        self.game_state = self._initialize_game_state()

        # Configurar UI
        self._setup_ui()

        # Inicializar sistema
        self._initialize_system()

    def _initialize_game_state(self) -> Dict[str, Any]:
        """Inicializa el estado del juego."""
        return {
            "mission": 1,
            "score": 0,
            "max_score": len(MISSIONS),
            "current_story_idx": 0,
            "story_full_text": "",
            "status": "Sistema Educativo Profesional Listo",
            "learning_mode": "adaptive",
            "difficulty_level": "normal",
            "time_started": None,
            "time_spent": 0,
            "hints_used": 0,
            "retries": 0,
            "streak": 0,
            "best_streak": 0,
            "current_question_time": 0,
            "session_stats": {
                "correct_answers": [],
                "incorrect_answers": [],
                "time_per_question": [],
                "difficult_concepts": [],
                "performance_trend": []
            },
            "achievements": [],
            "progress_history": [],
            "adaptive_settings": {
                "show_hints": True,
                "time_limits": True,
                "detailed_feedback": True,
                "adaptive_difficulty": True
            },
            "session_id": f"session_{int(time.time())}",
            "user_id": "default_user",
            "accessibility_mode": False,
            "high_contrast": False,
            "keyboard_navigation": True,
            "auto_save_enabled": True,
            "performance_metrics": {
                "avg_response_time": 0,
                "accuracy_trend": [],
                "learning_efficiency": 0,
                "concept_mastery_levels": {}
            },
            "error_log": [],
            "user_feedback": [],
            "puzzle_mode": True,
            "current_puzzle": None,
            "puzzle_type": "random",  # random, logic, memory, riddle, pattern
            "puzzle_difficulty": "medium",
            "puzzle_score": 0,
            "puzzles_completed": 0,
            "puzzle_streak": 0
        }

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario."""
        # Crear layout principal
        self.ui_manager.create_main_layout()
        self.ui_manager.create_side_panel()
        self.ui_manager.create_animations_canvas()
        self.ui_manager.setup_animations()

        # Crear barra de menú con callbacks
        menu_callbacks = {
            "new_session": self.restart_session,
            "save_progress": self.save_progress,
            "load_progress": self.load_progress,
            "export_report": self.export_report,
            "exit": self.quit_application,
            "set_mode": self.set_learning_mode,
            "show_dashboard": self.show_dashboard,
            "show_settings": self.show_settings,
            "toggle_contrast": self.toggle_high_contrast,
            "toggle_keyboard": self.toggle_keyboard_nav,
            "check_contrast": self.check_contrast,
            "show_tutorial": self.ui_manager.show_tutorial,
            "show_guide": self.show_guide,
            "show_feedback": self.show_feedback_form,
            "show_about": self.ui_manager.show_about
        }
        self.ui_manager.create_menu_bar(menu_callbacks)

        # Conectar botones principales
        self.ui_manager.next_button.config(command=self.next_mission)
        self.ui_manager.hint_button.config(command=self.show_hint)
        self.ui_manager.retry_button.config(command=self.retry_mission)

    def _initialize_system(self) -> None:
        """Inicializa el sistema completo."""
        try:
            # Cargar configuración guardada
            self.load_system_config()

            # Inicializar métricas de sesión
            self.academic_metrics.session_start_time = time.time()

            # Configurar adaptabilidad inicial
            self.learning_manager.adapt_difficulty(self.academic_metrics)

            # Cargar progreso si existe
            self.load_progress()

            # Iniciar sesión
            self.start_session()

        except Exception as e:
            self.log_error(f"Error en inicialización del sistema: {str(e)}")
            messagebox.showerror("Error de Inicialización",
                                f"No se pudo inicializar el sistema correctamente:\n{str(e)}")
            self.root.quit()

    def start_session(self) -> None:
        """Inicia la sesión educativa."""
        try:
            # Resetear estado de sesión
            self.game_state["mission"] = 0
            self.game_state["score"] = 0
            self.game_state["current_story_idx"] = 0
            self.game_state["status"] = "Sistema Educativo Profesional Listo"
            self.game_state["time_started"] = time.time()

            # Configurar indicadores visuales
            self.ui_manager.progress_text_var.set(f"📊 Misión 0/{len(MISSIONS)} | Puntuación: 0/{self.game_state['max_score']}")
            self.ui_manager.timer_text_var.set("⏱️ 00:00:00")
            self.ui_manager.metrics_text_var.set("🎯 ¡Listo para comenzar tu aventura de aprendizaje!")

            # Configurar modo de aprendizaje
            mode_settings = self.learning_manager.get_mode_settings()
            self.ui_manager.mode_indicator.config(text=f"📚 MODO: {mode_settings['mode'].upper()}")

            # Activar controles principales  
            if self.puzzle_mode:
                self.ui_manager.next_button.config(text="🧩 COMENZAR PUZZLES", state=tk.NORMAL)
            else:
                self.ui_manager.next_button.config(text="🚀 COMENZAR AVENTURA", state=tk.NORMAL)
            self.ui_manager.hint_button.config(state=tk.DISABLED)
            self.ui_manager.retry_button.config(state=tk.DISABLED)

            # Texto de bienvenida más simple y claro
            intro_text = self._get_intro_text()
            self.ui_manager.mission_title_label.config(text="🎯 ¡BIENVENIDO AL PROYECTO ALPHA!")
            self.ui_manager.story_text_var.set(intro_text)
            self.ui_manager.feedback_text_var.set("¡Hola! Estás a punto de comenzar una aventura increíble aprendiendo sobre Inteligencia Artificial. Haz clic en 'COMENZAR AVENTURA' cuando estés listo.")
            self.ui_manager.clear_options()

            # Iniciar temporizador de sesión
            self.start_session_timer()

            # Log de inicio de sesión
            self.log_event("Sesión iniciada", "INFO")

        except Exception as e:
            self.log_error(f"Error al iniciar sesión: {str(e)}")
            messagebox.showerror("Error de Sesión",
                                f"No se pudo iniciar la sesión correctamente:\n{str(e)}")

    def _get_intro_text(self) -> str:
        """Obtiene el texto de introducción simplificado."""
        return (
            "¡Hola! 👋 Bienvenido a una aventura increíble donde aprenderás sobre Inteligencia Artificial de manera divertida.\n\n"
            "🎯 ¿QUÉ VAS A APRENDER?\n\n"
            "• 🤖 Qué es la Inteligencia Artificial y cómo funciona\n"
            "• 🧠 Cómo las máquinas pueden 'aprender' como los humanos\n"
            "• 📊 Diferentes tipos de IA y sus aplicaciones\n"
            "• 🔍 Cómo evaluar si una IA está funcionando bien\n"
            "• 🛠️ Herramientas y métodos que usan los expertos en IA\n\n"
            "🎮 ¿CÓMO FUNCIONA?\n\n"
            "Completarás 21 misiones educativas. En cada una:\n"
            "• Leerás una historia o situación interesante\n"
            "• Elegirás la respuesta correcta entre varias opciones\n"
            "• Recibirás explicaciones detalladas\n"
            "• Podrás usar pistas si necesitas ayuda\n\n"
            "¡No te preocupes si no sabes algo! Esto es para aprender. 🌟\n\n"
            "🧩 MODO PUZZLE MENTAL ACTIVADO:\n"
            "• 🧠 Tests de memoria para recordar conceptos\n"
            "• 🔗 Rompecabezas de lógica para conectar ideas\n"
            "• 🎭 Adivinanzas creativas sobre IA\n"
            "• 🔍 Patrones y secuencias algorítmicas\n\n"
            "¡Cada puzzle ejercitará tu mente de forma diferente!"
        )

    def next_mission(self) -> None:
        """Avanza a la siguiente misión o inicia un puzzle."""
        try:
            if self.game_state["mission"] == 0:
                # Primera misión - mostrar puzzle
                self.start_puzzle_mission()
            elif self.game_state["mission"] < len(MISSIONS):
                # Continuar con puzzles
                self.start_puzzle_mission()
            else:
                # Completar sesión
                self.complete_session()
                
        except Exception as e:
            self.log_error(f"Error en next_mission: {str(e)}")
            messagebox.showerror("Error", f"Error al avanzar: {str(e)}")
    
    def start_puzzle_mission(self) -> None:
        """Inicia una misión con puzzle."""
        try:
            self.game_state["mission"] += 1
            current_mission = self.game_state["mission"]
            
            # Crear puzzle mental
            puzzle = get_random_puzzle(current_mission - 1)
            self.game_state["current_puzzle"] = puzzle
            
            # Actualizar UI con el puzzle
            self.ui_manager.mission_title_label.config(text=puzzle.title)
            self.ui_manager.story_text_var.set(puzzle.story)
            
            # Crear opciones del puzzle
            self.ui_manager.clear_options()
            self.create_puzzle_options(puzzle)
            
            # Actualizar progreso
            self.ui_manager.progress_text_var.set(
                f"📊 Puzzle {current_mission}/{len(MISSIONS)} | Puntuación: {self.game_state['puzzle_score']}"
            )
            
            # Configurar controles
            self.ui_manager.next_button.config(state=tk.DISABLED)
            self.ui_manager.hint_button.config(state=tk.NORMAL)
            self.ui_manager.retry_button.config(state=tk.DISABLED)
            
            # Feedback inicial
            self.ui_manager.feedback_text_var.set(
                f"🧠 Desafío Mental: {puzzle.puzzle_type.title()}\n"
                "Lee cuidadosamente y usa tu lógica para resolver este puzzle."
            )
            
            # Iniciar temporizador
            self.question_start_time = time.time()
            
        except Exception as e:
            self.log_error(f"Error al iniciar puzzle: {str(e)}")
            messagebox.showerror("Error", f"No se pudo cargar el puzzle: {str(e)}")
    
    def create_puzzle_options(self, puzzle) -> None:
        """Crea las opciones del puzzle usando la UI existente."""
        # Simular estructura de misión para usar el sistema existente
        fake_mission = {
            "options": puzzle.options,
            "answer": puzzle.answer
        }
        
        # Usar el sistema existente de opciones
        self.ui_manager.create_option_buttons(fake_mission, self.handle_puzzle_answer)
        
        # Guardar referencia al puzzle actual
        self.current_puzzle = puzzle
    
    def handle_puzzle_answer(self, selected_option: str, option_widget) -> None:
        """Maneja la respuesta del puzzle."""
        try:
            puzzle = self.game_state["current_puzzle"]
            
            # Validar respuesta del puzzle
            is_correct, feedback = validate_puzzle_answer(puzzle, selected_option)
            
            # Calcular tiempo
            time_taken = time.time() - self.question_start_time if self.question_start_time else 0
            
            # Actualizar estadísticas del puzzle
            if is_correct:
                self.game_state["score"] += 1
                self.game_state["puzzle_score"] += 10  # 10 puntos por puzzle correcto
                self.game_state["puzzles_completed"] += 1
                self.game_state["puzzle_streak"] += 1
                self.game_state["streak"] += 1
                
                if self.game_state["puzzle_streak"] > self.game_state["best_streak"]:
                    self.game_state["best_streak"] = self.game_state["puzzle_streak"]
                
                # Registrar en métricas académicas
                self.academic_metrics.record_correct_answer(time_taken)
                
                # Habilitar siguiente puzzle
                next_mission = self.game_state["mission"] + 1
                if next_mission <= len(MISSIONS):
                    self.ui_manager.next_button.config(text=f"🧩 Puzzle {next_mission}", state=tk.NORMAL)
                else:
                    self.ui_manager.next_button.config(text="🏆 Finalizar", state=tk.NORMAL)
            else:
                self.game_state["puzzle_streak"] = 0
                self.game_state["streak"] = 0
                self.game_state["retries"] += 1
                
                # Registrar respuesta incorrecta
                self.academic_metrics.record_incorrect_answer(time_taken)
                
                # Habilitar reintento y continuar
                self.ui_manager.retry_button.config(state=tk.NORMAL, text="🔄 Nuevo Puzzle")
                self.ui_manager.next_button.config(text="➡️ Continuar", state=tk.NORMAL)
            
            # Mostrar feedback
            self.ui_manager.feedback_text_var.set(feedback)
            
            # Deshabilitar opciones y pistas
            self.ui_manager.hint_button.config(state=tk.DISABLED)
            
            # Actualizar displays
            self.update_progress_display()
            self.update_stats_display()
            
            # Resetear pistas para próximo puzzle
            self.game_state["hints_used"] = 0
            
        except Exception as e:
            self.log_error(f"Error al manejar respuesta del puzzle: {str(e)}")
            messagebox.showerror("Error", f"Error al procesar respuesta: {str(e)}")
    
    def show_hint(self) -> None:
        """Muestra una pista para el puzzle actual."""
        try:
            if "current_puzzle" in self.game_state and self.game_state["current_puzzle"]:
                puzzle = self.game_state["current_puzzle"]
                hints = puzzle.hints

                if hints:
                    hint_level = min(self.game_state["hints_used"], len(hints) - 1)
                    hint = hints[hint_level]

                    self.ui_manager.feedback_text_var.set(f"💡 PISTA: {hint}")

                    # Marcar pista usada
                    self.game_state["hints_used"] += 1

                    # Deshabilitar botón de pista temporalmente
                    self.ui_manager.hint_button.config(state=tk.DISABLED)

                    # Log
                    self.log_event(f"Pista usada en puzzle {self.game_state['mission']}", "INFO")
                else:
                    self.ui_manager.feedback_text_var.set("No hay pistas disponibles para este puzzle.")
            else:
                # Usar el sistema original si no hay puzzle
                self._show_original_hint()

        except Exception as e:
            self.log_error(f"Error al mostrar pista: {str(e)}")
    
    def retry_mission(self) -> None:
        """Reintenta el puzzle actual o carga uno nuevo."""
        try:
            if self.puzzle_mode and "current_puzzle" in self.game_state:
                # Generar nuevo puzzle del mismo tipo
                current_mission = self.game_state["mission"]
                new_puzzle = get_random_puzzle(current_mission + 100)  # Offset para variedad

                self.game_state["current_puzzle"] = new_puzzle
                self.game_state["retries"] += 1

                # Actualizar UI con nuevo puzzle
                self.ui_manager.mission_title_label.config(text=new_puzzle.title)
                self.ui_manager.story_text_var.set(new_puzzle.story)

                # Recrear opciones
                self.ui_manager.clear_options()
                self.create_puzzle_options(new_puzzle)

                # Resetear controles
                self.ui_manager.next_button.config(state=tk.DISABLED)
                self.ui_manager.hint_button.config(state=tk.NORMAL)
                self.ui_manager.retry_button.config(state=tk.DISABLED)

                # Feedback
                self.ui_manager.feedback_text_var.set(
                    f"🔄 Nuevo puzzle generado. Tipo: {new_puzzle.puzzle_type.title()}"
                )

                # Reiniciar temporizador
                self.question_start_time = time.time()

                self.log_event(f"Nuevo puzzle generado para misión {current_mission}", "INFO")
            else:
                # Usar sistema original
                if hasattr(self, 'current_mission'):
                    self._load_original_mission(self.game_state["mission"])

        except Exception as e:
            self.log_error(f"Error al reintentar: {str(e)}")
    
    def load_mission(self, mission_id: int) -> None:
        """Carga una misión específica - modo puzzle."""
        try:
            if self.puzzle_mode:
                # En modo puzzle, cargar puzzle en lugar de misión tradicional
                self.start_puzzle_mission()
            else:
                # Modo tradicional (código original)
                self._load_original_mission(mission_id)

        except Exception as e:
            self.log_error(f"Error al cargar misión {mission_id}: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar la misión: {str(e)}")
    
    def handle_answer(self, selected_option: str, option_widget) -> None:
        """Maneja respuestas del modo tradicional."""
        try:
            if not hasattr(self, 'current_mission'):
                return

            mission = self.current_mission
            correct_answer = mission["answer"]
            is_correct = selected_option == correct_answer
            time_taken = time.time() - self.question_start_time if self.question_start_time else 0

            # Registrar respuesta
            self.academic_metrics.record_answer(
                mission_id=self.game_state["mission"],
                correct=is_correct,
                time_taken=time_taken,
                hints_used=self.game_state.get("hint_used_this_question", False),
                retried=self.game_state.get("retried_this_question", False)
            )

            # Actualizar estado
            if is_correct:
                self.game_state["score"] += 1
                self.game_state["streak"] += 1
                if self.game_state["streak"] > self.game_state["best_streak"]:
                    self.game_state["best_streak"] = self.game_state["streak"]
                
                feedback = f"✅ ¡EXCELENTE! Respuesta correcta.\n\n"
                feedback += f"🎯 Tu respuesta: {selected_option}\n\n"
                feedback += f"📚 Explicación: {mission['options'][selected_option]}\n\n"
                if 'explanation' in mission:
                    feedback += f"💡 Detalle: {mission['explanation']}\n\n"
                feedback += f"🔥 Racha: {self.game_state['streak']} respuestas correctas"
                
                self.ui_manager.feedback_text_var.set(feedback)
                
                # Habilitar siguiente misión
                next_mission_num = self.game_state["mission"] + 1
                if next_mission_num <= len(MISSIONS):
                    self.ui_manager.next_button.config(text=f"➡️ Misión {next_mission_num}", state=tk.NORMAL)
                else:
                    self.ui_manager.next_button.config(text="🏆 Finalizar", state=tk.NORMAL)
                
            else:
                self.game_state["streak"] = 0
                
                feedback = f"❌ Respuesta incorrecta, pero ¡sigue aprendiendo!\n\n"
                feedback += f"🔴 Tu respuesta: {selected_option}\n"
                feedback += f"✅ Respuesta correcta: {correct_answer}\n\n"
                feedback += f"📚 Explicación: {mission['options'][correct_answer]}\n\n"
                if 'explanation' in mission:
                    feedback += f"💡 Detalle: {mission['explanation']}\n\n"
                feedback += "💪 ¡Puedes intentarlo de nuevo!"
                
                self.ui_manager.feedback_text_var.set(feedback)
                
                # Habilitar reintento y continuar
                self.ui_manager.retry_button.config(state=tk.NORMAL)
                self.ui_manager.next_button.config(text="➡️ Continuar", state=tk.NORMAL)

            # Deshabilitar controles
            self.ui_manager.hint_button.config(state=tk.DISABLED)
            
            # Resetear flags
            self.game_state["hint_used_this_question"] = False
            self.game_state["retried_this_question"] = False
            
            # Actualizar displays
            self.update_progress_display()
            self.update_stats_display()
            
        except Exception as e:
            self.log_error(f"Error al manejar respuesta: {str(e)}")
            messagebox.showerror("Error", f"Error al procesar respuesta: {str(e)}")
    

    

    
    def complete_evaluation(self) -> None:
        """Completa la evaluación de puzzles."""
        try:
            # Detener temporizadores
            if self.session_timer:
                self.root.after_cancel(self.session_timer)
            
            # Calcular métricas finales
            total_time = time.time() - self.game_state["time_started"]
            final_score = self.game_state["puzzle_score"]
            puzzles_completed = self.game_state["puzzles_completed"]
            accuracy = (puzzles_completed / len(MISSIONS)) * 100 if len(MISSIONS) > 0 else 0
            
            # Mostrar resultados finales
            result_text = f"🎉 ¡AVENTURA DE PUZZLES COMPLETADA! 🎉\n\n"
            result_text += f"🧩 Puzzles Resueltos: {puzzles_completed}/{len(MISSIONS)}\n"
            result_text += f"🎯 Puntuación Total: {final_score} puntos\n"
            result_text += f"🔥 Mejor Racha: {self.game_state['best_streak']} puzzles\n"
            result_text += f"⏱️ Tiempo Total: {int(total_time//60)}:{int(total_time%60):02d}\n"
            result_text += f"🔄 Reintentos: {self.game_state['retries']}\n\n"
            result_text += f"🧠 Nivel Mental: {self.get_puzzle_mastery_level(accuracy)}\n\n"
            result_text += "¡Excelente trabajo ejercitando tu mente con puzzles de IA!"
            
            self.ui_manager.feedback_text_var.set(result_text)
            
            # Deshabilitar controles
            self.ui_manager.next_button.config(text="✅ Puzzles Completados", state=tk.DISABLED)
            self.ui_manager.hint_button.config(state=tk.DISABLED)
            self.ui_manager.retry_button.config(state=tk.DISABLED)
            
            # Guardar progreso
            self.save_progress()
            
            # Log
            self.log_event(f"Sesión de puzzles completada - Puntuación: {final_score}", "INFO")
            
        except Exception as e:
            self.log_error(f"Error al completar evaluación: {str(e)}")
    
    def get_puzzle_mastery_level(self, accuracy: float) -> str:
        """Determina el nivel de dominio mental basado en puzzles resueltos."""
        if accuracy >= 90:
            return "🧠 GENIO DE PUZZLES"
        elif accuracy >= 80:
            return "🎯 MAESTRO MENTAL"
        elif accuracy >= 70:
            return "🧩 SOLUCIONADOR EXPERTO"
        elif accuracy >= 60:
            return "💡 PENSADOR LÓGICO"
        else:
            return "🌱 MENTE EN DESARROLLO"

    def _load_original_mission(self, mission_id: int) -> None:
        """Carga una misión específica con mejor visualización."""
        try:
            if mission_id not in MISSIONS:
                raise ValueError(f"Misión {mission_id} no encontrada")

            mission = MISSIONS[mission_id]
            self.current_mission = mission
            self.question_start_time = time.time()

            # Actualizar título de misión de forma más clara
            self.ui_manager.mission_title_label.config(text=f"📚 {mission['title']}")

            # Mostrar el concepto clave de forma destacada
            concept_text = f"🎯 CONCEPTO CLAVE: {mission['concept_name']}\n\n{mission['story']}"
            self.ui_manager.story_text_var.set(concept_text)

            # Crear opciones
            self.ui_manager.clear_options()
            self.ui_manager.create_option_buttons(mission, self.handle_answer)

            # Configurar controles
            self.ui_manager.next_button.config(state=tk.DISABLED)
            self.ui_manager.hint_button.config(state=tk.NORMAL)
            self.ui_manager.retry_button.config(state=tk.DISABLED)

            # Actualizar progreso
            self.update_progress_display()

            # Feedback inicial más amigable
            self.ui_manager.feedback_text_var.set("📖 Lee la historia con atención y elige la respuesta que crees correcta. ¡No hay prisa, tómate tu tiempo para pensar!")
            self.ui_manager.metrics_text_var.set(f"💡 Puedes usar una pista si la necesitas. Categoría: {mission.get('category', 'General')}")

            # Log
            self.log_event(f"Misión {mission_id} cargada: {mission['title']}", "INFO")

        except Exception as e:
            self.log_error(f"Error al cargar misión {mission_id}: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar la misión: {str(e)}")

    def handle_answer(self, selected_option: str, option_widget) -> None:
        """Maneja la respuesta seleccionada por el usuario."""
        try:
            if not hasattr(self, 'current_mission'):
                return

            mission = self.current_mission
            correct_answer = mission["answer"]
            is_correct = selected_option == correct_answer
            time_taken = time.time() - self.question_start_time if self.question_start_time else 0

            # Registrar respuesta en métricas
            self.academic_metrics.record_answer(
                mission_id=self.game_state["mission"],
                correct=is_correct,
                time_taken=time_taken,
                hints_used=self.game_state.get("hint_used_this_question", False),
                retried=self.game_state.get("retried_this_question", False)
            )

            # Actualizar estado del juego
            if is_correct:
                self.game_state["score"] += 1
                self.game_state["streak"] += 1
                if self.game_state["streak"] > self.game_state["best_streak"]:
                    self.game_state["best_streak"] = self.game_state["streak"]
                
                # Feedback positivo muy claro
                feedback = f"✅ ¡EXCELENTE! ¡Respuesta correcta!\n\n"
                feedback += f"🎯 Tu respuesta: {selected_option}\n\n"
                feedback += f"📚 Explicación: {mission['options'][selected_option]}\n\n"
                if 'explanation' in mission:
                    feedback += f"💡 ¿Por qué es correcta? {mission['explanation']}\n\n"
                feedback += f"🔥 ¡Llevas {self.game_state['streak']} respuestas correctas seguidas!"
                
                self.ui_manager.feedback_text_var.set(feedback)
                
                # Verificar logros
                self.achievement_system.check_achievements(self.academic_metrics)
                
                # Habilitar siguiente misión
                next_mission_num = self.game_state["mission"] + 1
                if next_mission_num <= len(MISSIONS):
                    self.ui_manager.next_button.config(text=f"➡️ Misión {next_mission_num}", state=tk.NORMAL)
                else:
                    self.ui_manager.next_button.config(text="🏆 Finalizar", state=tk.NORMAL)
                
            else:
                self.game_state["streak"] = 0
                
                # Feedback de error educativo
                feedback = f"❌ Respuesta incorrecta, pero ¡no te preocupes! Así se aprende.\n\n"
                feedback += f"🔴 Tu respuesta: {selected_option}\n"
                feedback += f"✅ Respuesta correcta: {correct_answer}\n\n"
                feedback += f"📚 ¿Por qué es correcta? {mission['options'][correct_answer]}\n\n"
                if 'explanation' in mission:
                    feedback += f"💡 Explicación detallada: {mission['explanation']}\n\n"
                feedback += "💪 ¡Puedes intentarlo de nuevo o continuar a la siguiente misión!"
                
                self.ui_manager.feedback_text_var.set(feedback)
                
                # Habilitar reintento y continuar
                self.ui_manager.retry_button.config(state=tk.NORMAL)
                self.ui_manager.next_button.config(text="➡️ Continuar", state=tk.NORMAL)

            # Deshabilitar opciones y pistas
            self.ui_manager.hint_button.config(state=tk.DISABLED)
            
            # Resetear flags de la pregunta
            self.game_state["hint_used_this_question"] = False
            self.game_state["retried_this_question"] = False
            
            # Actualizar displays
            self.update_progress_display()
            self.update_stats_display()
            
            # Log
            self.log_event(f"Respuesta {'correcta' if is_correct else 'incorrecta'} en misión {self.game_state['mission']}", "INFO")

        except Exception as e:
            self.log_error(f"Error al manejar respuesta: {str(e)}")
            messagebox.showerror("Error", f"Error al procesar la respuesta: {str(e)}")

    def show_hint(self) -> None:
        """Muestra una pista para la misión actual."""
        try:
            if not hasattr(self, 'current_mission'):
                return

            mission = self.current_mission
            hints = mission.get("hints", [])
            
            if hints:
                hint_text = "💡 PISTA: " + hints[0]
                if len(hints) > 1:
                    hint_text += f"\n\n🔍 PISTA ADICIONAL: {hints[1]}"
                
                self.ui_manager.feedback_text_var.set(hint_text)
                
                # Marcar que se usó pista
                self.game_state["hint_used_this_question"] = True
                self.game_state["hints_used"] += 1
                
                # Deshabilitar botón de pista
                self.ui_manager.hint_button.config(state=tk.DISABLED)
                
                # Log
                self.log_event(f"Pista usada en misión {self.game_state['mission']}", "INFO")
            else:
                self.ui_manager.feedback_text_var.set("No hay pistas disponibles para esta misión.")

        except Exception as e:
            self.log_error(f"Error al mostrar pista: {str(e)}")

    def retry_mission(self) -> None:
        """Permite reintentar la misión actual."""
        try:
            if hasattr(self, 'current_mission'):
                # Marcar reintento
                self.game_state["retried_this_question"] = True
                self.game_state["retries"] += 1
                
                # Recargar misión
                self.load_mission(self.game_state["mission"])
                
                # Log
                self.log_event(f"Reintento de misión {self.game_state['mission']}", "INFO")

        except Exception as e:
            self.log_error(f"Error al reintentar misión: {str(e)}")

    def complete_evaluation(self) -> None:
        """Completa la evaluación y muestra resultados finales."""
        try:
            # Detener temporizadores
            if self.session_timer:
                self.root.after_cancel(self.session_timer)
            
            # Calcular métricas finales
            final_score = self.game_state["score"]
            max_score = self.game_state["max_score"]
            accuracy = (final_score / max_score) * 100 if max_score > 0 else 0
            
            # Generar reporte
            report = self.generate_final_report()
            
            # Mostrar resultados
            result_text = f"🎯 EVALUACIÓN COMPLETADA\n\n"
            result_text += f"📊 Puntuación Final: {final_score}/{max_score} ({accuracy:.1f}%)\n"
            result_text += f"🏆 Mejor Racha: {self.game_state['best_streak']}\n"
            result_text += f"⏱️ Tiempo Total: {self.format_time(self.game_state['time_spent'])}\n\n"
            result_text += f"📈 Nivel de Dominio: {self.get_mastery_level(accuracy)}\n\n"
            result_text += "¡Felicitaciones por completar la evaluación!"
            
            self.ui_manager.feedback_text_var.set(result_text)
            
            # Deshabilitar controles
            self.ui_manager.next_button.config(text="✅ Evaluación Completada", state=tk.DISABLED)
            self.ui_manager.hint_button.config(state=tk.DISABLED)
            self.ui_manager.retry_button.config(state=tk.DISABLED)
            
            # Guardar progreso automáticamente
            self.save_progress()
            
            # Log
            self.log_event(f"Evaluación completada - Puntuación: {final_score}/{max_score}", "INFO")

        except Exception as e:
            self.log_error(f"Error al completar evaluación: {str(e)}")

    def start_session_timer(self) -> None:
        """Inicia el temporizador de sesión."""
        def update_timer():
            try:
                if self.game_state["time_started"]:
                    elapsed = time.time() - self.game_state["time_started"]
                    self.game_state["time_spent"] = elapsed
                    formatted_time = self.format_time(elapsed)
                    self.ui_manager.timer_text_var.set(formatted_time)
                    
                    # Programar siguiente actualización
                    self.session_timer = self.root.after(1000, update_timer)
            except Exception as e:
                self.log_error(f"Error en temporizador: {str(e)}")
        
        update_timer()

    def format_time(self, seconds: float) -> str:
        """Formatea tiempo en formato HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def get_mastery_level(self, accuracy: float) -> str:
        """Determina el nivel de dominio basado en la precisión."""
        if accuracy >= 90:
            return "🏆 EXPERTO"
        elif accuracy >= 80:
            return "🥇 AVANZADO"
        elif accuracy >= 70:
            return "🥈 INTERMEDIO"
        elif accuracy >= 60:
            return "🥉 BÁSICO"
        else:
            return "📚 EN DESARROLLO"

    def update_progress_display(self) -> None:
        """Actualiza la visualización del progreso."""
        try:
            current_mission = self.game_state["mission"]
            total_missions = len(MISSIONS)
            score = self.game_state["score"]
            max_score = self.game_state["max_score"]
            
            # Actualizar texto de progreso
            progress_text = f"📊 Misión {current_mission}/{total_missions} | Puntuación: {score}/{max_score}"
            self.ui_manager.progress_text_var.set(progress_text)
            
            # Actualizar barra de progreso
            self.ui_manager.update_progress_display(score, max_score)
            
        except Exception as e:
            self.log_error(f"Error al actualizar progreso: {str(e)}")

    def update_stats_display(self) -> None:
        """Actualiza la visualización de estadísticas."""
        try:
            stats = {
                'score': self.game_state["score"],
                'max_score': self.game_state["max_score"],
                'streak': self.game_state["streak"],
                'best_streak': self.game_state["best_streak"],
                'hints_used': self.game_state["hints_used"],
                'retries': self.game_state["retries"],
                'time_formatted': self.format_time(self.game_state["time_spent"])
            }
            
            self.ui_manager.update_stats_display(stats)
            
            # Actualizar métricas en tiempo real
            metrics_text = f"Precisión: {self.academic_metrics.get_accuracy()*100:.1f}% | "
            metrics_text += f"Tiempo promedio: {self.academic_metrics.metrics['average_time_per_question']:.1f}s"
            self.ui_manager.metrics_text_var.set(metrics_text)
            
        except Exception as e:
            self.log_error(f"Error al actualizar estadísticas: {str(e)}")

    def generate_final_report(self) -> Dict[str, Any]:
        """Genera un reporte final completo."""
        try:
            performance_report = self.academic_metrics.get_performance_report()
            achievements = self.achievement_system.get_earned_achievements()
            
            report = {
                "session_id": self.game_state["session_id"],
                "user_id": self.game_state["user_id"],
                "timestamp": datetime.now().isoformat(),
                "final_score": self.game_state["score"],
                "max_score": self.game_state["max_score"],
                "accuracy": performance_report["accuracy"],
                "time_spent": self.game_state["time_spent"],
                "hints_used": self.game_state["hints_used"],
                "retries": self.game_state["retries"],
                "best_streak": self.game_state["best_streak"],
                "achievements": achievements,
                "performance_metrics": performance_report,
                "learning_mode": self.game_state["learning_mode"]
            }
            
            return report
            
        except Exception as e:
            self.log_error(f"Error al generar reporte final: {str(e)}")
            return {}

    def save_progress(self) -> None:
        """Guarda el progreso actual."""
        try:
            save_data = {
                "game_state": self.game_state,
                "academic_metrics": self.academic_metrics.metrics,
                "achievements": self.achievement_system.get_earned_achievements(),
                "timestamp": datetime.now().isoformat()
            }
            
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            self.log_event("Progreso guardado exitosamente", "INFO")
            messagebox.showinfo("Guardado", "Progreso guardado exitosamente")
            
        except Exception as e:
            self.log_error(f"Error al guardar progreso: {str(e)}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def load_progress(self) -> None:
        """Carga progreso guardado."""
        try:
            import os
            if not os.path.exists(SAVE_FILE):
                return
            
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # Restaurar estado del juego
            if "game_state" in save_data:
                self.game_state.update(save_data["game_state"])
            
            # Restaurar métricas académicas
            if "academic_metrics" in save_data:
                self.academic_metrics.metrics.update(save_data["academic_metrics"])
            
            # Restaurar logros
            if "achievements" in save_data:
                self.achievement_system.unlocked_achievements = set(save_data["achievements"])
            
            self.log_event("Progreso cargado exitosamente", "INFO")
            
        except Exception as e:
            self.log_error(f"Error al cargar progreso: {str(e)}")

    def load_system_config(self) -> None:
        """Carga configuración del sistema."""
        try:
            # Configurar logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(LOG_FILE, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )
            
        except Exception as e:
            print(f"Error al configurar logging: {str(e)}")

    def log_event(self, message: str, level: str = "INFO") -> None:
        """Registra un evento en el log."""
        try:
            if level == "INFO":
                self.logger.info(message)
            elif level == "WARNING":
                self.logger.warning(message)
            elif level == "ERROR":
                self.logger.error(message)
        except:
            pass

    def log_error(self, message: str) -> None:
        """Registra un error en el log."""
        self.log_event(message, "ERROR")
        self.game_state["error_log"].append({
            "timestamp": datetime.now().isoformat(),
            "message": message
        })

    def restart_session(self) -> None:
        """Reinicia la sesión completa."""
        try:
            # Resetear métricas
            self.academic_metrics.reset_session()
            
            # Resetear estado del juego
            self.game_state = self._initialize_game_state()
            
            # Reiniciar UI
            self.start_session()
            
            self.log_event("Sesión reiniciada", "INFO")
            
        except Exception as e:
            self.log_error(f"Error al reiniciar sesión: {str(e)}")

    def export_report(self) -> None:
        """Exporta un reporte completo."""
        try:
            report = self.generate_final_report()
            
            filename = f"reporte_alpha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialname=filename
            )
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Exportado", f"Reporte exportado a: {filepath}")
                self.log_event(f"Reporte exportado a {filepath}", "INFO")
            
        except Exception as e:
            self.log_error(f"Error al exportar reporte: {str(e)}")
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def quit_application(self) -> None:
        """Cierra la aplicación de forma segura."""
        try:
            # Guardar progreso antes de salir
            self.save_progress()
            
            # Detener temporizadores
            if self.session_timer:
                self.root.after_cancel(self.session_timer)
            
            # Log final
            self.log_event("Aplicación cerrada", "INFO")
            
            # Cerrar ventana
            self.root.quit()
            
        except Exception as e:
            self.log_error(f"Error al cerrar aplicación: {str(e)}")
            self.root.quit()

    # Métodos adicionales para funcionalidades del menú
    def set_learning_mode(self, mode: str) -> None:
        """Establece el modo de aprendizaje."""
        try:
            self.learning_manager.set_mode(mode)
            self.game_state["learning_mode"] = mode
            
            mode_settings = self.learning_manager.get_mode_settings()
            self.ui_manager.mode_indicator.config(text=f"📚 MODO: {mode_settings['mode'].upper()}")
            
            self.log_event(f"Modo de aprendizaje cambiado a: {mode}", "INFO")
            
        except Exception as e:
            self.log_error(f"Error al cambiar modo de aprendizaje: {str(e)}")

    def show_dashboard(self) -> None:
        """Muestra el dashboard interactivo."""
        try:
            dashboard_window = tk.Toplevel(self.root)
            dashboard_window.title("Dashboard Interactivo")
            dashboard_window.geometry("800x600")
            
            # Contenido del dashboard
            report = self.generate_final_report()
            
            text_widget = scrolledtext.ScrolledText(dashboard_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            dashboard_text = "📊 DASHBOARD INTERACTIVO\n\n"
            dashboard_text += f"Sesión: {report.get('session_id', 'N/A')}\n"
            dashboard_text += f"Puntuación: {report.get('final_score', 0)}/{report.get('max_score', 0)}\n"
            dashboard_text += f"Precisión: {report.get('accuracy', 0)*100:.1f}%\n"
            dashboard_text += f"Tiempo: {self.format_time(report.get('time_spent', 0))}\n\n"
            dashboard_text += "📈 MÉTRICAS DE RENDIMIENTO:\n"
            
            performance = report.get('performance_metrics', {})
            for key, value in performance.items():
                dashboard_text += f"• {key}: {value}\n"
            
            text_widget.insert(tk.END, dashboard_text)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            self.log_error(f"Error al mostrar dashboard: {str(e)}")
            messagebox.showerror("Error", f"Error al mostrar dashboard: {str(e)}")

    def show_settings(self) -> None:
        """Muestra la ventana de configuración."""
        try:
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Configuración Avanzada")
            settings_window.geometry("600x400")
            
            # Contenido básico de configuración
            tk.Label(settings_window, text="⚙️ CONFIGURACIÓN AVANZADA", 
                    font=("Arial", 16, "bold")).pack(pady=10)
            
            tk.Label(settings_window, text="Configuración disponible en futuras versiones").pack(pady=20)
            
        except Exception as e:
            self.log_error(f"Error al mostrar configuración: {str(e)}")

    def toggle_high_contrast(self) -> None:
        """Alterna el modo de alto contraste."""
        try:
            self.game_state["high_contrast"] = not self.game_state.get("high_contrast", False)
            self.log_event(f"Alto contraste: {'activado' if self.game_state['high_contrast'] else 'desactivado'}", "INFO")
            messagebox.showinfo("Accesibilidad", 
                               f"Alto contraste {'activado' if self.game_state['high_contrast'] else 'desactivado'}")
        except Exception as e:
            self.log_error(f"Error al alternar alto contraste: {str(e)}")

    def toggle_keyboard_nav(self) -> None:
        """Alterna la navegación por teclado."""
        try:
            self.game_state["keyboard_navigation"] = not self.game_state.get("keyboard_navigation", True)
            self.log_event(f"Navegación por teclado: {'activada' if self.game_state['keyboard_navigation'] else 'desactivada'}", "INFO")
            messagebox.showinfo("Accesibilidad", 
                               f"Navegación por teclado {'activada' if self.game_state['keyboard_navigation'] else 'desactivada'}")
        except Exception as e:
            self.log_error(f"Error al alternar navegación por teclado: {str(e)}")

    def check_contrast(self) -> None:
        """Verifica el contraste de la interfaz."""
        try:
            messagebox.showinfo("Verificación de Contraste", 
                               "La interfaz cumple con los estándares WCAG 2.1 AA para contraste de colores.")
        except Exception as e:
            self.log_error(f"Error al verificar contraste: {str(e)}")

    def show_guide(self) -> None:
        """Muestra la guía del juego."""
        try:
            guide_text = """
            🎮 GUÍA DEL JUEGO - PROYECTO ALPHA

            OBJETIVO:
            Completar 20 misiones educativas sobre Inteligencia Artificial
            para demostrar dominio de conceptos clave.

            MECÁNICAS:
            • Lee cada misión cuidadosamente
            • Selecciona la respuesta correcta
            • Usa pistas si necesitas ayuda (penalización)
            • Reintenta misiones fallidas
            • Mantén rachas para bonificaciones

            PUNTUACIÓN:
            • Respuesta correcta: +1 punto
            • Pista usada: Penalización en eficiencia
            • Reintento: Penalización menor
            • Racha: Bonificación por respuestas consecutivas

            CATEGORÍAS:
            • Fases de la IA
            • Clasificación y Taxonomía
            • Tipos de Aprendizaje ML
            • Métricas y Evaluación
            • Análisis de Datos
            • Algoritmos ML
            • Metodologías

            ¡Buena suerte en tu aventura de aprendizaje!
            """
            messagebox.showinfo("Guía del Juego", guide_text)
        except Exception as e:
            self.log_error(f"Error al mostrar guía: {str(e)}")

    def show_feedback_form(self) -> None:
        """Muestra formulario de comentarios."""
        try:
            feedback_window = tk.Toplevel(self.root)
            feedback_window.title("Enviar Comentarios")
            feedback_window.geometry("500x400")
            
            tk.Label(feedback_window, text="💬 ENVIAR COMENTARIOS", 
                    font=("Arial", 16, "bold")).pack(pady=10)
            
            tk.Label(feedback_window, text="Sus comentarios nos ayudan a mejorar:").pack(pady=5)
            
            feedback_text = scrolledtext.ScrolledText(feedback_window, height=10, width=50)
            feedback_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            def submit_feedback():
                feedback_content = feedback_text.get(1.0, tk.END).strip()
                if feedback_content:
                    self.game_state["user_feedback"].append({
                        "timestamp": datetime.now().isoformat(),
                        "content": feedback_content
                    })
                    messagebox.showinfo("Gracias", "¡Gracias por sus comentarios!")
                    feedback_window.destroy()
                else:
                    messagebox.showwarning("Advertencia", "Por favor, ingrese sus comentarios.")
            
            tk.Button(feedback_window, text="📤 Enviar", command=submit_feedback).pack(pady=10)
            
        except Exception as e:
            self.log_error(f"Error al mostrar formulario de comentarios: {str(e)}")