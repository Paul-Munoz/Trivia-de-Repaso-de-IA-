"""
UI Manager Simple - Proyecto Alpha v4.0
Interfaz de usuario simplificada y clara para mejor visualización.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Dict, Any, Optional, Callable, List
import time
from datetime import datetime

from config import COLORS, UI_CONFIG, PROFESSIONAL_CONFIG


class UIManager:
    """
    Gestor simplificado de la interfaz de usuario.
    
    Enfocado en claridad y legibilidad de los conceptos educativos.
    """

    def __init__(self, root: tk.Tk):
        """Inicializa el gestor de UI simplificado."""
        self.root = root
        
        # Configurar ventana principal
        self.root.configure(bg='white')
        self.root.geometry("1200x800")
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
        
        # Configurar estilos
        self.setup_styles()

    def setup_styles(self) -> None:
        """Configura estilos simples y claros."""
        self.fonts = {
            "title": ("Arial", 24, "bold"),
            "header": ("Arial", 18, "bold"),
            "subheader": ("Arial", 16, "bold"),
            "body": ("Arial", 14, "normal"),
            "caption": ("Arial", 12, "normal"),
            "small": ("Arial", 10, "normal"),
            "button": ("Arial", 12, "bold"),
        }
        
        self.colors = {
            "bg_main": "#FFFFFF",
            "bg_card": "#F8F9FA",
            "bg_option": "#E3F2FD",
            "bg_correct": "#C8E6C9",
            "bg_incorrect": "#FFCDD2",
            "text_main": "#212529",
            "text_secondary": "#6C757D",
            "accent": "#2196F3",
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800"
        }

    def create_main_layout(self) -> None:
        """Crea el layout principal simplificado."""
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.root, bg=self.colors["bg_main"])
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        
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
        """Crea el encabezado simple."""
        header_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="🧠 PROYECTO ALPHA - SISTEMA EDUCATIVO DE IA",
            font=self.fonts["title"],
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"]
        )
        title_label.pack()
        
        # Indicador de modo
        self.mode_indicator = tk.Label(
            header_frame,
            text="📚 MODO: ADAPTATIVO",
            font=self.fonts["caption"],
            bg=self.colors["accent"],
            fg="white",
            padx=10,
            pady=5
        )
        self.mode_indicator.pack(pady=(10, 0))

    def create_progress_section(self) -> None:
        """Crea la sección de progreso clara."""
        progress_frame = tk.Frame(self.main_frame, bg=self.colors["bg_card"])
        progress_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Información de progreso
        self.progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_text_var,
            font=self.fonts["header"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"]
        )
        self.progress_label.pack()
        
        # Temporizador
        self.timer_label = tk.Label(
            progress_frame,
            textvariable=self.timer_text_var,
            font=self.fonts["body"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_secondary"]
        )
        self.timer_label.pack(pady=(5, 0))
        
        # Barra de progreso visual simple
        progress_bar_frame = tk.Frame(progress_frame, bg=self.colors["bg_card"])
        progress_bar_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress_bar_bg = tk.Frame(progress_bar_frame, bg="#E0E0E0", height=10)
        self.progress_bar_bg.pack(fill=tk.X)
        
        self.progress_bar = tk.Frame(self.progress_bar_bg, bg=self.colors["accent"], height=10)
        self.progress_bar.pack(side=tk.LEFT)

    def create_content_section(self) -> None:
        """Crea la sección de contenido educativo clara."""
        content_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        content_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Título de la misión
        self.mission_title_label = tk.Label(
            content_frame,
            text="",
            font=self.fonts["subheader"],
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"],
            wraplength=1000,
            justify=tk.LEFT
        )
        self.mission_title_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Contenido de la historia - MUY VISIBLE
        story_frame = tk.Frame(content_frame, bg=self.colors["bg_card"], relief=tk.RAISED, bd=2)
        story_frame.pack(fill=tk.X, pady=10)
        
        self.story_label = tk.Label(
            story_frame,
            textvariable=self.story_text_var,
            font=self.fonts["body"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"],
            wraplength=1000,
            justify=tk.LEFT,
            padx=20,
            pady=20
        )
        self.story_label.pack(fill=tk.X)

    def create_options_section(self) -> None:
        """Crea la sección de opciones muy clara."""
        options_container = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        options_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Título de opciones
        options_title = tk.Label(
            options_container,
            text="🎯 SELECCIONA LA RESPUESTA CORRECTA:",
            font=self.fonts["subheader"],
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"]
        )
        options_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Frame para las opciones
        self.options_frame = tk.Frame(options_container, bg=self.colors["bg_main"])
        self.options_frame.pack(fill=tk.X)

    def create_feedback_section(self) -> None:
        """Crea la sección de feedback clara."""
        feedback_frame = tk.Frame(self.main_frame, bg=self.colors["bg_card"], relief=tk.RAISED, bd=2)
        feedback_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Título de feedback
        feedback_title = tk.Label(
            feedback_frame,
            text="💬 RETROALIMENTACIÓN:",
            font=self.fonts["subheader"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"]
        )
        feedback_title.pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        # Feedback principal
        self.feedback_label = tk.Label(
            feedback_frame,
            textvariable=self.feedback_text_var,
            font=self.fonts["body"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"],
            wraplength=1000,
            justify=tk.LEFT,
            padx=20,
            pady=(0, 15)
        )
        self.feedback_label.pack(fill=tk.X)
        
        # Métricas
        self.metrics_label = tk.Label(
            feedback_frame,
            textvariable=self.metrics_text_var,
            font=self.fonts["caption"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_secondary"],
            padx=20,
            pady=(0, 15)
        )
        self.metrics_label.pack(fill=tk.X)

    def create_controls_section(self) -> None:
        """Crea la sección de controles clara."""
        controls_frame = tk.Frame(self.main_frame, bg=self.colors["bg_main"])
        controls_frame.pack(fill=tk.X, padx=20, pady=(0, 30))
        
        # Contenedor centrado para botones
        button_container = tk.Frame(controls_frame, bg=self.colors["bg_main"])
        button_container.pack()
        
        # Botón principal
        self.next_button = tk.Button(
            button_container,
            text="🚀 Empezar",
            font=self.fonts["button"],
            bg=self.colors["accent"],
            fg="white",
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # Botón de pista
        self.hint_button = tk.Button(
            button_container,
            text="💡 Pista",
            font=self.fonts["button"],
            bg=self.colors["warning"],
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.hint_button.pack(side=tk.LEFT, padx=10)
        
        # Botón de reintento
        self.retry_button = tk.Button(
            button_container,
            text="🔄 Reintentar",
            font=self.fonts["button"],
            bg=self.colors["text_secondary"],
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.retry_button.pack(side=tk.LEFT, padx=10)

    def create_side_panel(self) -> None:
        """Crea un panel lateral simple con estadísticas."""
        # Panel lateral
        side_frame = tk.Frame(self.root, bg=self.colors["bg_card"], width=250)
        side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        side_frame.pack_propagate(False)
        
        # Título del panel
        panel_title = tk.Label(
            side_frame,
            text="📊 ESTADÍSTICAS",
            font=self.fonts["header"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"]
        )
        panel_title.pack(pady=20)
        
        # Estadísticas
        stats_frame = tk.Frame(side_frame, bg=self.colors["bg_card"])
        stats_frame.pack(fill=tk.X, padx=20)
        
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
            stat_frame = tk.Frame(stats_frame, bg=self.colors["bg_main"])
            stat_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(stat_frame, text=label_text + ":", font=self.fonts["caption"],
                    bg=self.colors["bg_main"], fg=self.colors["text_secondary"]).pack(side=tk.LEFT)
            
            self.stats_labels[label_text] = tk.Label(
                stat_frame, text=value, font=self.fonts["body"],
                bg=self.colors["bg_main"], fg=self.colors["text_main"]
            )
            self.stats_labels[label_text].pack(side=tk.RIGHT)
        
        # Logros
        achievements_title = tk.Label(
            side_frame,
            text="🏆 LOGROS",
            font=self.fonts["subheader"],
            bg=self.colors["bg_card"],
            fg=self.colors["text_main"]
        )
        achievements_title.pack(pady=(30, 10))
        
        self.achievements_text = tk.Text(
            side_frame,
            height=8,
            width=25,
            font=self.fonts["small"],
            bg=self.colors["bg_main"],
            fg=self.colors["text_main"],
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.achievements_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.achievements_text.insert(tk.END, "¡Comienza a jugar para\ndesbloquear logros!")
        self.achievements_text.config(state=tk.DISABLED)

    def create_animations_canvas(self) -> None:
        """Crea canvas para animaciones (simplificado)."""
        pass  # No necesario en versión simplificada

    def setup_animations(self) -> None:
        """Configura animaciones (simplificado)."""
        pass  # No necesario en versión simplificada

    def create_menu_bar(self, callbacks: Dict[str, Callable]) -> None:
        """Crea la barra de menú simplificada."""
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
        
        # Menú Modo
        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modo", menu=mode_menu)
        mode_menu.add_command(label="Adaptativo", command=lambda: callbacks.get("set_mode")("adaptive"))
        mode_menu.add_command(label="Quiz", command=lambda: callbacks.get("set_mode")("quiz"))
        mode_menu.add_command(label="Estudio", command=lambda: callbacks.get("set_mode")("study"))
        
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
        """Crea botones de opción muy claros y visibles."""
        options = list(mission_data["options"].items())
        
        for i, (choice_key, choice_description) in enumerate(options):
            # Frame para cada opción
            option_frame = tk.Frame(
                self.options_frame,
                bg=self.colors["bg_option"],
                relief=tk.RAISED,
                bd=2,
                padx=15,
                pady=15,
                cursor="hand2"
            )
            option_frame.pack(fill=tk.X, pady=5)
            
            # Letra de opción (A, B, C)
            option_letter = chr(65 + i)
            letter_label = tk.Label(
                option_frame,
                text=f"{option_letter})",
                font=self.fonts["subheader"],
                bg=self.colors["bg_option"],
                fg=self.colors["accent"],
                width=3
            )
            letter_label.pack(side=tk.LEFT, anchor=tk.N)
            
            # Contenido de la opción
            content_frame = tk.Frame(option_frame, bg=self.colors["bg_option"])
            content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            
            # Título de la opción
            title_label = tk.Label(
                content_frame,
                text=choice_key,
                font=self.fonts["body"],
                bg=self.colors["bg_option"],
                fg=self.colors["text_main"],
                wraplength=800,
                justify=tk.LEFT,
                anchor=tk.W
            )
            title_label.pack(fill=tk.X, anchor=tk.W)
            
            # Descripción de la opción
            desc_label = tk.Label(
                content_frame,
                text=choice_description,
                font=self.fonts["caption"],
                bg=self.colors["bg_option"],
                fg=self.colors["text_secondary"],
                wraplength=800,
                justify=tk.LEFT,
                anchor=tk.W
            )
            desc_label.pack(fill=tk.X, anchor=tk.W, pady=(5, 0))
            
            # Efectos hover
            def on_enter(e, frame=option_frame):
                frame.config(bg="#BBDEFB")
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg="#BBDEFB")
                    elif isinstance(child, tk.Frame):
                        child.config(bg="#BBDEFB")
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.config(bg="#BBDEFB")
            
            def on_leave(e, frame=option_frame):
                frame.config(bg=self.colors["bg_option"])
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=self.colors["bg_option"])
                    elif isinstance(child, tk.Frame):
                        child.config(bg=self.colors["bg_option"])
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.config(bg=self.colors["bg_option"])
            
            def on_click(e, key=choice_key, frame=option_frame):
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
        """Actualiza la barra de progreso visual."""
        if max_score > 0:
            percentage = score / max_score
            # Calcular ancho de la barra (asumiendo 800px de ancho disponible)
            bar_width = int(percentage * 800)
            self.progress_bar.config(width=bar_width)

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
            for achievement in achievements[-5:]:  # Mostrar últimos 5
                self.achievements_text.insert(tk.END, achievement + "\n")
        else:
            self.achievements_text.insert(tk.END, "¡Comienza a jugar para\ndesbloquear logros!")
        
        self.achievements_text.config(state=tk.DISABLED)

    def type_story_effect(self, full_text: str, callback: callable = None) -> None:
        """Efecto de escritura simplificado (más rápido)."""
        # En lugar del efecto lento, mostrar el texto inmediatamente para mejor UX
        self.story_text_var.set(full_text)
        if callback:
            callback()

    def show_tutorial(self) -> None:
        """Muestra tutorial simplificado."""
        tutorial_text = """
        🎯 CÓMO JUGAR - PROYECTO ALPHA

        OBJETIVO:
        Aprender conceptos de Inteligencia Artificial completando misiones educativas.

        INSTRUCCIONES:
        1. Lee cada misión cuidadosamente
        2. Selecciona la respuesta que crees correcta
        3. Recibe retroalimentación inmediata
        4. Usa pistas si necesitas ayuda
        5. Reintenta si fallas

        PUNTUACIÓN:
        • Respuesta correcta: +1 punto
        • Mantén rachas para mejores resultados
        • Las pistas y reintentos tienen pequeñas penalizaciones

        ¡Disfruta aprendiendo sobre IA!
        """
        messagebox.showinfo("Tutorial", tutorial_text)

    def show_about(self) -> None:
        """Muestra información sobre el proyecto."""
        about_text = """
        PROYECTO ALPHA v4.0
        Sistema Educativo de Inteligencia Artificial

        Un juego educativo interactivo diseñado para enseñar
        conceptos fundamentales de IA de manera divertida y efectiva.

        Características:
        ✓ 21 misiones educativas
        ✓ Sistema de logros
        ✓ Métricas de aprendizaje
        ✓ Interfaz clara y accesible
        ✓ Retroalimentación inmediata

        ¡Aprende IA jugando!
        """
        messagebox.showinfo("Acerca de Proyecto Alpha", about_text)

    def show_message(self, title: str, message: str, type: str = "info") -> None:
        """Muestra un mensaje al usuario."""
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)