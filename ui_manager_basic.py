"""
UI Manager Básico - Proyecto Alpha v4.0
Interfaz de usuario básica y funcional.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from typing import Dict, Any, Optional, Callable, List


class UIManager:
    """Gestor básico de la interfaz de usuario."""

    def __init__(self, root: tk.Tk):
        """Inicializa el gestor de UI básico."""
        self.root = root
        
        # Configurar ventana principal
        self.root.configure(bg='white')
        self.root.geometry("1000x700")
        self.root.title("Proyecto Alpha - Sistema Educativo de IA")
        
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
        """Crea el layout principal básico."""
        # Frame principal simple
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear secciones
        self.create_header()
        self.create_progress_section()
        self.create_content_section()
        self.create_options_section()
        self.create_feedback_section()
        self.create_controls_section()

    def create_header(self) -> None:
        """Crea el encabezado."""
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X)
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="🧠 PROYECTO ALPHA - SISTEMA EDUCATIVO DE IA",
            font=("Arial", 20, "bold"),
            bg='white',
            fg='black'
        )
        title_label.pack()
        
        # Indicador de modo
        self.mode_indicator = tk.Label(
            header_frame,
            text="📚 MODO: ADAPTATIVO",
            font=("Arial", 12),
            bg='lightblue',
            fg='black'
        )
        self.mode_indicator.pack()

    def create_progress_section(self) -> None:
        """Crea la sección de progreso."""
        progress_frame = tk.Frame(self.main_frame, bg='lightgray')
        progress_frame.pack(fill=tk.X)
        
        # Información de progreso
        self.progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_text_var,
            font=("Arial", 14, "bold"),
            bg='lightgray',
            fg='black'
        )
        self.progress_label.pack()
        
        # Temporizador
        self.timer_label = tk.Label(
            progress_frame,
            textvariable=self.timer_text_var,
            font=("Arial", 12),
            bg='lightgray',
            fg='black'
        )
        self.timer_label.pack()

    def create_content_section(self) -> None:
        """Crea la sección de contenido."""
        content_frame = tk.Frame(self.main_frame, bg='white')
        content_frame.pack(fill=tk.X)
        
        # Título de la misión
        self.mission_title_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg='white',
            fg='black',
            wraplength=800,
            justify=tk.LEFT
        )
        self.mission_title_label.pack(anchor=tk.W)
        
        # Contenido de la historia
        story_frame = tk.Frame(content_frame, bg='lightyellow', relief=tk.RAISED, bd=2)
        story_frame.pack(fill=tk.X)
        
        self.story_label = tk.Label(
            story_frame,
            textvariable=self.story_text_var,
            font=("Arial", 12),
            bg='lightyellow',
            fg='black',
            wraplength=800,
            justify=tk.LEFT
        )
        self.story_label.pack()

    def create_options_section(self) -> None:
        """Crea la sección de opciones."""
        options_container = tk.Frame(self.main_frame, bg='white')
        options_container.pack(fill=tk.X)
        
        # Título de opciones
        options_title = tk.Label(
            options_container,
            text="🎯 SELECCIONA LA RESPUESTA CORRECTA:",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='black'
        )
        options_title.pack(anchor=tk.W)
        
        # Frame para las opciones
        self.options_frame = tk.Frame(options_container, bg='white')
        self.options_frame.pack(fill=tk.X)

    def create_feedback_section(self) -> None:
        """Crea la sección de feedback."""
        feedback_frame = tk.Frame(self.main_frame, bg='lightgreen', relief=tk.RAISED, bd=2)
        feedback_frame.pack(fill=tk.X)
        
        # Título de feedback
        feedback_title = tk.Label(
            feedback_frame,
            text="💬 RETROALIMENTACIÓN:",
            font=("Arial", 14, "bold"),
            bg='lightgreen',
            fg='black'
        )
        feedback_title.pack(anchor=tk.W)
        
        # Feedback principal
        self.feedback_label = tk.Label(
            feedback_frame,
            textvariable=self.feedback_text_var,
            font=("Arial", 12),
            bg='lightgreen',
            fg='black',
            wraplength=800,
            justify=tk.LEFT
        )
        self.feedback_label.pack(fill=tk.X)
        
        # Métricas
        self.metrics_label = tk.Label(
            feedback_frame,
            textvariable=self.metrics_text_var,
            font=("Arial", 10),
            bg='lightgreen',
            fg='darkgreen'
        )
        self.metrics_label.pack(fill=tk.X)

    def create_controls_section(self) -> None:
        """Crea la sección de controles."""
        controls_frame = tk.Frame(self.main_frame, bg='white')
        controls_frame.pack(fill=tk.X)
        
        # Contenedor para botones
        button_container = tk.Frame(controls_frame, bg='white')
        button_container.pack()
        
        # Botón principal
        self.next_button = tk.Button(
            button_container,
            text="🚀 Empezar",
            font=("Arial", 12, "bold"),
            bg='blue',
            fg='white',
            width=15,
            height=2
        )
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Botón de pista
        self.hint_button = tk.Button(
            button_container,
            text="💡 Pista",
            font=("Arial", 12, "bold"),
            bg='orange',
            fg='white',
            width=10,
            height=2,
            state=tk.DISABLED
        )
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        # Botón de reintento
        self.retry_button = tk.Button(
            button_container,
            text="🔄 Reintentar",
            font=("Arial", 12, "bold"),
            bg='gray',
            fg='white',
            width=10,
            height=2,
            state=tk.DISABLED
        )
        self.retry_button.pack(side=tk.LEFT, padx=5)

    def create_side_panel(self) -> None:
        """Crea un panel lateral básico."""
        # Panel lateral
        side_frame = tk.Frame(self.root, bg='lightgray', width=200)
        side_frame.pack(side=tk.RIGHT, fill=tk.Y)
        side_frame.pack_propagate(False)
        
        # Título del panel
        panel_title = tk.Label(
            side_frame,
            text="📊 ESTADÍSTICAS",
            font=("Arial", 14, "bold"),
            bg='lightgray',
            fg='black'
        )
        panel_title.pack()
        
        # Estadísticas
        stats_frame = tk.Frame(side_frame, bg='lightgray')
        stats_frame.pack(fill=tk.X)
        
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
            stat_frame = tk.Frame(stats_frame, bg='white')
            stat_frame.pack(fill=tk.X)
            
            tk.Label(stat_frame, text=label_text + ":", font=("Arial", 10),
                    bg='white', fg='black').pack(side=tk.LEFT)
            
            self.stats_labels[label_text] = tk.Label(
                stat_frame, text=value, font=("Arial", 10, "bold"),
                bg='white', fg='black'
            )
            self.stats_labels[label_text].pack(side=tk.RIGHT)
        
        # Logros
        achievements_title = tk.Label(
            side_frame,
            text="🏆 LOGROS",
            font=("Arial", 12, "bold"),
            bg='lightgray',
            fg='black'
        )
        achievements_title.pack()
        
        self.achievements_text = tk.Text(
            side_frame,
            height=8,
            width=25,
            font=("Arial", 9),
            bg='white',
            fg='black',
            wrap=tk.WORD
        )
        self.achievements_text.pack(fill=tk.BOTH, expand=True)
        self.achievements_text.insert(tk.END, "¡Comienza a jugar para\ndesbloquear logros!")
        self.achievements_text.config(state=tk.DISABLED)

    def create_animations_canvas(self) -> None:
        """Placeholder para animaciones."""
        pass

    def setup_animations(self) -> None:
        """Placeholder para animaciones."""
        pass

    def create_menu_bar(self, callbacks: Dict[str, Callable]) -> None:
        """Crea la barra de menú básica."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva Sesión", command=callbacks.get("new_session"))
        file_menu.add_command(label="Guardar", command=callbacks.get("save_progress"))
        file_menu.add_command(label="Cargar", command=callbacks.get("load_progress"))
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=callbacks.get("exit"))
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Tutorial", command=callbacks.get("show_tutorial"))
        help_menu.add_command(label="Acerca de", command=callbacks.get("show_about"))

    def clear_options(self) -> None:
        """Limpia todas las opciones."""
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def create_option_buttons(self, mission_data: Dict[str, Any], callback: Callable) -> None:
        """Crea botones de opción básicos pero claros."""
        options = list(mission_data["options"].items())
        
        for i, (choice_key, choice_description) in enumerate(options):
            # Frame para cada opción
            option_frame = tk.Frame(
                self.options_frame,
                bg='lightblue',
                relief=tk.RAISED,
                bd=2
            )
            option_frame.pack(fill=tk.X, pady=2)
            
            # Letra de opción (A, B, C)
            option_letter = chr(65 + i)
            letter_label = tk.Label(
                option_frame,
                text=f"{option_letter})",
                font=("Arial", 12, "bold"),
                bg='lightblue',
                fg='darkblue',
                width=3
            )
            letter_label.pack(side=tk.LEFT)
            
            # Contenido de la opción
            content_frame = tk.Frame(option_frame, bg='lightblue')
            content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Título de la opción
            title_label = tk.Label(
                content_frame,
                text=choice_key,
                font=("Arial", 11, "bold"),
                bg='lightblue',
                fg='black',
                wraplength=600,
                justify=tk.LEFT,
                anchor=tk.W
            )
            title_label.pack(fill=tk.X, anchor=tk.W)
            
            # Descripción de la opción
            desc_label = tk.Label(
                content_frame,
                text=choice_description,
                font=("Arial", 10),
                bg='lightblue',
                fg='darkblue',
                wraplength=600,
                justify=tk.LEFT,
                anchor=tk.W
            )
            desc_label.pack(fill=tk.X, anchor=tk.W)
            
            # Evento de clic
            def on_click(e, key=choice_key, frame=option_frame):
                # Cambiar color para mostrar selección
                frame.config(bg='yellow')
                callback(key, frame)
            
            # Bind eventos
            option_frame.bind("<Button-1>", on_click)
            letter_label.bind("<Button-1>", on_click)
            title_label.bind("<Button-1>", on_click)
            desc_label.bind("<Button-1>", on_click)

    def update_progress_display(self, score: int, max_score: int) -> None:
        """Actualiza el progreso."""
        pass  # Básico, no necesita barra visual

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
                self.achievements_text.insert(tk.END, achievement + "\n")
        else:
            self.achievements_text.insert(tk.END, "¡Comienza a jugar para\ndesbloquear logros!")
        
        self.achievements_text.config(state=tk.DISABLED)

    def type_story_effect(self, full_text: str, callback: callable = None) -> None:
        """Muestra el texto inmediatamente."""
        self.story_text_var.set(full_text)
        if callback:
            callback()

    def show_tutorial(self) -> None:
        """Muestra tutorial."""
        tutorial_text = """
        🎯 CÓMO JUGAR - PROYECTO ALPHA

        OBJETIVO:
        Aprender conceptos de Inteligencia Artificial completando misiones.

        INSTRUCCIONES:
        1. Lee cada misión cuidadosamente
        2. Selecciona la respuesta correcta
        3. Recibe retroalimentación
        4. Usa pistas si necesitas ayuda
        5. Reintenta si fallas

        ¡Disfruta aprendiendo sobre IA!
        """
        messagebox.showinfo("Tutorial", tutorial_text)

    def show_about(self) -> None:
        """Muestra información del proyecto."""
        about_text = """
        PROYECTO ALPHA v4.0
        Sistema Educativo de Inteligencia Artificial

        Un juego educativo para aprender IA de manera divertida.

        ¡Aprende IA jugando!
        """
        messagebox.showinfo("Acerca de", about_text)

    def show_message(self, title: str, message: str, type: str = "info") -> None:
        """Muestra un mensaje."""
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)