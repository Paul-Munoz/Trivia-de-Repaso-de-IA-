"""
UI Manager Module - Proyecto Alpha v4.0
Gestor de interfaz de usuario y componentes visuales.
"""

import tkinter as tk
from tkinter import ttk, Canvas, scrolledtext, messagebox, filedialog
from typing import Dict, Any, Optional, Callable, List
import time
from datetime import datetime

from config import COLORS, UI_CONFIG, PROFESSIONAL_CONFIG
import logging
from academic_metrics import AcademicMetrics
from achievement_system import AchievementSystem


class UIManager:
    """
    Gestor centralizado de la interfaz de usuario.

    Maneja todos los componentes visuales, layouts, estilos y
    interacciones de usuario de manera organizada y accesible.
    """

    def __init__(self, root: tk.Tk):
        self.logger = logging.getLogger(self.__class__.__name__)
        """Inicializa el gestor de UI."""
        self.root = root
        self.style = ttk.Style()

        # Componentes principales
        self.main_canvas = None
        self.progress_canvas = None
        self.story_label = None
        self.feedback_label = None
        self.metrics_label = None
        self.mission_title_label = None
        self.timer_label = None
        self.progress_label = None
        self.mode_indicator = None

        # Contenedores
        self.options_frame = None
        self.main_container = None
        self.side_frame = None

        # Barras de menú
        self.menubar = None

        # Variables de estado
        self.focusable_widgets = []
        self.current_focus_index = 0
        self.after_id = None

        # Variables de texto
        self.story_text_var = tk.StringVar()
        self.progress_text_var = tk.StringVar()
        self.feedback_text_var = tk.StringVar()
        self.timer_text_var = tk.StringVar()
        self.metrics_text_var = tk.StringVar()

        # Configurar estilos y tema
        self.setup_styles()
        self.setup_fonts()

    def setup_styles(self) -> None:
        """Configura estilos ttk profesionales."""
        self.style.configure('Professional.TButton',
                           font=UI_CONFIG["font_button"],
                           padding=10)
        self.style.configure('Professional.TLabel',
                           font=UI_CONFIG["font_body"])
        self.style.configure('Card.TFrame',
                           relief='raised',
                           borderwidth=2)

    def setup_fonts(self) -> None:
        """Configura fuentes tipográficas modernas."""
        # Intentar usar Inter, fallback a fuentes del sistema
        try:
            # En un entorno real, cargaríamos la fuente Inter
            # Por ahora usamos fuentes del sistema similares
            self.fonts = {
                "title": ("Arial", 28, "bold"),
                "header": ("Arial", 20, "bold"),
                "subheader": ("Arial", 18, "bold"),
                "body": ("Arial", 16, "normal"),
                "caption": ("Arial", 14, "normal"),
                "small": ("Arial", 12, "normal"),
                "button": ("Arial", 14, "bold"),
                "metrics": ("Arial", 13, "normal"),
            }
        except:
            # Fallback a configuración original
            self.fonts = {
                "title": UI_CONFIG["font_title"],
                "header": UI_CONFIG["font_header"],
                "subheader": UI_CONFIG["font_subheader"],
                "body": UI_CONFIG["font_body"],
                "caption": UI_CONFIG["font_caption"],
                "small": UI_CONFIG["font_small"],
                "button": UI_CONFIG["font_button"],
                "metrics": UI_CONFIG["font_metrics"],
            }

    def _is_mac(self) -> bool:
        """Verifica si estamos en macOS."""
        import platform
        return platform.system() == "Darwin"

    def create_main_layout(self) -> None:
        """Crea el layout principal de la aplicación."""
        # Frame principal con scroll
        self.main_container = tk.Frame(self.root, bg=COLORS["bg_primary"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas con scrollbar para contenido extenso
        self.main_canvas = Canvas(self.main_container, bg=COLORS["bg_primary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.main_canvas.yview)
        scrollable_frame = tk.Frame(self.main_canvas, bg=COLORS["bg_primary"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        # Contenido principal
        main_frame = tk.Frame(scrollable_frame, bg=COLORS["bg_primary"], padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear secciones principales
        self.create_header_section(main_frame)
        self.create_progress_section(main_frame)
        self.create_content_section(main_frame)
        self.create_options_section(main_frame)
        self.create_feedback_section(main_frame)
        self.create_controls_section(main_frame)

        # Configuración final del scroll
        scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # Bindings para scroll
        self.setup_scroll_bindings()

    def create_header_section(self, parent: tk.Frame) -> None:
        """Crea la sección de encabezado moderna."""
        header_frame = tk.Frame(parent, bg=COLORS["bg_primary"], height=UI_CONFIG["header_height"])
        header_frame.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_lg"]))
        header_frame.pack_propagate(False)

        # Logo y título principal
        title_frame = tk.Frame(header_frame, bg=COLORS["bg_primary"])
        title_frame.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_lg"])

        # Icono moderno
        logo_label = tk.Label(title_frame, text="🧠",
                             font=("SF Pro Display", 32),
                             bg=COLORS["bg_primary"], fg=COLORS["primary"])
        logo_label.pack(side=tk.LEFT, padx=(0, UI_CONFIG["spacing_md"]))

        # Título principal
        title_label = tk.Label(title_frame, text="PROYECTO ALPHA",
                              font=self.fonts["title"],
                              bg=COLORS["bg_primary"], fg=COLORS["text_primary"])
        title_label.pack(side=tk.LEFT)

        # Subtítulo
        subtitle_label = tk.Label(title_frame, text="Sistema Educativo de IA Avanzada",
                                 font=self.fonts["caption"],
                                 bg=COLORS["bg_primary"], fg=COLORS["text_secondary"])
        subtitle_label.pack(side=tk.LEFT, padx=(UI_CONFIG["spacing_sm"], 0))

        # Indicador de modo moderno
        mode_frame = tk.Frame(header_frame, bg=COLORS["bg_primary"])
        mode_frame.pack(side=tk.RIGHT, padx=UI_CONFIG["spacing_lg"])

        self.mode_indicator = tk.Label(mode_frame, text="🎯 MODO: ADAPTATIVO",
                                      font=self.fonts["caption"],
                                      bg=COLORS["primary"], fg=COLORS["text_white"],
                                      padx=UI_CONFIG["spacing_md"], pady=UI_CONFIG["spacing_xs"],
                                      relief="flat", borderwidth=0)
        self.mode_indicator.pack()

    def create_progress_section(self, parent: tk.Frame) -> None:
        """Crea la sección de progreso moderna."""
        progress_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
        progress_frame.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_lg"]))

        # Información de progreso
        progress_info_frame = tk.Frame(progress_frame, bg=COLORS["bg_primary"])
        progress_info_frame.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_md"]))

        # Etiqueta de progreso
        self.progress_label = tk.Label(progress_info_frame, textvariable=self.progress_text_var,
                                      font=self.fonts["header"],
                                      bg=COLORS["bg_primary"],
                                      fg=COLORS["text_primary"])
        self.progress_label.pack(side=tk.LEFT)

        # Temporizador moderno
        timer_frame = tk.Frame(progress_info_frame, bg=COLORS["bg_primary"])
        timer_frame.pack(side=tk.RIGHT)

        timer_icon = tk.Label(timer_frame, text="⏱️",
                             font=self.fonts["caption"],
                             bg=COLORS["bg_primary"], fg=COLORS["text_secondary"])
        timer_icon.pack(side=tk.LEFT, padx=(0, UI_CONFIG["spacing_xs"]))

        self.timer_label = tk.Label(timer_frame, textvariable=self.timer_text_var,
                                   font=self.fonts["caption"],
                                   bg=COLORS["bg_primary"], fg=COLORS["text_primary"])
        self.timer_label.pack(side=tk.LEFT)

        # Barra de progreso moderna
        progress_bar_frame = tk.Frame(progress_frame, bg=COLORS["bg_primary"])
        progress_bar_frame.pack(fill=tk.X)

        # Contenedor de la barra
        bar_container = tk.Frame(progress_bar_frame, bg="lightgray",
                                height=8, relief="flat", borderwidth=0)
        bar_container.pack(fill=tk.X, padx=UI_CONFIG["spacing_lg"])
        bar_container.pack_propagate(False)

        # Barra de progreso (se actualizará dinámicamente)
        self.progress_bar = tk.Frame(bar_container, bg="blue",
                                    height=8, width=0)
        self.progress_bar.pack(side=tk.LEFT)

        # Etiqueta de porcentaje
        self.progress_percentage_label = tk.Label(progress_bar_frame, text="0%",
                                                 font=self.fonts["small"],
                                                 bg=COLORS["bg_primary"], fg=COLORS["text_secondary"])
        self.progress_percentage_label.pack(side=tk.RIGHT, padx=UI_CONFIG["spacing_lg"])

    def create_content_section(self, parent: tk.Frame) -> None:
        """Crea la sección de contenido educativo moderna."""
        # Card principal para el contenido
        content_card = tk.Frame(parent, bg=COLORS["bg_card"],
                               relief="flat", borderwidth=0)
        content_card.pack(fill=tk.X, pady=UI_CONFIG["spacing_lg"])

        # Sombra sutil (simulada con borde)
        content_container = tk.Frame(content_card, bg=COLORS["bg_card"],
                                    padx=UI_CONFIG["card_padding"], pady=UI_CONFIG["card_padding"],
                                    relief="solid", borderwidth=1)
        content_container.pack(fill=tk.X, padx=UI_CONFIG["spacing_md"], pady=UI_CONFIG["spacing_md"])

        # Header de la misión
        mission_header = tk.Frame(content_container, bg=COLORS["bg_card"])
        mission_header.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_lg"]))

        # Badge de misión
        mission_badge = tk.Frame(mission_header, bg=COLORS["primary"],
                                padx=UI_CONFIG["spacing_sm"], pady=UI_CONFIG["spacing_xs"])
        mission_badge.pack(side=tk.LEFT)

        mission_badge_label = tk.Label(mission_badge, text="🎯 MISIÓN",
                                      font=self.fonts["small"], bg=COLORS["primary"],
                                      fg=COLORS["text_white"])
        mission_badge_label.pack()

        # Título de la misión
        self.mission_title_label = tk.Label(mission_header, text="",
                                           font=self.fonts["subheader"],
                                           bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        self.mission_title_label.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_md"])

        # Separador visual
        separator = tk.Frame(content_container, bg=COLORS["border_light"], height=1)
        separator.pack(fill=tk.X, pady=UI_CONFIG["spacing_md"])

        # Contenido de la historia
        story_frame = tk.Frame(content_container, bg=COLORS["bg_card"])
        story_frame.pack(fill=tk.X)

        # Texto de la historia - moderna y legible
        self.story_label = tk.Label(story_frame, textvariable=self.story_text_var,
                                   wraplength=UI_CONFIG["content_max_width"], justify=tk.LEFT,
                                   font=self.fonts["body"], bg=COLORS["bg_card"],
                                   fg=COLORS["text_primary"], anchor="w")
        self.story_label.pack(fill=tk.X, anchor=tk.W)

    def create_options_section(self, parent: tk.Frame) -> None:
        """Crea la sección de opciones interactivas moderna."""
        options_container = tk.Frame(parent, bg=COLORS["bg_primary"])
        options_container.pack(fill=tk.X, pady=UI_CONFIG["spacing_lg"])

        # Header de opciones
        options_header = tk.Frame(options_container, bg=COLORS["bg_primary"])
        options_header.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_lg"]))

        # Icono y título
        options_icon = tk.Label(options_header, text="🎯",
                               font=self.fonts["subheader"],
                               bg=COLORS["bg_primary"], fg=COLORS["primary"])
        options_icon.pack(side=tk.LEFT)

        options_title = tk.Label(options_header, text="Elige la mejor respuesta",
                                font=self.fonts["subheader"],
                                bg=COLORS["bg_primary"], fg=COLORS["text_primary"])
        options_title.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_sm"])

        # Frame para las opciones con layout moderno
        self.options_frame = tk.Frame(options_container, bg=COLORS["bg_primary"])
        self.options_frame.pack(fill=tk.X)

    def create_feedback_section(self, parent: tk.Frame) -> None:
        """Crea la sección de feedback y métricas moderna."""
        feedback_container = tk.Frame(parent, bg=COLORS["bg_primary"])
        feedback_container.pack(fill=tk.X, pady=UI_CONFIG["spacing_lg"])

        # Card de feedback
        feedback_card = tk.Frame(feedback_container, bg=COLORS["bg_card"],
                                relief="flat", borderwidth=0)
        feedback_card.pack(fill=tk.X)

        feedback_inner = tk.Frame(feedback_card, bg=COLORS["bg_card"],
                                 padx=UI_CONFIG["card_padding"], pady=UI_CONFIG["card_padding"],
                                 relief="solid", borderwidth=1)
        feedback_inner.pack(fill=tk.X, padx=UI_CONFIG["spacing_md"], pady=UI_CONFIG["spacing_md"])

        # Header de feedback
        feedback_header = tk.Frame(feedback_inner, bg=COLORS["bg_card"])
        feedback_header.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_md"]))

        feedback_icon = tk.Label(feedback_header, text="💬",
                                font=self.fonts["caption"],
                                bg=COLORS["bg_card"], fg=COLORS["primary"])
        feedback_icon.pack(side=tk.LEFT)

        feedback_title = tk.Label(feedback_header, text="Retroalimentación",
                                 font=self.fonts["caption"],
                                 bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        feedback_title.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_sm"])

        # Separador
        separator = tk.Frame(feedback_inner, bg=COLORS["border_light"], height=1)
        separator.pack(fill=tk.X, pady=UI_CONFIG["spacing_sm"])

        # Feedback principal
        self.feedback_label = tk.Label(feedback_inner, textvariable=self.feedback_text_var,
                                      wraplength=UI_CONFIG["content_max_width"], justify=tk.LEFT,
                                      font=self.fonts["body"], bg=COLORS["bg_card"],
                                      fg=COLORS["text_primary"])
        self.feedback_label.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_md"]))

        # Métricas en tiempo real
        metrics_frame = tk.Frame(feedback_inner, bg=COLORS["bg_card"])
        metrics_frame.pack(fill=tk.X)

        metrics_icon = tk.Label(metrics_frame, text="📊",
                               font=self.fonts["small"],
                               bg=COLORS["bg_card"], fg=COLORS["text_secondary"])
        metrics_icon.pack(side=tk.LEFT)

        self.metrics_label = tk.Label(metrics_frame, textvariable=self.metrics_text_var,
                                     font=self.fonts["caption"], bg=COLORS["bg_card"],
                                     fg=COLORS["text_secondary"])
        self.metrics_label.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_xs"])

    def create_controls_section(self, parent: tk.Frame) -> None:
        """Crea la sección de controles principales moderna."""
        controls_frame = tk.Frame(parent, bg=COLORS["bg_primary"])
        controls_frame.pack(fill=tk.X, pady=UI_CONFIG["spacing_lg"])

        # Contenedor centrado para botones
        button_container = tk.Frame(controls_frame, bg=COLORS["bg_primary"])
        button_container.pack(anchor=tk.CENTER)

        # Botón principal moderno
        self.next_button = tk.Button(button_container, text="🚀 Empezar aventura",
                                    bg=COLORS["primary"], fg=COLORS["text_white"],
                                    font=self.fonts["button"], relief="flat", borderwidth=0,
                                    padx=UI_CONFIG["spacing_xl"], pady=UI_CONFIG["spacing_md"],
                                    state=tk.DISABLED, cursor="hand2",
                                    activebackground=COLORS["primary_dark"],
                                    activeforeground=COLORS["text_white"])
        self.next_button.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_md"])

        # Botón de pista moderno
        self.hint_button = tk.Button(button_container, text="💡 Pista",
                                    bg=COLORS["warning"], fg=COLORS["text_white"],
                                    font=self.fonts["button"], relief="flat", borderwidth=0,
                                    padx=UI_CONFIG["spacing_lg"], pady=UI_CONFIG["spacing_md"],
                                    state=tk.DISABLED, cursor="hand2",
                                    activebackground=COLORS["warning"],
                                    activeforeground=COLORS["text_white"])
        self.hint_button.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_md"])

        # Botón de reintento moderno
        self.retry_button = tk.Button(button_container, text="🔄 Reintentar",
                                     bg=COLORS["secondary"], fg=COLORS["text_white"],
                                     font=self.fonts["button"], relief="flat", borderwidth=0,
                                     padx=UI_CONFIG["spacing_lg"], pady=UI_CONFIG["spacing_md"],
                                     state=tk.DISABLED, cursor="hand2",
                                     activebackground=COLORS["text_secondary"],
                                     activeforeground=COLORS["text_white"])
        self.retry_button.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_md"])

    def create_side_panel(self) -> None:
        """Crea el panel lateral moderno con estadísticas."""
        self.side_frame = tk.Frame(self.root, bg=COLORS["bg_primary"],
                                  width=UI_CONFIG["sidebar_width"])
        self.side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=UI_CONFIG["spacing_md"],
                           pady=UI_CONFIG["spacing_md"])
        self.side_frame.pack_propagate(False)

        # Header del panel
        panel_header = tk.Frame(self.side_frame, bg=COLORS["bg_primary"])
        panel_header.pack(fill=tk.X, pady=(UI_CONFIG["spacing_lg"], UI_CONFIG["spacing_md"]))

        panel_icon = tk.Label(panel_header, text="📊",
                             font=self.fonts["header"],
                             bg=COLORS["bg_primary"], fg=COLORS["primary"])
        panel_icon.pack(side=tk.LEFT)

        panel_title = tk.Label(panel_header, text="Panel de Control",
                              font=self.fonts["header"],
                              bg=COLORS["bg_primary"], fg=COLORS["text_primary"])
        panel_title.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_sm"])

        # Estadísticas actuales en cards modernas
        stats_container = tk.Frame(self.side_frame, bg=COLORS["bg_primary"])
        stats_container.pack(fill=tk.X, padx=UI_CONFIG["spacing_md"])

        self.stats_labels = {}
        stats = [
            ("Puntuación", "0/21"),
            ("Racha", "0"),
            ("Mejor Racha", "0"),
            ("Pistas Usadas", "0"),
            ("Reintentos", "0"),
            ("Tiempo", "00:00:00")
        ]

        for label_text, value in stats:
            # Card para cada estadística
            stat_card = tk.Frame(stats_container, bg=COLORS["bg_card"],
                                relief="flat", borderwidth=0)
            stat_card.pack(fill=tk.X, pady=UI_CONFIG["spacing_xs"])

            stat_inner = tk.Frame(stat_card, bg=COLORS["bg_card"],
                                 padx=UI_CONFIG["spacing_md"], pady=UI_CONFIG["spacing_sm"],
                                 relief="solid", borderwidth=1)
            stat_inner.pack(fill=tk.X, padx=UI_CONFIG["spacing_xs"], pady=UI_CONFIG["spacing_xs"])

            # Etiqueta y valor
            tk.Label(stat_inner, text=label_text, font=self.fonts["small"],
                    bg=COLORS["bg_card"], fg=COLORS["text_secondary"], anchor="w").pack(side=tk.LEFT)
            self.stats_labels[label_text] = tk.Label(stat_inner, text=value, font=self.fonts["caption"],
                                                    bg=COLORS["bg_card"], fg=COLORS["text_primary"], anchor="e")
            self.stats_labels[label_text].pack(side=tk.RIGHT)

        # Logros recientes
        achievements_container = tk.Frame(self.side_frame, bg=COLORS["bg_primary"])
        achievements_container.pack(fill=tk.BOTH, expand=True, padx=UI_CONFIG["spacing_md"],
                                   pady=UI_CONFIG["spacing_md"])

        # Header de logros
        achievements_header = tk.Frame(achievements_container, bg=COLORS["bg_primary"])
        achievements_header.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_md"]))

        achievements_icon = tk.Label(achievements_header, text="🏆",
                                    font=self.fonts["subheader"],
                                    bg=COLORS["bg_primary"], fg=COLORS["accent"])
        achievements_icon.pack(side=tk.LEFT)

        achievements_title = tk.Label(achievements_header, text="Logros",
                                     font=self.fonts["subheader"],
                                     bg=COLORS["bg_primary"], fg=COLORS["text_primary"])
        achievements_title.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_sm"])

        # Card de logros
        achievements_card = tk.Frame(achievements_container, bg=COLORS["bg_card"],
                                    relief="flat", borderwidth=0)
        achievements_card.pack(fill=tk.BOTH, expand=True)

        achievements_inner = tk.Frame(achievements_card, bg=COLORS["bg_card"],
                                     padx=UI_CONFIG["card_padding"], pady=UI_CONFIG["card_padding"],
                                     relief="solid", borderwidth=1)
        achievements_inner.pack(fill=tk.BOTH, expand=True, padx=UI_CONFIG["spacing_xs"],
                               pady=UI_CONFIG["spacing_xs"])

        self.achievements_text = scrolledtext.ScrolledText(achievements_inner, height=8, width=25,
                                                          bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                                                          font=self.fonts["small"], relief="flat",
                                                          borderwidth=0)
        self.achievements_text.pack(fill=tk.BOTH, expand=True)
        self.achievements_text.insert(tk.END, "¡Comienza a jugar para\ndesbloquear logros!")
        self.achievements_text.config(state=tk.DISABLED)

    def create_animations_canvas(self) -> None:
        """Crea el canvas para animaciones visuales modernas."""
        # Canvas principal para logo y branding
        self.canvas = Canvas(self.root, width=UI_CONFIG["window_width"]//2, height=200,
                            bg=COLORS["bg_primary"], highlightthickness=0)
        self.canvas.pack(side=tk.TOP, pady=UI_CONFIG["spacing_lg"])

        # Barra de progreso integrada (ya no es un canvas separado)
        # Se maneja en create_progress_section

    def setup_animations(self) -> None:
        """Configura animaciones visuales modernas."""
        # Limpiar canvas anterior
        self.canvas.delete("all")

        # Centro del canvas
        center_x = UI_CONFIG["window_width"] // 4  # Mitad del ancho del canvas

        # Logo moderno con gradiente visual
        self.canvas.create_text(center_x, 80, text="🧠",
                               font=("SF Pro Display", 48),
                               fill=COLORS["primary"], justify=tk.CENTER)

        self.canvas.create_text(center_x, 120, text="PROYECTO ALPHA",
                               font=self.fonts["title"],
                               fill=COLORS["text_primary"], justify=tk.CENTER)

        self.canvas.create_text(center_x, 150, text="Sistema Educativo de IA Avanzada",
                               font=self.fonts["caption"],
                               fill=COLORS["text_secondary"], justify=tk.CENTER)

        self.canvas.create_text(center_x, 175, text="Versión 4.0 Profesional",
                               font=self.fonts["small"],
                               fill=COLORS["text_muted"], justify=tk.CENTER)

        # Indicador de estado moderno
        self.status_indicator = self.canvas.create_text(center_x, 200,
                                                       text="Sistema listo para evaluación académica",
                                                       font=self.fonts["small"],
                                                       fill=COLORS["text_secondary"], justify=tk.CENTER)

    def create_menu_bar(self, callbacks: Dict[str, Callable]) -> None:
        """Crea la barra de menú profesional."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Menú Archivo
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="📁 Archivo", menu=file_menu)
        file_menu.add_command(label="🆕 Nueva Sesión", command=callbacks.get("new_session"))
        file_menu.add_command(label="💾 Guardar Progreso", command=callbacks.get("save_progress"))
        file_menu.add_command(label="📂 Cargar Progreso", command=callbacks.get("load_progress"))
        file_menu.add_separator()
        file_menu.add_command(label="📊 Exportar Reporte Completo", command=callbacks.get("export_report"))
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Salir", command=callbacks.get("exit"))

        # Menú Modo de Aprendizaje
        mode_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="🎓 Modo de Aprendizaje", menu=mode_menu)
        mode_menu.add_command(label="🧠 Adaptativo (Recomendado)", command=lambda: callbacks.get("set_mode")("adaptive"))
        mode_menu.add_command(label="📝 Modo Quiz", command=lambda: callbacks.get("set_mode")("quiz"))
        mode_menu.add_command(label="📚 Modo Estudio", command=lambda: callbacks.get("set_mode")("study"))
        mode_menu.add_command(label="🔄 Modo Repaso", command=lambda: callbacks.get("set_mode")("review"))

        # Menú Herramientas
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="🛠️ Herramientas", menu=tools_menu)
        tools_menu.add_command(label="📊 Dashboard Interactivo", command=callbacks.get("show_dashboard"))
        tools_menu.add_separator()
        tools_menu.add_command(label="⚙️ Configuración Avanzada", command=callbacks.get("show_settings"))

        # Menú Accesibilidad
        accessibility_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="♿ Accesibilidad", menu=accessibility_menu)
        accessibility_menu.add_checkbutton(label="Modo Alto Contraste", command=callbacks.get("toggle_contrast"))
        accessibility_menu.add_checkbutton(label="Navegación por Teclado", command=callbacks.get("toggle_keyboard"))
        accessibility_menu.add_separator()
        accessibility_menu.add_command(label="🔍 Verificar Contraste", command=callbacks.get("check_contrast"))

        # Menú Ayuda
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="❓ Ayuda", menu=help_menu)
        help_menu.add_command(label="📖 Tutorial Interactivo", command=callbacks.get("show_tutorial"))
        help_menu.add_command(label="🎮 Guía de Juego", command=callbacks.get("show_guide"))
        help_menu.add_separator()
        help_menu.add_command(label="💬 Enviar Comentarios", command=callbacks.get("show_feedback"))
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ Acerca de Proyecto Alpha", command=callbacks.get("show_about"))

        # Atajos de teclado
        self.setup_keyboard_shortcuts(callbacks)

    def setup_keyboard_shortcuts(self, callbacks: Dict[str, Callable]) -> None:
        """Configura atajos de teclado."""
        shortcuts = {
            '<Control-n>': callbacks.get("new_session"),
            '<Control-s>': callbacks.get("save_progress"),
            '<Control-o>': callbacks.get("load_progress"),
            '<Control-q>': callbacks.get("exit"),
            '<Key>': self.handle_keyboard_navigation
        }

        for key, callback in shortcuts.items():
            if callback:
                self.root.bind(key, lambda e, cb=callback: cb() if callable(cb) else None)

    def setup_scroll_bindings(self) -> None:
        """Configura bindings para scroll con mouse."""
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.main_canvas.bind('<Enter>', lambda e: self._bound_to_mousewheel(e, self.main_canvas))
        self.main_canvas.bind('<Leave>', lambda e: self._unbound_to_mousewheel(e, self.main_canvas))

    def update_progress_display(self, score: int, max_score: int) -> None:
        """Actualiza la visualización de progreso moderna."""
        if max_score > 0 and hasattr(self, 'progress_bar'):
            percentage = int((score / max_score) * 100)
            # Calcular ancho basado en el contenedor (asumiendo 800px de ancho disponible)
            progress_width = int((percentage / 100) * 800)
            self.progress_bar.config(width=progress_width, bg="blue")
            self.progress_percentage_label.config(text=f"{percentage}%")

    def update_stats_display(self, stats: Dict[str, Any]) -> None:
        """Actualiza la visualización de estadísticas."""
        mappings = {
            "Puntuación": f"{stats.get('score', 0)}/{stats.get('max_score', 21)}",
            "Racha": str(stats.get('streak', 0)),
            "Mejor Racha": str(stats.get('best_streak', 0)),
            "Pistas Usadas": str(stats.get('hints_used', 0)),
            "Reintentos": str(stats.get('retries', 0)),
            "Tiempo": stats.get('time_formatted', '00:00:00')
        }

        for label, value in mappings.items():
            if label in self.stats_labels:
                self.stats_labels[label].config(text=value)

    def update_achievements_display(self, achievements: List[str]) -> None:
        """Actualiza la visualización de logros."""
        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)

        if achievements:
            for achievement in achievements[-5:]:  # Mostrar últimos 5
                self.achievements_text.insert(tk.END, achievement + "\n")
        else:
            self.achievements_text.insert(tk.END, "¡Comienza a jugar para\ndesbloquear logros!")

        self.achievements_text.config(state=tk.DISABLED)

    def clear_options(self) -> None:
        """Limpia todas las opciones de respuesta."""
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def create_option_buttons(self, mission_data: Dict[str, Any], callback: Callable) -> None:
        """Crea botones de opción interactivos modernos."""
        options = list(mission_data["options"].items())

        for i, (choice_key, choice_description) in enumerate(options):
            # Card de opción moderna
            option_card = tk.Frame(self.options_frame, bg=COLORS["bg_card"],
                                  relief="flat", borderwidth=0, cursor="hand2")
            option_card.pack(fill=tk.X, padx=UI_CONFIG["spacing_lg"], pady=UI_CONFIG["spacing_sm"])

            # Contenedor interno con borde sutil
            option_inner = tk.Frame(option_card, bg=COLORS["bg_card"],
                                   padx=UI_CONFIG["card_padding"], pady=UI_CONFIG["card_padding"],
                                   relief="solid", borderwidth=1)
            option_inner.pack(fill=tk.X, padx=UI_CONFIG["spacing_xs"], pady=UI_CONFIG["spacing_xs"])

            # Header de opción
            option_header = tk.Frame(option_inner, bg=COLORS["bg_card"])
            option_header.pack(fill=tk.X, pady=(0, UI_CONFIG["spacing_sm"]))

            # Letra de opción (A, B, C, etc.)
            option_letter = chr(65 + i)  # A, B, C...
            letter_badge = tk.Frame(option_header, bg=COLORS["primary"],
                                   padx=UI_CONFIG["spacing_sm"], pady=UI_CONFIG["spacing_xs"])
            letter_badge.pack(side=tk.LEFT)

            letter_label = tk.Label(letter_badge, text=option_letter,
                                   font=self.fonts["caption"], bg=COLORS["primary"],
                                   fg=COLORS["text_white"])
            letter_label.pack()

            # Título de opción
            option_title = tk.Label(option_header, text=choice_key,
                                   font=self.fonts["body"], bg=COLORS["bg_card"],
                                   fg=COLORS["text_primary"])
            option_title.pack(side=tk.LEFT, padx=UI_CONFIG["spacing_md"])

            # Descripción
            description_label = tk.Label(option_inner, text=choice_description,
                                        font=self.fonts["caption"], bg=COLORS["bg_card"],
                                        fg=COLORS["text_secondary"], wraplength=UI_CONFIG["content_max_width"],
                                        justify=tk.LEFT)
            description_label.pack(fill=tk.X, anchor=tk.W)

            # Efectos hover modernos
            def on_enter(e, card=option_card, inner=option_inner):
                card.config(bg=COLORS["bg_overlay"])
                inner.config(border=COLORS["primary"])

            def on_leave(e, card=option_card, inner=option_inner):
                card.config(bg=COLORS["bg_card"])
                inner.config(border=COLORS["border_light"])

            option_card.bind("<Enter>", on_enter)
            option_card.bind("<Leave>", on_leave)
            option_inner.bind("<Enter>", on_enter)
            option_inner.bind("<Leave>", on_leave)
            option_title.bind("<Enter>", on_enter)
            option_title.bind("<Leave>", on_leave)
            description_label.bind("<Enter>", on_enter)
            description_label.bind("<Leave>", on_leave)

            # Evento de selección
            def select_option(e, key=choice_key, card=option_card):
                callback(key, card)

            option_card.bind("<Button-1>", select_option)
            option_inner.bind("<Button-1>", select_option)
            option_title.bind("<Button-1>", select_option)
            description_label.bind("<Button-1>", select_option)

    def show_message(self, title: str, message: str, type: str = "info") -> None:
        """Muestra un mensaje al usuario."""
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)

    def show_tutorial(self) -> None:
        """Muestra el tutorial de la aplicación."""
        tutorial_text = """
        TUTORIAL - PROYECTO ALPHA

        🎯 OBJETIVO:
        Aprender conceptos clave de Inteligencia Artificial
        completando misiones interactivas.

        🎮 CÓMO JUGAR:
        1. Lee la historia de cada misión
        2. Elige la respuesta correcta entre las opciones
        3. Recibe feedback inmediato sobre tu elección
        4. Usa pistas si necesitas ayuda (penalización)
        5. Reintenta misiones si fallas

        📊 MODOS DE APRENDIZAJE:
        • Quiz: Evaluación tradicional
        • Estudio: Más explicaciones detalladas
        • Repaso: Enfoque en conceptos difíciles

        🏆 SISTEMA DE PUNTUACIÓN:
        • Respuestas correctas: +1 punto
        • Pistas usadas: Penalización en puntuación máxima
        • Racha: Bonus por respuestas consecutivas

        💡 CONSEJOS:
        • Lee atentamente cada misión
        • Usa pistas solo cuando sea necesario
        • Revisa conceptos que te cuesten más
        • Mantén rachas para mejores puntuaciones

        ¡Buena suerte, Comandante!
        """
        messagebox.showinfo("Tutorial", tutorial_text)

    def show_about(self) -> None:
        """Muestra información sobre el proyecto."""
        about_text = """
        PROYECTO ALPHA - PLATAFORMA EDUCATIVA DE IA

        Versión: 4.0 - Arquitectura Modular Profesional

        Desarrollado para facilitar el aprendizaje de
        conceptos fundamentales de Inteligencia Artificial
        de manera interactiva y atractiva.

        Características principales:
        ✓ Arquitectura modular con clases especializadas
        ✓ Sistema de aprendizaje adaptativo avanzado
        ✓ Métricas académicas profesionales
        ✓ Desafíos temporales y elementos competitivos
        ✓ Sistema de evaluación comprehensivo
        ✓ Reportes académicos detallados
        ✓ Interfaz de usuario moderna y accesible
        ✓ Sistema de logros y gamificación avanzado

        ¡Transformando el aprendizaje en una aventura!
        """
        messagebox.showinfo("Acerca de", about_text)

    def handle_keyboard_navigation(self, event) -> None:
        """Maneja navegación por teclado para accesibilidad."""
        if not PROFESSIONAL_CONFIG.get("keyboard_navigation", True):
            return

        key = event.keysym

        if key == 'Tab':
            self.navigate_to_next_focusable_element()
            return "break"  # Prevenir comportamiento por defecto
        elif key == 'Return' and self.focusable_widgets:
            current_widget = self.focusable_widgets[self.current_focus_index]
            if hasattr(current_widget, 'invoke'):
                current_widget.invoke()
            elif hasattr(current_widget, 'event_generate'):
                current_widget.event_generate('<Button-1>')
        elif key in ['Up', 'Down', 'Left', 'Right']:
            self.handle_arrow_navigation(key)

    def navigate_to_next_focusable_element(self) -> None:
        """Navega al siguiente elemento enfocable."""
        if not self.focusable_widgets:
            self.update_focusable_widgets()

        if self.focusable_widgets:
            # Remover foco anterior
            if hasattr(self.focusable_widgets[self.current_focus_index], 'config'):
                self.focusable_widgets[self.current_focus_index].config(relief=tk.RAISED)

            # Mover al siguiente
            self.current_focus_index = (self.current_focus_index + 1) % len(self.focusable_widgets)

            # Aplicar foco nuevo
            current_widget = self.focusable_widgets[self.current_focus_index]
            if hasattr(current_widget, 'config'):
                current_widget.config(relief=tk.SUNKEN)
                current_widget.focus_set()

    def update_focusable_widgets(self) -> None:
        """Actualiza la lista de widgets enfocables."""
        self.focusable_widgets = [
            self.next_button,
            self.hint_button,
            self.retry_button
        ]

        # Agregar opciones si existen
        if self.options_frame:
            for widget in self.options_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    self.focusable_widgets.append(widget)

    def handle_arrow_navigation(self, direction: str) -> None:
        """Maneja navegación con flechas."""
        if direction in ['Up', 'Down']:
            self.navigate_to_next_focusable_element()

    def _on_mousewheel(self, event) -> None:
        """Maneja el scroll del mouse."""
        try:
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass

    def _bound_to_mousewheel(self, event, canvas: Canvas) -> None:
        """Vincula el scroll al canvas."""
        try:
            canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        except:
            pass

    def _unbound_to_mousewheel(self, event, canvas: Canvas) -> None:
        """Desvincula el scroll del canvas."""
        try:
            canvas.unbind_all("<MouseWheel>")
        except:
            pass

    def type_story_effect(self, full_text: str, callback: callable = None) -> None:
        """Implementa el efecto de escritura de teletipo."""
        if not hasattr(self, '_story_idx'):
            self._story_idx = 0
            self.story_text_var.set("")

        if self._story_idx < len(full_text):
            current_char = full_text[self._story_idx]
            self.story_text_var.set(self.story_text_var.get() + current_char)
            self._story_idx += 1
            self.after_id = self.root.after(30, lambda: self.type_story_effect(full_text, callback))
        else:
            self.after_id = None
            self._story_idx = 0
            if callback:
                callback()