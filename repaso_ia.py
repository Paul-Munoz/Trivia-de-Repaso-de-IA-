# -*- coding: utf-8 -*-
"""
Trivia de Repaso de IA - Versión Profesional Mejorada
Aplicación educativa interactiva para repasar conceptos de Inteligencia Artificial
utilizando la librería gráfica Tkinter.

Este archivo contiene toda la lógica:
1. Gestión de datos (Configuración, Preguntas, Estadísticas).
2. Estructura de la aplicación con Tkinter (QuizGame).
3. Interfaces de usuario (StartScreen, QuizScreen, ResultScreen).
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# ==============================================================================
# 1. CONFIGURACIÓN INICIAL Y LOGGING
# ==============================================================================

# Constantes para los nombres de los archivos de datos
LOG_FILE = 'repaso_ia.log'
CONFIG_FILE = "config.json"
QUESTIONS_FILE = "questions_data.json"
STATS_FILE = "game_stats.json"

try:
    # Configuración de logging para registrar eventos en consola y archivo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
except Exception:
    # Fallback básico si hay problemas con la configuración avanzada
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==============================================================================
# 2. ESTRUCTURAS DE DATOS (Dataclasses)
# ==============================================================================

@dataclass
class Question:
    """
    Estructura de datos para una pregunta.
    Contiene la pregunta, las opciones, la respuesta correcta,
    el concepto relacionado, una explicación/fórmula, y la categoría.
    """
    question: str
    options: List[str]
    answer: str
    concept: str
    formula: str  # Usado para la explicación en modo estudio
    category: str = "General"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        """
        Crea una instancia de Question desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la pregunta.

        Returns:
            Una instancia de Question.

        Raises:
            ValueError: Si los datos del diccionario son inválidos o incompletos.
        """
        try:
            return cls(**data)
        except (TypeError, KeyError) as e:
            logger.error(f"Error creando Question desde dict: {e}")
            raise ValueError(f"Datos de pregunta inválidos: {e}")

@dataclass
class GameSession:
    """
    Estructura para almacenar los datos de una sesión de juego.
    Incluye puntuación, errores, número total de preguntas,
    tiempo de inicio y fin, y la categoría seleccionada.
    """
    score: int = 0
    errors: int = 0
    total_questions: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    category: str = "Todas"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la sesión a diccionario para serialización JSON.

        Returns:
            Diccionario con datos de la sesión listos para JSON.
        """
        data = asdict(self)
        # Convertir objetos datetime a cadenas ISO 8601 para JSON
        if self.start_time is not None:
            data['start_time'] = self.start_time.isoformat()
        if self.end_time is not None:
            data['end_time'] = self.end_time.isoformat()
        return data


# ==============================================================================
# 3. GESTORES DE DATOS (Managers)
# ==============================================================================

class ConfigManager:
    """Gestor de configuración y temas de la aplicación."""

    def __init__(self, config_file: str = CONFIG_FILE):
        """
        Inicializa el gestor, carga la configuración y establece el tema.
        
        Args:
            config_file: Ruta al archivo de configuración.
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.current_theme = "light"

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Define y retorna la configuración por defecto de la aplicación.
        
        Returns:
            Diccionario con la configuración predeterminada.
        """
        return {
            "app": {
                "title": "Trivia de Repaso de IA",
                "version": "2.1",
                "window_size": {"width": 900, "height": 700}
            },
            "themes": {
                "light": {
                    "bg_primary": "#F0F4F8",        # Fondo principal claro
                    "bg_secondary": "#FFFFFF",      # Fondo de secciones (tarjetas)
                    "primary_blue": "#4A90E2",      # Color principal para títulos/botones
                    "secondary_green": "#4CAF50",   # Color para éxito/iniciar
                    "color_error": "#D32F2F",       # Color para errores
                    "text_dark": "#2C3E50",         # Texto oscuro
                    "text_light": "#FFFFFF",        # Texto claro
                    "accent_highlight": "#FFC107"   # Acento/Alerta (Amarillo)
                }
                # Aquí se añadiría un tema "dark" si estuviera implementado
            }
        }

    def _load_config(self) -> Dict[str, Any]:
        """
        Carga la configuración desde un archivo JSON o usa la por defecto.

        Returns:
            Diccionario con la configuración cargada.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error cargando configuración, usando valores por defecto: {e}")
            return self._get_default_config()

    def get_colors(self) -> Dict[str, str]:
        """
        Obtiene el diccionario de colores del tema actual.
        
        Returns:
            Diccionario de colores (e.g., {"bg_primary": "#F0F4F8", ...}).
        """
        themes = self.config.get("themes", {})
        return themes.get(self.current_theme, themes.get("light", {}))

    def toggle_theme(self) -> None:
        """
        Alterna entre tema claro y oscuro (solo para futuras implementaciones).
        """
        self.current_theme = "dark" if self.current_theme == "light" else "light"


class QuestionManager:
    """Gestor de preguntas, responsable de cargar, almacenar y filtrar las preguntas."""

    def __init__(self, questions_file: str = QUESTIONS_FILE):
        """
        Inicializa el gestor y carga las preguntas desde el archivo.

        Args:
            questions_file: Ruta al archivo JSON de preguntas.
        """
        self.questions_file = questions_file
        self.questions: List[Question] = []
        self.categories: List[str] = []
        self._load_questions()

    def _load_questions(self) -> None:
        """Carga las preguntas desde el archivo JSON de datos y extrae categorías."""
        try:
            if os.path.exists(self.questions_file):
                with open(self.questions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convertir cada diccionario a un objeto Question
                    self.questions = [Question.from_dict(q) for q in data]
                    # Extraer categorías únicas y ordenarlas
                    self.categories = sorted(list(set(q.category for q in self.questions)))
                    logger.info(f"Cargadas {len(self.questions)} preguntas")
            else:
                logger.warning(f"Archivo de preguntas no encontrado: {self.questions_file}")
                self.questions = []
                self.categories = []
        except Exception as e:
            logger.error(f"Error cargando preguntas: {e}")
            self.questions = []
            self.categories = []

    def get_questions_by_category(self, category: str = "Todas") -> List[Question]:
        """
        Obtiene una lista de preguntas filtradas por la categoría especificada.
        Si la categoría es "Todas", retorna todas las preguntas.

        Args:
            category: Nombre de la categoría a filtrar.

        Returns:
            Lista de objetos Question.
        """
        if not self.questions:
            logger.warning("No hay preguntas disponibles")
            return []

        if category == "Todas":
            # Retorna una copia para evitar modificar la lista original (ej. al mezclar)
            return self.questions.copy()

        filtered = [q for q in self.questions if q.category == category]
        if not filtered:
            logger.warning(f"No se encontraron preguntas para la categoría: {category}")
        return filtered


class StatsManager:
    """Gestor de estadísticas de juego, encargado de cargar y guardar sesiones."""

    def __init__(self, stats_file: str = STATS_FILE):
        """
        Inicializa el gestor y carga las estadísticas existentes.

        Args:
            stats_file: Ruta al archivo JSON de estadísticas.
        """
        self.stats_file = stats_file
        self.stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        """
        Carga las estadísticas de juego desde el archivo JSON.

        Returns:
            Diccionario con las estadísticas (o estructura por defecto).
        """
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Retorna estructura por defecto si no existe el archivo
                return {"total_games": 0, "sessions": []}
        except Exception as e:
            logger.error(f"Error cargando estadísticas: {e}")
            return {"total_games": 0, "sessions": []}

    def save_session(self, session: GameSession) -> None:
        """
        Guarda una sesión de juego completada en el archivo de estadísticas.
        Mantiene un máximo de 50 sesiones recientes.

        Args:
            session: Objeto GameSession a guardar.
        """
        try:
            self.stats["total_games"] += 1
            self.stats["sessions"].append(session.to_dict())

            # Limitar el historial a las últimas 50 sesiones para evitar archivos grandes
            if len(self.stats["sessions"]) > 50:
                self.stats["sessions"] = self.stats["sessions"][-50:]

            with open(self.stats_file, 'w', encoding='utf-8') as f:
                # El indent=2 mejora la legibilidad del JSON
                json.dump(self.stats, f, indent=2, ensure_ascii=False)

            logger.info(f"Sesión guardada: {session.score}/{session.total_questions}")
        except Exception as e:
            logger.error(f"Error guardando sesión: {e}")


# ==============================================================================
# 4. APLICACIÓN PRINCIPAL (QuizGame)
# ==============================================================================

class QuizGame(tk.Tk):
    """
    Clase principal de la aplicación.
    Hereda de tk.Tk, gestiona la interfaz, el estado del juego y la navegación entre pantallas.
    """

    def __init__(self):
        super().__init__()

        # Inicialización de gestores de datos
        self.config_manager = ConfigManager()
        self.question_manager = QuestionManager()
        self.stats_manager = StatsManager()

        # Estado del juego
        self.current_session = GameSession()
        self.current_questions: List[Question] = []
        self.current_question_index = 0
        self.selected_category = tk.StringVar(value="Todas")
        self.study_mode = tk.BooleanVar(value=False)

        self._setup_window()

        self.frames: Dict[str, tk.Frame] = {}
        self._create_frames()

        # Inicia la aplicación en la pantalla de inicio
        self.show_frame("StartScreen")

    def _setup_window(self) -> None:
        """Configura el título, tamaño, tema y centrado de la ventana principal."""
        config = self.config_manager.config
        app_config = config["app"]

        self.title(app_config["title"])
        size = app_config["window_size"]
        self.geometry(f"{size['width']}x{size['height']}")
        self.minsize(800, 600)

        self._center_window(size['width'], size['height'])

        colors = self.config_manager.get_colors()
        self.configure(bg=colors.get("bg_primary", "#F0F4F8"))

    def _center_window(self, width: int, height: int) -> None:
        """
        Calcula las coordenadas para centrar la ventana en la pantalla.
        
        Args:
            width: Ancho de la ventana.
            height: Alto de la ventana.
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_frames(self) -> None:
        """Crea el contenedor principal y todas las pantallas (frames) de la aplicación."""
        colors = self.config_manager.get_colors()
        container = tk.Frame(self, bg=colors.get("bg_primary", "#F0F4F8"))
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Definir las clases de las pantallas
        screen_classes = (StartScreen, QuizScreen, ResultScreen)
        for F in screen_classes:
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            # Colocar todos los frames en la misma posición (0, 0)
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name: str) -> None:
        """
        Muestra un frame específico y llama a su método `on_show` si existe.

        Args:
            frame_name: Nombre de la clase del frame a mostrar.
        """
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()  # Trae el frame deseado al frente
            if hasattr(frame, 'on_show'):
                frame.on_show()

    def start_quiz(self) -> None:
        """
        Prepara el juego: carga preguntas por categoría, las mezcla
        e inicializa la sesión.
        """
        try:
            category = self.selected_category.get()
            self.current_questions = self.question_manager.get_questions_by_category(category)

            if not self.current_questions:
                messagebox.showwarning("Advertencia", f"No hay preguntas disponibles para '{category}'. Intente otra categoría.")
                return

            random.shuffle(self.current_questions)

            # Inicializar la nueva sesión de juego
            self.current_session = GameSession(
                total_questions=len(self.current_questions),
                start_time=datetime.now(),
                category=category
            )

            self.current_question_index = 0

            # Navegar a la pantalla del quiz y cargar la primera pregunta
            self.frames["QuizScreen"].load_question()
            self.show_frame("QuizScreen")

        except Exception as e:
            logger.error(f"Error iniciando quiz: {e}")
            messagebox.showerror("Error", f"No se pudo iniciar el quiz. Verifique el archivo de preguntas (questions_data.json).")

    def check_answer(self, selected_option: str) -> None:
        """
        Verifica si la respuesta seleccionada es correcta, actualiza la puntuación
        y muestra el feedback.
        
        Args:
            selected_option: La opción seleccionada por el usuario.
        """
        if self.current_question_index >= len(self.current_questions):
            return

        current_question = self.current_questions[self.current_question_index]
        is_correct = selected_option == current_question.answer

        if is_correct:
            self.current_session.score += 1
        else:
            self.current_session.errors += 1

        # Generar feedback
        quiz_screen = self.frames["QuizScreen"]
        colors = self.config_manager.get_colors()

        if is_correct:
            feedback_text = "✅ ¡Correcto!"
            feedback_color = colors.get("secondary_green", "#4CAF50")
        else:
            feedback_text = f"❌ Incorrecto. Respuesta correcta: {current_question.answer}"
            feedback_color = colors.get("color_error", "#D32F2F")

        # Añadir explicación en modo estudio
        if self.study_mode.get():
            feedback_text += f"\n\n💡 Concepto clave: {current_question.formula}"

        quiz_screen.show_feedback(feedback_text, feedback_color)

        # Configurar un retraso antes de pasar a la siguiente pregunta
        delay = 3000 if self.study_mode.get() else 1500
        self.after(delay, self.next_question)

    def next_question(self) -> None:
        """Pasa a la siguiente pregunta o finaliza el quiz si no quedan más."""
        quiz_screen = self.frames["QuizScreen"]
        quiz_screen.clear_feedback()

        self.current_question_index += 1

        if self.current_question_index < len(self.current_questions):
            quiz_screen.load_question()
        else:
            self.show_results()

    def show_results(self) -> None:
        """Finaliza la sesión de juego, guarda las estadísticas y muestra la pantalla de resultados."""
        try:
            self.current_session.end_time = datetime.now()

            # Guardar la sesión antes de mostrar resultados
            self.stats_manager.save_session(self.current_session)

            result_screen = self.frames.get("ResultScreen")
            if result_screen:
                result_screen.display_results(
                    self.current_session.score,
                    self.current_session.errors,
                    self.current_session.total_questions
                )
                self.show_frame("ResultScreen")
            else:
                raise RuntimeError("ResultScreen no encontrada")

        except Exception as e:
            logger.error(f"Error mostrando resultados: {e}")
            messagebox.showerror("Error", f"No se pudieron mostrar los resultados: {e}")


# ==============================================================================
# 5. PANTALLAS DE LA INTERFAZ (Frames)
# ==============================================================================

class BaseScreen(tk.Frame):
    """Clase base para las pantallas para centralizar la configuración de colores."""
    def __init__(self, parent: tk.Frame, controller: QuizGame):
        """Inicializa la pantalla base y aplica el tema."""
        super().__init__(parent)
        self.controller = controller
        # Obtener los colores del tema actual
        self.colors = controller.config_manager.get_colors()
        self.configure(bg=self.colors.get("bg_primary", "#F0F4F8"))

class StartScreen(BaseScreen):
    """Pantalla de inicio: configuración de categoría y modo de estudio."""

    def __init__(self, parent: tk.Frame, controller: QuizGame):
        super().__init__(parent, controller)
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Crea los widgets de la pantalla de inicio."""
        title = tk.Label(self, text="🎓 Trivia de Repaso de IA 🤖",
                        font=("Arial", 28, "bold"),
                        bg=self.colors.get("bg_primary"),
                        fg=self.colors.get("primary_blue"))
        title.pack(pady=(40, 20))

        subtitle = tk.Label(self, text="Repasa conceptos clave de Inteligencia Artificial",
                           font=("Arial", 14),
                           bg=self.colors.get("bg_primary"),
                           fg=self.colors.get("text_dark"))
        subtitle.pack(pady=(0, 30))

        # --- Frame de Configuración ---
        config_frame = tk.LabelFrame(self, text="⚙️ Configuración",
                                   font=("Arial", 12, "bold"),
                                   bg=self.colors.get("bg_secondary"),
                                   fg=self.colors.get("text_dark"),
                                   padx=20, pady=15)
        config_frame.pack(pady=20, padx=40, fill="x", ipadx=5, ipady=5)
        config_frame.grid_columnconfigure(1, weight=1) # Permite que el combobox se expanda

        # Selección de Categoría
        tk.Label(config_frame, text="Categoría:",
                font=("Arial", 11),
                bg=self.colors.get("bg_secondary"),
                fg=self.colors.get("text_dark")).grid(row=0, column=0, sticky="w", pady=5, padx=5)

        categories = ["Todas"] + self.controller.question_manager.categories
        category_combo = ttk.Combobox(config_frame,
                                    textvariable=self.controller.selected_category,
                                    values=categories,
                                    state="readonly", # No permite escribir, solo seleccionar
                                    width=30)
        category_combo.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="ew")
        category_combo.set(self.controller.selected_category.get())

        # Modo Estudio
        study_check = tk.Checkbutton(config_frame,
                                   text="Modo estudio (mostrar respuesta y explicación tras responder)",
                                   variable=self.controller.study_mode,
                                   font=("Arial", 10),
                                   bg=self.colors.get("bg_secondary"),
                                   fg=self.colors.get("text_dark"),
                                   selectcolor=self.colors.get("bg_secondary"))
        study_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=10, padx=5)

        # --- Frame de Información ---
        info_frame = tk.LabelFrame(self, text="📊 Información",
                                 font=("Arial", 12, "bold"),
                                 bg=self.colors.get("bg_secondary"),
                                 fg=self.colors.get("text_dark"),
                                 padx=20, pady=15)
        info_frame.pack(pady=20, padx=40, fill="x", ipadx=5, ipady=5)

        self.questions_label = tk.Label(info_frame,
                                      text="Cargando...",
                                      font=("Arial", 11),
                                      bg=self.colors.get("bg_secondary"),
                                      fg=self.colors.get("text_dark"))
        self.questions_label.pack(anchor="w")

        # --- Botón de Inicio ---
        start_btn = tk.Button(self, text="🚀 EMPEZAR QUIZ",
                            command=self.controller.start_quiz,
                            font=("Arial", 16, "bold"),
                            bg=self.colors.get("secondary_green"),
                            fg=self.colors.get("text_light"),
                            padx=30, pady=12,
                            relief=tk.FLAT, # Estilo plano para una apariencia moderna
                            cursor="hand2")
        start_btn.pack(pady=30)

    def on_show(self) -> None:
        """Se llama cuando la pantalla de inicio se trae al frente. Actualiza la información."""
        self._update_info()

    def _update_info(self) -> None:
        """Actualiza el texto con el número total de preguntas y categorías cargadas."""
        try:
            question_manager = self.controller.question_manager
            total_questions = len(question_manager.questions)
            categories_count = len(question_manager.categories)

            info_text = f"Total de preguntas cargadas: {total_questions} en {categories_count} categorías"
            self.questions_label.config(text=info_text)
        except Exception as e:
            logger.error(f"Error actualizando información: {e}")
            self.questions_label.config(text="Error cargando información")

class QuizScreen(BaseScreen):
    """Pantalla principal del quiz: muestra la pregunta y las opciones."""

    def __init__(self, parent: tk.Frame, controller: QuizGame):
        super().__init__(parent, controller)
        self.selected_option = tk.StringVar()
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Crea los widgets de la pantalla del quiz (encabezado, pregunta, opciones, feedback)."""
        # --- Encabezado y Progreso ---
        header_frame = tk.Frame(self, bg=self.colors.get("bg_primary"))
        header_frame.pack(fill="x", pady=(20, 10), padx=40)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        self.question_label = tk.Label(header_frame,
                                     text="Pregunta X / Y",
                                     font=("Arial", 14, "bold"),
                                     bg=self.colors.get("bg_primary"),
                                     fg=self.colors.get("primary_blue"))
        self.question_label.grid(row=0, column=0, sticky="w")

        self.score_label = tk.Label(header_frame,
                                  text="✅ 0 | ❌ 0",
                                  font=("Arial", 14, "bold"),
                                  bg=self.colors.get("bg_primary"),
                                  fg=self.colors.get("text_dark"))
        self.score_label.grid(row=0, column=1, sticky="e")

        # Barra de progreso (ttk.Progressbar usa estilos del sistema, es moderno)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self,
                                           variable=self.progress_var,
                                           maximum=100,
                                           mode='determinate')
        self.progress_bar.pack(fill="x", pady=(0, 20), padx=40)

        # --- Contenedor Principal de Pregunta ---
        main_frame = tk.Frame(self,
                            bg=self.colors.get("bg_secondary"),
                            relief=tk.RAISED,
                            bd=1,
                            padx=30,
                            pady=30)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.category_label = tk.Label(main_frame,
                                     text="", # Categoría
                                     font=("Arial", 12, "bold"),
                                     bg=self.colors.get("bg_secondary"),
                                     fg=self.colors.get("accent_highlight"))
        self.category_label.pack(pady=(0, 10), anchor="w")

        self.question_text = tk.Label(main_frame,
                                    text="", # Texto de la pregunta
                                    font=("Arial", 16, "bold"),
                                    bg=self.colors.get("bg_secondary"),
                                    fg=self.colors.get("text_dark"),
                                    wraplength=750, # Ajusta el texto al ancho
                                    justify=tk.LEFT)
        self.question_text.pack(pady=(0, 25), fill="x")

        # --- Opciones de Respuesta ---
        self.options_frame = tk.Frame(main_frame, bg=self.colors.get("bg_secondary"))
        self.options_frame.pack(fill="x", pady=(0, 20))

        self.option_buttons = []
        for i in range(4):
            # Uso de Radiobutton para selección única
            rb = tk.Radiobutton(self.options_frame,
                              text="",
                              variable=self.selected_option,
                              value="",
                              font=("Arial", 12),
                              bg=self.colors.get("bg_secondary"),
                              fg=self.colors.get("text_dark"),
                              selectcolor=self.colors.get("bg_secondary"), # Evita el cambio de color de fondo al seleccionar
                              activebackground=self.colors.get("bg_secondary"),
                              anchor="w",
                              padx=10,
                              pady=8,
                              command=self._enable_submit)
            rb.pack(fill="x", pady=3)
            self.option_buttons.append(rb)

        # --- Feedback y Explicación ---
        self.feedback_label = tk.Label(main_frame,
                                     text="",
                                     font=("Arial", 12),
                                     bg=self.colors.get("bg_secondary"),
                                     fg=self.colors.get("text_dark"),
                                     wraplength=750,
                                     justify=tk.LEFT)
        self.feedback_label.pack(pady=10, fill="x")

        # --- Botón de Envío ---
        self.submit_button = tk.Button(self,
                                     text="✅ ENVIAR RESPUESTA",
                                     command=self._submit_answer,
                                     font=("Arial", 14, "bold"),
                                     bg=self.colors.get("primary_blue"),
                                     fg=self.colors.get("text_light"),
                                     padx=20,
                                     pady=10,
                                     relief=tk.FLAT,
                                     state=tk.DISABLED, # Deshabilitado hasta seleccionar una opción
                                     cursor="hand2")
        self.submit_button.pack(pady=20)

    def load_question(self) -> None:
        """Carga los datos de la pregunta actual y actualiza la interfaz."""
        try:
            q_index = self.controller.current_question_index
            total_q = len(self.controller.current_questions)
            if q_index >= total_q:
                return

            self.selected_option.set("")
            self.submit_button.config(state=tk.DISABLED)
            self.clear_feedback()

            question_data = self.controller.current_questions[q_index]

            # Actualizar progreso y puntuación
            self.question_label.config(text=f"Pregunta {q_index + 1} / {total_q}")
            self.score_label.config(text=f"✅ {self.controller.current_session.score} | ❌ {self.controller.current_session.errors}")
            progress = ((q_index + 1) / total_q) * 100
            self.progress_var.set(progress)

            # Actualizar texto de pregunta
            self.category_label.config(text=f"📚 {question_data.category}")
            self.question_text.config(text=question_data.question)

            # Mezclar opciones antes de mostrarlas (importante para evitar sesgos)
            options = question_data.options.copy()
            random.shuffle(options)

            # Configurar botones de opción
            for i, option in enumerate(options[:4]):
                if i < len(self.option_buttons):
                    self.option_buttons[i].config(text=option, value=option, state=tk.NORMAL)

            # Deshabilitar botones no usados (si hay menos de 4 opciones)
            for i in range(len(options), len(self.option_buttons)):
                self.option_buttons[i].config(text="", value="", state=tk.DISABLED)

            self._enable_options(True)
        except Exception as e:
            logger.error(f"Error cargando pregunta: {e}")
            messagebox.showerror("Error", f"No se pudo cargar la pregunta: {e}")

    def _enable_submit(self) -> None:
        """Habilita el botón de enviar solo si una opción ha sido seleccionada."""
        if self.selected_option.get():
            self.submit_button.config(state=tk.NORMAL)

    def _submit_answer(self) -> None:
        """Llama a la lógica de verificación de respuesta del controlador."""
        selected = self.selected_option.get()
        if selected:
            self.controller.check_answer(selected)

    def _enable_options(self, enabled: bool) -> None:
        """
        Habilita o deshabilita todos los botones de opción.

        Args:
            enabled: True para habilitar, False para deshabilitar.
        """
        state = tk.NORMAL if enabled else tk.DISABLED
        for rb in self.option_buttons:
            # Solo cambiar el estado de los que realmente tienen texto (opción válida)
            if rb.cget('text'):
                rb.config(state=state)

    def show_feedback(self, text: str, color: str) -> None:
        """
        Muestra el feedback (Correcto/Incorrecto) y la explicación.
        
        Args:
            text: Mensaje de feedback.
            color: Color del mensaje.
        """
        self.feedback_label.config(text=text, fg=color, font=("Arial", 12, "bold"))
        self.submit_button.config(state=tk.DISABLED)
        self._enable_options(False) # Bloquea las opciones después de responder

    def clear_feedback(self) -> None:
        """Limpia el feedback para la siguiente pregunta."""
        self.feedback_label.config(text="")

class ResultScreen(BaseScreen):
    """Pantalla de resultados finales del quiz."""

    def __init__(self, parent: tk.Frame, controller: QuizGame):
        super().__init__(parent, controller)
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Crea los widgets de la pantalla de resultados."""
        self.title_label = tk.Label(self,
                                  text="🌟 ¡Quiz Completado! 🌟",
                                  font=("Arial", 28, "bold"),
                                  bg=self.colors.get("bg_primary"),
                                  fg=self.colors.get("primary_blue"))
        self.title_label.pack(pady=(50, 30))

        # --- Frame de Estadísticas ---
        stats_frame = tk.LabelFrame(self,
                                  text="📊 Resultados",
                                  font=("Arial", 14, "bold"),
                                  bg=self.colors.get("bg_secondary"),
                                  fg=self.colors.get("text_dark"),
                                  padx=40,
                                  pady=30)
        stats_frame.pack(pady=30, padx=50, ipadx=10, ipady=10)

        self.score_label = tk.Label(stats_frame,
                                  text="",
                                  font=("Arial", 16, "bold"),
                                  bg=self.colors.get("bg_secondary"),
                                  fg=self.colors.get("secondary_green"))
        self.score_label.pack(pady=10)

        self.errors_label = tk.Label(stats_frame,
                                   text="",
                                   font=("Arial", 14),
                                   bg=self.colors.get("bg_secondary"),
                                   fg=self.colors.get("color_error"))
        self.errors_label.pack(pady=5)

        self.percentage_label = tk.Label(stats_frame,
                                       text="",
                                       font=("Arial", 14),
                                       bg=self.colors.get("bg_secondary"),
                                       fg=self.colors.get("text_dark"))
        self.percentage_label.pack(pady=5)

        # Mensaje de ánimo/reconocimiento
        self.message_label = tk.Label(self,
                                    text="",
                                    font=("Arial", 12),
                                    bg=self.colors.get("bg_primary"),
                                    fg=self.colors.get("text_dark"),
                                    wraplength=600,
                                    justify=tk.CENTER)
        self.message_label.pack(pady=30, padx=40)

        # --- Botones de Navegación ---
        button_frame = tk.Frame(self, bg=self.colors.get("bg_primary"))
        button_frame.pack(pady=30)

        restart_btn = tk.Button(button_frame,
                              text="🔄 JUGAR DE NUEVO",
                              command=self._restart_quiz,
                              font=("Arial", 14, "bold"),
                              bg=self.colors.get("secondary_green"),
                              fg=self.colors.get("text_light"),
                              padx=20,
                              pady=10,
                              relief=tk.FLAT,
                              cursor="hand2")
        restart_btn.pack(side=tk.LEFT, padx=10)

        start_btn = tk.Button(button_frame,
                            text="🏠 VOLVER AL INICIO",
                            command=self._back_to_start,
                            font=("Arial", 12),
                            bg=self.colors.get("primary_blue"),
                            fg=self.colors.get("text_light"),
                            padx=15,
                            pady=8,
                            relief=tk.FLAT,
                            cursor="hand2")
        start_btn.pack(side=tk.LEFT, padx=10)

    def display_results(self, score: int, errors: int, total: int) -> None:
        """
        Calcula el porcentaje y muestra los resultados y un mensaje motivacional.

        Args:
            score: Puntuación de respuestas correctas.
            errors: Número de errores.
            total: Número total de preguntas.
        """
        try:
            percentage = (score / total * 100) if total > 0 else 0

            self.score_label.config(text=f"Puntuación: {score} de {total} correctas")
            self.errors_label.config(text=f"Errores: {errors}")
            self.percentage_label.config(text=f"Porcentaje de acierto: {percentage:.1f}%")

            # Lógica para el mensaje y color del título
            if percentage == 100:
                message = "🎉 ¡Perfecto! Dominas completamente el tema."
                title_color = self.colors.get("secondary_green")
            elif percentage >= 80:
                message = "👍 ¡Excelente! Muy buen dominio del material."
                title_color = self.colors.get("primary_blue")
            elif percentage >= 60:
                message = "📚 Buen trabajo. Sigue practicando para mejorar."
                title_color = self.colors.get("accent_highlight")
            else:
                message = "🧐 Necesitas repasar más. ¡No te rindas!"
                title_color = self.colors.get("color_error")

            self.title_label.config(fg=title_color)
            self.message_label.config(text=message)
        except Exception as e:
            logger.error(f"Error mostrando resultados: {e}")
            self.score_label.config(text="Error calculando resultados")

    def _restart_quiz(self) -> None:
        """Llama al controlador para reiniciar el quiz con la misma configuración (categoría/modo estudio)."""
        try:
            self.controller.start_quiz()
        except Exception as e:
            logger.error(f"Error reiniciando quiz: {e}")
            messagebox.showerror("Error", f"No se pudo reiniciar el quiz: {e}")

    def _back_to_start(self) -> None:
        """Vuelve a la pantalla de inicio para cambiar la configuración o empezar de nuevo."""
        try:
            self.controller.show_frame("StartScreen")
        except Exception as e:
            logger.error(f"Error volviendo al inicio: {e}")
            messagebox.showerror("Error", f"No se pudo volver al inicio: {e}")


# ==============================================================================
# 6. PUNTO DE ENTRADA
# ==============================================================================

def main():
    """Función principal para inicializar y ejecutar la aplicación."""
    try:
        logger.info("Iniciando aplicación de repaso de IA")
        app = QuizGame()
        app.mainloop()  # Bucle principal de Tkinter
    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
    except Exception as e:
        logger.critical(f"Error crítico en la aplicación: {e}", exc_info=True)
        try:
            # Mostrar un messagebox con el error antes de cerrar
            messagebox.showerror("Error Crítico",
                               f"Se produjo un error crítico:\n\n{str(e)}\n\n"
                               "La aplicación se cerrará. Consulte repaso_ia.log para más detalles.")
        except Exception:
            print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()

# ==============================================================================
# 7. INSTRUCCIONES DE USO
# ==============================================================================

# NOTA IMPORTANTE:
# Para que la aplicación funcione correctamente, debe crear el archivo 
# de preguntas en el mismo directorio que el script Python:
#
# Archivo requerido: questions_data.json
#
# EJEMPLO MÍNIMO DE questions_data.json:
# [
#   {
#     "question": "¿Qué algoritmo de aprendizaje supervisado se usa para clasificación y regresión?",
#     "options": ["K-Means", "Random Forest", "PCA", "Autoencoder"],
#     "answer": "Random Forest",
#     "concept": "Aprendizaje Supervisado",
#     "formula": "Random Forest construye múltiples árboles de decisión y combina sus resultados para mejorar la precisión y evitar el sobreajuste. Es un algoritmo de ensemble.",
#     "category": "Algoritmos Clásicos"
#   },
#   {
#     "question": "¿Cuál es la función de activación más común en las capas ocultas de una red neuronal profunda?",
#     "options": ["Sigmoid", "Tanh", "Softmax", "ReLU"],
#     "answer": "ReLU",
#     "concept": "Redes Neuronales",
#     "formula": "La función ReLU (Rectified Linear Unit) es f(x) = max(0, x). Es popular por mitigar el problema del gradiente desvanecido y acelerar la convergencia.",
#     "category": "Deep Learning"
#   }
# ]
#
# Otros archivos (opcionales):
# - config.json: Si no existe, usa la configuración de tema y tamaño de ventana por defecto.
# - game_stats.json: Se creará automáticamente al finalizar la primera sesión de juego.