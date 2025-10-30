"""
UI Manager Futurístico - Proyecto Alpha v4.0
Interfaz futurística con letras grandes y colores amigables para la vista.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from typing import Dict, Any, Optional, Callable, List


class UIManager:
    """Gestor de interfaz futurística con excelente legibilidad."""

    def __init__(self, root: tk.Tk):
        """Inicializa el gestor de UI futurístico."""
        self.root = root
        
        # Configurar ventana principal
        self.root.configure(bg='#0a0a0a')  # Negro suave
        self.root.geometry("1400x900")
        self.root.title("🚀 PROYECTO ALPHA - SISTEMA EDUCATIVO FUTURÍSTICO DE IA")
        
        # Colores futurísticos amigables para la vista
        self.colors = {
            "bg_main": "#0a0a0a",        # Negro suave
            "bg_card": "#1a1a2e",        # Azul oscuro suave
            "bg_option": "#16213e",      # Azul medio
            "bg_selected": "#0f3460",    # Azul selección
            "text_main": "#e0e6ed",      # Blanco suave
            "text_bright": "#ffffff",    # Blanco puro
            "text_secondary": "#a8b2d1", # Gris azulado
            "accent": "#00d4ff",         # Cian brillante
            "success": "#00ff88",        # Verde neón suave
            "error": "#ff6b6b",          # Rojo suave
            "warning": "#ffa726",        # Naranja suave
            "glow": "#4fc3f7"            # Azul glow
        }
        
        # Fuentes grandes y legibles
        self.fonts = {
            "title": ("Arial", 28, "bold"),
            "header": ("Arial", 22, "bold"),
            "subheader": ("Arial", 18, "bold"),
            "body": ("Arial", 16, "normal"),
            "body_large": ("Arial", 18, "normal"),
            "caption": ("Arial", 14, "normal"),
            "button": ("Arial", 16, "bold"),
            "stats": ("Arial", 14, "bold")
        }
        
        # Variables de texto
        self.story_text_var = tk.StringVar()
        self.progress_text_var = tk.StringVar()
        self.feedback_text_var = tk.StringVar()
        self.timer_text_var = tk.StringVar()
        self.metrics_text_var = tk.StringVar()
        
        # Componentes principales
        self.main_frame = None
        self.story_label = None
        self.feedback_label = None
        self.metrics_label = None
        self.mission_title_label = None
        self.timer_label = None
        self.progress_label = None
        self.mode_indicator = None
        self.options_frame = None
        self.next_button = None
        self.hint_button = None
        self.retry_button = None
        self.stats_labels = {}
        self.achievements_text = None
        
        # Estado
        self.after_id = None

    def create_main_layout(self) -> None:
        """Crea el layout principal futurístico."""
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.root, bg=self.colors["bg_main"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview,
                                bg=self.colors["bg_card"], troughcolor=self.colors["bg_main"])
        
        self.main_frame = tk.Frame(main_canvas, bg=self.colors["bg_main"])
        self.main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Crear secciones
        self.create_header()
        self.create_progress_section()
        self.create_content_section()
        self.create_options_section()
        self.create_feedback_section()
        self.create_controls_section()

    def create_header(self) -> None:
        """Crea el encabezado futurístico."""
        header_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        header_frame.pack(fill=tk.X, padx=30, pady=20)
        
        # Título principal con efecto futurístico
        title_label = tk.Label(
            header_frame,
            text="🚀 PROYECTO ALPHA - SISTEMA EDUCATIVO FUTURÍSTICO DE IA",
            font=self.fonts["title"],
            bg=self.colors["bg_main"],
            fg=self.colors["accent"],
            relief=tk.FLAT
        )
        title_label.pack()
        
        # Línea decorativa
        line_frame = tk.Frame(header_frame, bg=self.colors["accent"], height=3)
        line_frame.pack(fill=tk.X, pady=10)
        
        # Indicador de modo
        self.mode_indicator = tk.Label(
            header_frame,
            text="📚 MODO: ADAPTATIVO",
            font=self.fonts["caption"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_bright"],
            padx=20,
            pady=8,
            relief=tk.FLAT
        )
        self.mode_indicator.pack()

    def create_progress_section(self) -> None:
        """Crea la sección de progreso futurística."""
        progress_frame = tk.Frame(self.main_frame, bg=self.colors["bg_card"], relief=tk.FLAT, bd=2)
        progress_frame.pack(fill=tk.X, padx=30, pady=15)
        
        # Información de progreso
        self.progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_text_var,
            font=self.fonts["header"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_bright"],
            pady=15
        )
        self.progress_label.pack()
        
        # Temporizador
        self.timer_label = tk.Label(
            progress_frame,
            textvariable=self.timer_text_var,
            font=self.fonts["body_large"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_secondary"],
            pady=5
        )
        self.timer_label.pack()

    def create_content_section(self) -> None:
        """Crea la sección de contenido futurística."""
        content_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        content_frame.pack(fill=tk.X, padx=30, pady=15)
        
        # Título de la misión
        self.mission_title_label = tk.Label(
            content_frame,
            text="",
            font=self.fonts["subheader"],
            bg=self.colors["bg_main"],
            fg=self.colors["success"],
            wraplength=1200,
            justify=tk.LEFT,
            pady=10
        )
        self.mission_title_label.pack(anchor=tk.W)
        
        # Contenido de la historia con diseño futurístico
        story_frame = tk.Frame(content_frame, bg=self.colors["bg_card"], relief=tk.FLAT, bd=3)
        story_frame.pack(fill=tk.X, pady=10)
        
        # Borde superior decorativo
        top_border = tk.Frame(story_frame, bg=self.colors["glow"], height=2)
        top_border.pack(fill=tk.X)
        
        self.story_label = tk.Label(
            story_frame,
            textvariable=self.story_text_var,
            font=self.fonts["body_large"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"],
            wraplength=1200,
            justify=tk.LEFT,
            padx=30,
            pady=25
        )
        self.story_label.pack(fill=tk.X)

    def create_options_section(self) -> None:
        """Crea la sección de opciones futurística."""
        options_container = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        options_container.pack(fill=tk.X, padx=30, pady=15)
        
        # Título de opciones
        options_title = tk.Label(
            options_container,
            text="🎯 SELECCIONA LA RESPUESTA CORRECTA:",
            font=self.fonts["subheader"],
            bg=self.colors["bg_main"],
            fg=self.colors["accent"],
            pady=10
        )
        options_title.pack(anchor=tk.W)
        
        # Frame para las opciones
        self.options_frame = tk.Frame(options_container, bg=self.colors["bg_main"])
        self.options_frame.pack(fill=tk.X)

    def create_feedback_section(self) -> None:
        """Crea la sección de feedback futurística."""
        feedback_frame = tk.Frame(self.main_frame, bg=self.colors["bg_card"], relief=tk.FLAT, bd=3)
        feedback_frame.pack(fill=tk.X, padx=30, pady=15)
        
        # Borde superior decorativo
        top_border = tk.Frame(feedback_frame, bg=self.colors["success"], height=2)
        top_border.pack(fill=tk.X)
        
        # Título de feedback
        feedback_title = tk.Label(
            feedback_frame,
            text="💬 RETROALIMENTACIÓN DEL SISTEMA:",
            font=self.fonts["subheader"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_bright"],
            pady=10
        )
        feedback_title.pack(anchor=tk.W, padx=30)
        
        # Feedback principal
        self.feedback_label = tk.Label(
            feedback_frame,
            textvariable=self.feedback_text_var,
            font=self.fonts["body_large"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"],
            wraplength=1200,
            justify=tk.LEFT,
            padx=30,
            pady=15
        )
        self.feedback_label.pack(fill=tk.X)
        
        # Métricas
        self.metrics_label = tk.Label(
            feedback_frame,
            textvariable=self.metrics_text_var,
            font=self.fonts["caption"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_secondary"],
            padx=30,
            pady=10
        )
        self.metrics_label.pack(fill=tk.X)

    def create_controls_section(self) -> None:
        """Crea la sección de controles futurística."""
        controls_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        controls_frame.pack(fill=tk.X, padx=30, pady=30)
        
        # Contenedor para botones
        button_container = tk.Frame(controls_frame, bg=self.colors["bg_main"])
        button_container.pack()
        
        # Botón principal futurístico
        self.next_button = tk.Button(
            button_container,
            text="🚀 Empezar",
            font=self.fonts["button"],
            bg=self.colors["accent"],
            fg=self.colors["bg_main"],
            width=18,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors["glow"],
            activeforeground=self.colors["bg_main"]
        )
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # Botón de pista
        self.hint_button = tk.Button(
            button_container,
            text="💡 Pista",
            font=self.fonts["button"],
            bg=self.colors["warning"],
            fg=self.colors["bg_main"],
            width=12,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground="#ffb74d",
            activeforeground=self.colors["bg_main"]
        )
        self.hint_button.pack(side=tk.LEFT, padx=10)
        
        # Botón de reintento
        self.retry_button = tk.Button(
            button_container,
            text="🔄 Reintentar",
            font=self.fonts["button"],
            bg=self.colors["text_secondary"],
            fg=self.colors["bg_main"],
            width=12,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground="#90a4ae",
            activeforeground=self.colors["bg_main"]
        )
        self.retry_button.pack(side=tk.LEFT, padx=10)

    def create_side_panel(self) -> None:
        """Crea un panel lateral futurístico."""
        # Panel lateral
        side_frame = tk.Frame(self.root, bg=self.colors["bg_card"], width=280)
        side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        side_frame.pack_propagate(False)
        
        # Título del panel
        panel_title = tk.Label(
            side_frame,
            text="📊 ESTADÍSTICAS DEL SISTEMA",
            font=self.fonts["header"],
            bg=self.colors["bg_card"],
            fg=self.colors["accent"],
            pady=20
        )
        panel_title.pack()
        
        # Línea decorativa
        line = tk.Frame(side_frame, bg=self.colors["glow"], height=2)
        line.pack(fill=tk.X, padx=20)
        
        # Estadísticas
        stats_frame = tk.Frame(side_frame, bg=self.colors["bg_card"])
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        stats = [
            ("Puntuación", "0/21"),
            ("Racha", "0"),
            ("Mejor Racha", "0"),
            ("Pistas Usadas", "0"),
            ("Reintentos", "0"),
            ("Tiempo", "00:00:00")
        ]
        
        self.stats_labels = {}
        for label_text, value in stats:
            stat_frame = tk.Frame(stats_frame, bg=self.colors["bg_option"], relief=tk.FLAT, bd=1)
            stat_frame.pack(fill=tk.X, pady=3)
            
            tk.Label(stat_frame, text=label_text + ":", font=self.fonts["caption"],
                    bg=self.colors["bg_option"], fg=self.colors["text_secondary"],
                    padx=10, pady=5).pack(side=tk.LEFT)
            
            self.stats_labels[label_text] = tk.Label(
                stat_frame, text=value, font=self.fonts["stats"],
                bg=self.colors["bg_option"], fg=self.colors["text_bright"],
                padx=10, pady=5
            )
            self.stats_labels[label_text].pack(side=tk.RIGHT)
        
        # Logros
        achievements_title = tk.Label(
            side_frame,
            text="🏆 LOGROS DESBLOQUEADOS",
            font=self.fonts["subheader"],
            bg=self.colors["bg_card"],
            fg=self.colors["success"],
            pady=15
        )
        achievements_title.pack()
        
        # Línea decorativa
        line2 = tk.Frame(side_frame, bg=self.colors["success"], height=2)
        line2.pack(fill=tk.X, padx=20)
        
        self.achievements_text = tk.Text(
            side_frame,
            height=8,
            width=30,
            font=self.fonts["caption"],
            bg=self.colors["bg_option"],
            fg=self.colors["text_main"],
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=15,
            pady=15,
            insertbackground=self.colors["accent"]
        )
        self.achievements_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        self.achievements_text.insert(tk.END, "🌟 ¡Comienza tu aventura para\ndesbloquear logros increíbles!")
        self.achievements_text.config(state=tk.DISABLED)

    def create_animations_canvas(self) -> None:
        """Placeholder para animaciones."""
        pass

    def setup_animations(self) -> None:
        """Placeholder para animaciones."""
        pass

    def create_menu_bar(self, callbacks: Dict[str, Callable]) -> None:
        """Crea la barra de menú futurística."""
        menubar = tk.Menu(self.root, bg=self.colors["bg_card"], fg=self.colors["text_main"],
                         activebackground=self.colors["accent"], activeforeground=self.colors["bg_main"])
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg_card"], fg=self.colors["text_main"])
        menubar.add_cascade(label="🗂️ Archivo", menu=file_menu)
        file_menu.add_command(label="🆕 Nueva Sesión", command=callbacks.get("new_session"))
        file_menu.add_command(label="💾 Guardar", command=callbacks.get("save_progress"))
        file_menu.add_command(label="📂 Cargar", command=callbacks.get("load_progress"))
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Salir", command=callbacks.get("exit"))
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.colors["bg_card"], fg=self.colors["text_main"])
        menubar.add_cascade(label="❓ Ayuda", menu=help_menu)
        help_menu.add_command(label="📖 Tutorial", command=callbacks.get("show_tutorial"))
        help_menu.add_command(label="ℹ️ Acerca de", command=callbacks.get("show_about"))

    def clear_options(self) -> None:
        """Limpia todas las opciones."""
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def create_option_buttons(self, mission_data: Dict[str, Any], callback: Callable) -> None:
        """Crea botones de opción futurísticos con letras grandes."""
        options = list(mission_data["options"].items())
        
        for i, (choice_key, choice_description) in enumerate(options):
            # Frame para cada opción con diseño futurístico
            option_frame = tk.Frame(
                self.options_frame,
                bg=self.colors["bg_option"],
                relief=tk.FLAT,
                bd=2,
                cursor="hand2"
            )
            option_frame.pack(fill=tk.X, pady=8)
            
            # Borde lateral decorativo
            side_border = tk.Frame(option_frame, bg=self.colors["glow"], width=4)
            side_border.pack(side=tk.LEFT, fill=tk.Y)
            
            # Letra de opción (A, B, C) más grande
            option_letter = chr(65 + i)
            letter_frame = tk.Frame(option_frame, bg=self.colors["accent"], width=60)
            letter_frame.pack(side=tk.LEFT, fill=tk.Y)
            letter_frame.pack_propagate(False)
            
            letter_label = tk.Label(
                letter_frame,
                text=f"{option_letter}",
                font=("Arial", 24, "bold"),
                bg=self.colors["accent"],
                fg=self.colors["bg_main"]
            )
            letter_label.pack(expand=True)
            
            # Contenido de la opción
            content_frame = tk.Frame(option_frame, bg=self.colors["bg_option"])
            content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=15)
            
            # Título de la opción con letra más grande
            title_label = tk.Label(
                content_frame,
                text=choice_key,
                font=self.fonts["body_large"],
                bg=self.colors["bg_option"],
                fg=self.colors["text_bright"],
                wraplength=900,
                justify=tk.LEFT,
                anchor=tk.W
            )
            title_label.pack(fill=tk.X, anchor=tk.W)
            
            # Descripción de la opción con letra más grande
            desc_label = tk.Label(
                content_frame,
                text=choice_description,
                font=self.fonts["body"],
                bg=self.colors["bg_option"],
                fg=self.colors["text_secondary"],
                wraplength=900,
                justify=tk.LEFT,
                anchor=tk.W
            )
            desc_label.pack(fill=tk.X, anchor=tk.W, pady=(8, 0))
            
            # Efectos hover futurísticos
            def on_enter(e, frame=option_frame, border=side_border):
                frame.config(bg=self.colors["bg_selected"])
                border.config(bg=self.colors["success"])
                for child in frame.winfo_children():
                    if isinstance(child, tk.Frame) and child != border and child != letter_frame:
                        child.config(bg=self.colors["bg_selected"])
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.config(bg=self.colors["bg_selected"])
            
            def on_leave(e, frame=option_frame, border=side_border):
                frame.config(bg=self.colors["bg_option"])
                border.config(bg=self.colors["glow"])
                for child in frame.winfo_children():
                    if isinstance(child, tk.Frame) and child != border and child != letter_frame:
                        child.config(bg=self.colors["bg_option"])
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.config(bg=self.colors["bg_option"])
            
            def on_click(e, key=choice_key, frame=option_frame):
                # Efecto de selección
                frame.config(bg=self.colors["success"])
                callback(key, frame)
            
            # Bind eventos
            option_frame.bind("<Enter>", on_enter)
            option_frame.bind("<Leave>", on_leave)
            option_frame.bind("<Button-1>", on_click)
            letter_label.bind("<Enter>", on_enter)
            letter_label.bind("<Leave>", on_leave)
            letter_label.bind("<Button-1>", on_click)
            title_label.bind("<Enter>", on_enter)
            title_label.bind("<Leave>", on_leave)
            title_label.bind("<Button-1>", on_click)
            desc_label.bind("<Enter>", on_enter)
            desc_label.bind("<Leave>", on_leave)
            desc_label.bind("<Button-1>", on_click)

    def update_progress_display(self, score: int, max_score: int) -> None:
        """Actualiza el progreso."""
        pass

    def update_stats_display(self, stats: Dict[str, Any]) -> None:
        """Actualiza las estadísticas."""
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
        """Actualiza los logros."""
        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)
        
        if achievements:
            for achievement in achievements[-5:]:
                self.achievements_text.insert(tk.END, f"⭐ {achievement}\n")
        else:
            self.achievements_text.insert(tk.END, "🌟 ¡Comienza tu aventura para\ndesbloquear logros increíbles!")
        
        self.achievements_text.config(state=tk.DISABLED)

    def type_story_effect(self, full_text: str, callback: callable = None) -> None:
        """Muestra el texto inmediatamente."""
        self.story_text_var.set(full_text)
        if callback:
            callback()

    def show_tutorial(self) -> None:
        """Muestra tutorial futurístico."""
        tutorial_text = """
        🚀 MANUAL DEL COMANDANTE - PROYECTO ALPHA

        🎯 MISIÓN PRINCIPAL:
        Dominar los conceptos de Inteligencia Artificial completando 21 misiones educativas.

        🎮 CONTROLES DEL SISTEMA:
        1. 📖 Lee cada misión con atención
        2. 🎯 Selecciona la respuesta correcta
        3. 💡 Usa pistas si necesitas asistencia
        4. 🔄 Reintenta misiones si es necesario
        5. 📊 Monitorea tu progreso en tiempo real

        🏆 SISTEMA DE RECOMPENSAS:
        • Respuesta correcta: +1 punto
        • Rachas consecutivas: Bonificaciones especiales
        • Logros desbloqueables por rendimiento

        ¡Que la fuerza del conocimiento te acompañe, Comandante! 🌟
        """
        messagebox.showinfo("🚀 Manual del Comandante", tutorial_text)

    def show_about(self) -> None:
        """Muestra información del proyecto."""
        about_text = """
        🚀 PROYECTO ALPHA v4.0
        SISTEMA EDUCATIVO FUTURÍSTICO DE INTELIGENCIA ARTIFICIAL

        🌟 CARACTERÍSTICAS AVANZADAS:
        ✓ Interfaz futurística optimizada para la vista
        ✓ 21 misiones educativas interactivas
        ✓ Sistema de logros y métricas avanzadas
        ✓ Diseño ergonómico con letras grandes
        ✓ Colores amigables para sesiones largas
        ✓ Retroalimentación educativa inmediata

        🎯 OBJETIVO:
        Democratizar el aprendizaje de IA a través de
        una experiencia educativa inmersiva y futurística.

        ¡El futuro del aprendizaje está aquí! 🌟
        """
        messagebox.showinfo("🚀 Acerca del Proyecto Alpha", about_text)

    def show_message(self, title: str, message: str, type: str = "info") -> None:
        """Muestra un mensaje."""
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)