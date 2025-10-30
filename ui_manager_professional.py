"""
UI Manager Profesional - Proyecto Alpha v4.0
Interfaz profesional de calidad comercial para sistema educativo.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional, Callable, List


class UIManager:
    """Gestor de interfaz profesional de calidad comercial."""

    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Configuración profesional de ventana
        self.root.configure(bg='#f8f9fa')
        self.root.geometry("1200x800")
        self.root.title("Proyecto Alpha - Sistema de Aprendizaje de IA")
        self.root.minsize(1000, 700)
        
        # Paleta de colores profesional (inspirada en aplicaciones educativas premium)
        self.colors = {
            "primary": "#2563eb",      # Azul profesional
            "primary_light": "#3b82f6",
            "secondary": "#64748b",    # Gris moderno
            "success": "#10b981",      # Verde éxito
            "warning": "#f59e0b",      # Ámbar advertencia
            "danger": "#ef4444",       # Rojo error
            "bg_main": "#ffffff",      # Blanco puro
            "bg_secondary": "#f8f9fa", # Gris muy claro
            "bg_card": "#ffffff",      # Blanco para tarjetas
            "text_primary": "#1f2937", # Gris oscuro
            "text_secondary": "#6b7280", # Gris medio
            "border": "#e5e7eb",       # Borde sutil
            "shadow": "rgba(0,0,0,0.1)" # Sombra suave
        }
        
        # Tipografía profesional
        self.fonts = {
            "title": ("Segoe UI", 24, "bold"),
            "heading": ("Segoe UI", 18, "bold"),
            "subheading": ("Segoe UI", 16, "bold"),
            "body": ("Segoe UI", 14, "normal"),
            "body_large": ("Segoe UI", 16, "normal"),
            "caption": ("Segoe UI", 12, "normal"),
            "button": ("Segoe UI", 14, "bold")
        }
        
        # Variables
        self.story_text_var = tk.StringVar()
        self.progress_text_var = tk.StringVar()
        self.feedback_text_var = tk.StringVar()
        self.timer_text_var = tk.StringVar()
        self.metrics_text_var = tk.StringVar()
        
        # Componentes
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
        self.after_id = None
        
        # Configurar estilo
        self.setup_styles()

    def setup_styles(self):
        """Configura estilos profesionales."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Botones profesionales
        style.configure("Primary.TButton",
                       background=self.colors["primary"],
                       foreground="white",
                       font=self.fonts["button"],
                       padding=(20, 10))
        
        style.configure("Secondary.TButton",
                       background=self.colors["secondary"],
                       foreground="white",
                       font=self.fonts["button"],
                       padding=(15, 8))

    def create_main_layout(self):
        """Crea layout principal profesional."""
        # Container principal con padding
        main_container = tk.Frame(self.root, bg=self.colors["bg_secondary"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header profesional
        self.create_header(main_container)
        
        # Contenido principal en grid
        content_frame = tk.Frame(main_container, bg=self.colors["bg_secondary"])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Configurar grid
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel principal (izquierda)
        main_panel = self.create_main_panel(content_frame)
        main_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Panel lateral (derecha)
        side_panel = self.create_sidebar(content_frame)
        side_panel.grid(row=0, column=1, sticky="nsew")

    def create_header(self, parent):
        """Crea header profesional."""
        header = tk.Frame(parent, bg=self.colors["bg_main"], relief=tk.FLAT, bd=1)
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Contenido del header con padding
        header_content = tk.Frame(header, bg=self.colors["bg_main"])
        header_content.pack(fill=tk.X, padx=30, pady=20)
        
        # Logo y título
        title_frame = tk.Frame(header_content, bg=self.colors["bg_main"])
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="🧠", font=("Segoe UI", 32), 
                bg=self.colors["bg_main"], fg=self.colors["primary"]).pack(side=tk.LEFT)
        
        title_text = tk.Frame(title_frame, bg=self.colors["bg_main"])
        title_text.pack(side=tk.LEFT, padx=(15, 0))
        
        tk.Label(title_text, text="Proyecto Alpha", font=self.fonts["title"],
                bg=self.colors["bg_main"], fg=self.colors["text_primary"]).pack(anchor=tk.W)
        
        tk.Label(title_text, text="Sistema de Aprendizaje de Inteligencia Artificial", 
                font=self.fonts["caption"], bg=self.colors["bg_main"], 
                fg=self.colors["text_secondary"]).pack(anchor=tk.W)
        
        # Indicador de progreso en header
        progress_frame = tk.Frame(header_content, bg=self.colors["bg_main"])
        progress_frame.pack(side=tk.RIGHT)
        
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_text_var,
                                      font=self.fonts["body"], bg=self.colors["bg_main"],
                                      fg=self.colors["text_primary"])
        self.progress_label.pack()
        
        self.timer_label = tk.Label(progress_frame, textvariable=self.timer_text_var,
                                   font=self.fonts["caption"], bg=self.colors["bg_main"],
                                   fg=self.colors["text_secondary"])
        self.timer_label.pack()

    def create_main_panel(self, parent):
        """Crea panel principal."""
        panel = tk.Frame(parent, bg=self.colors["bg_secondary"])
        
        # Card de misión
        mission_card = self.create_card(panel)
        mission_card.pack(fill=tk.BOTH, expand=True)
        
        # Título de misión
        self.mission_title_label = tk.Label(mission_card, text="", font=self.fonts["heading"],
                                           bg=self.colors["bg_card"], fg=self.colors["text_primary"],
                                           wraplength=700, justify=tk.LEFT)
        self.mission_title_label.pack(anchor=tk.W, padx=30, pady=(30, 15))
        
        # Contenido de la historia
        story_frame = tk.Frame(mission_card, bg=self.colors["bg_secondary"], relief=tk.FLAT, bd=1)
        story_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        self.story_label = tk.Label(story_frame, textvariable=self.story_text_var,
                                   font=self.fonts["body_large"], bg=self.colors["bg_secondary"],
                                   fg=self.colors["text_primary"], wraplength=700, justify=tk.LEFT,
                                   padx=20, pady=20)
        self.story_label.pack(fill=tk.X)
        
        # Opciones
        options_title = tk.Label(mission_card, text="Selecciona tu respuesta:",
                                font=self.fonts["subheading"], bg=self.colors["bg_card"],
                                fg=self.colors["text_primary"])
        options_title.pack(anchor=tk.W, padx=30, pady=(10, 15))
        
        self.options_frame = tk.Frame(mission_card, bg=self.colors["bg_card"])
        self.options_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Feedback
        feedback_card = self.create_card(panel)
        feedback_card.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(feedback_card, text="Retroalimentación", font=self.fonts["subheading"],
                bg=self.colors["bg_card"], fg=self.colors["text_primary"]).pack(anchor=tk.W, padx=30, pady=(20, 10))
        
        self.feedback_label = tk.Label(feedback_card, textvariable=self.feedback_text_var,
                                      font=self.fonts["body"], bg=self.colors["bg_card"],
                                      fg=self.colors["text_primary"], wraplength=700, justify=tk.LEFT)
        self.feedback_label.pack(anchor=tk.W, padx=30, pady=(0, 10))
        
        self.metrics_label = tk.Label(feedback_card, textvariable=self.metrics_text_var,
                                     font=self.fonts["caption"], bg=self.colors["bg_card"],
                                     fg=self.colors["text_secondary"])
        self.metrics_label.pack(anchor=tk.W, padx=30, pady=(0, 20))
        
        # Controles
        controls = tk.Frame(feedback_card, bg=self.colors["bg_card"])
        controls.pack(anchor=tk.W, padx=30, pady=(0, 30))
        
        self.next_button = tk.Button(controls, text="Comenzar", font=self.fonts["button"],
                                    bg=self.colors["primary"], fg="white", relief=tk.FLAT,
                                    padx=25, pady=12, cursor="hand2")
        self.next_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.hint_button = tk.Button(controls, text="💡 Pista", font=self.fonts["button"],
                                    bg=self.colors["warning"], fg="white", relief=tk.FLAT,
                                    padx=20, pady=12, cursor="hand2", state=tk.DISABLED)
        self.hint_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.retry_button = tk.Button(controls, text="🔄 Reintentar", font=self.fonts["button"],
                                     bg=self.colors["secondary"], fg="white", relief=tk.FLAT,
                                     padx=20, pady=12, cursor="hand2", state=tk.DISABLED)
        self.retry_button.pack(side=tk.LEFT)
        
        return panel

    def create_sidebar(self, parent):
        """Crea sidebar profesional."""
        sidebar = tk.Frame(parent, bg=self.colors["bg_secondary"])
        
        # Card de estadísticas
        stats_card = self.create_card(sidebar)
        stats_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(stats_card, text="📊 Estadísticas", font=self.fonts["subheading"],
                bg=self.colors["bg_card"], fg=self.colors["text_primary"]).pack(padx=20, pady=(20, 15))
        
        # Stats
        stats_data = [
            ("Puntuación", "0/21"),
            ("Racha actual", "0"),
            ("Mejor racha", "0"),
            ("Pistas usadas", "0"),
            ("Reintentos", "0"),
            ("Tiempo", "00:00:00")
        ]
        
        self.stats_labels = {}
        for label, value in stats_data:
            stat_row = tk.Frame(stats_card, bg=self.colors["bg_card"])
            stat_row.pack(fill=tk.X, padx=20, pady=2)
            
            tk.Label(stat_row, text=label, font=self.fonts["caption"],
                    bg=self.colors["bg_card"], fg=self.colors["text_secondary"]).pack(side=tk.LEFT)
            
            self.stats_labels[label] = tk.Label(stat_row, text=value, font=self.fonts["body"],
                                               bg=self.colors["bg_card"], fg=self.colors["text_primary"])
            self.stats_labels[label].pack(side=tk.RIGHT)
        
        # Espacio
        tk.Frame(stats_card, bg=self.colors["bg_card"], height=20).pack()
        
        # Card de logros
        achievements_card = self.create_card(sidebar)
        achievements_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(achievements_card, text="🏆 Logros", font=self.fonts["subheading"],
                bg=self.colors["bg_card"], fg=self.colors["text_primary"]).pack(padx=20, pady=(20, 15))
        
        self.achievements_text = tk.Text(achievements_card, height=10, font=self.fonts["caption"],
                                        bg=self.colors["bg_secondary"], fg=self.colors["text_primary"],
                                        relief=tk.FLAT, wrap=tk.WORD, padx=10, pady=10)
        self.achievements_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.achievements_text.insert(tk.END, "Completa misiones para desbloquear logros")
        self.achievements_text.config(state=tk.DISABLED)
        
        return sidebar

    def create_card(self, parent):
        """Crea una tarjeta profesional con sombra."""
        card = tk.Frame(parent, bg=self.colors["bg_card"], relief=tk.FLAT, bd=1)
        return card

    def create_side_panel(self):
        """Método requerido por compatibilidad."""
        pass

    def create_animations_canvas(self):
        """Método requerido por compatibilidad."""
        pass

    def setup_animations(self):
        """Método requerido por compatibilidad."""
        pass

    def create_menu_bar(self, callbacks: Dict[str, Callable]):
        """Crea menú profesional."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva sesión", command=callbacks.get("new_session"))
        file_menu.add_command(label="Guardar progreso", command=callbacks.get("save_progress"))
        file_menu.add_command(label="Cargar progreso", command=callbacks.get("load_progress"))
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=callbacks.get("exit"))
        
        # Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Tutorial", command=callbacks.get("show_tutorial"))
        help_menu.add_command(label="Acerca de", command=callbacks.get("show_about"))

    def clear_options(self):
        """Limpia opciones."""
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def create_option_buttons(self, mission_data: Dict[str, Any], callback: Callable):
        """Crea opciones profesionales."""
        options = list(mission_data["options"].items())
        
        for i, (choice_key, choice_description) in enumerate(options):
            # Container de opción
            option_container = tk.Frame(self.options_frame, bg=self.colors["bg_card"])
            option_container.pack(fill=tk.X, pady=5)
            
            # Botón de opción profesional
            option_btn = tk.Button(option_container, text=f"{chr(65+i)}", font=("Segoe UI", 16, "bold"),
                                  bg=self.colors["primary"], fg="white", width=3, height=1,
                                  relief=tk.FLAT, cursor="hand2")
            option_btn.pack(side=tk.LEFT, padx=(0, 15))
            
            # Contenido
            content_frame = tk.Frame(option_container, bg=self.colors["bg_card"])
            content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            title_label = tk.Label(content_frame, text=choice_key, font=self.fonts["body"],
                                  bg=self.colors["bg_card"], fg=self.colors["text_primary"],
                                  wraplength=500, justify=tk.LEFT, anchor=tk.W)
            title_label.pack(fill=tk.X)
            
            desc_label = tk.Label(content_frame, text=choice_description, font=self.fonts["caption"],
                                 bg=self.colors["bg_card"], fg=self.colors["text_secondary"],
                                 wraplength=500, justify=tk.LEFT, anchor=tk.W)
            desc_label.pack(fill=tk.X, pady=(5, 0))
            
            # Hover effects
            def on_enter(e, btn=option_btn, container=option_container):
                btn.config(bg=self.colors["primary_light"])
                container.config(bg=self.colors["bg_secondary"])
            
            def on_leave(e, btn=option_btn, container=option_container):
                btn.config(bg=self.colors["primary"])
                container.config(bg=self.colors["bg_card"])
            
            def on_click(e, key=choice_key, container=option_container):
                container.config(bg=self.colors["success"])
                callback(key, container)
            
            # Bind events
            for widget in [option_btn, option_container, title_label, desc_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
                widget.bind("<Button-1>", on_click)

    def update_progress_display(self, score: int, max_score: int):
        """Actualiza progreso."""
        pass

    def update_stats_display(self, stats: Dict[str, Any]):
        """Actualiza estadísticas."""
        mappings = {
            "Puntuación": f"{stats.get('score', 0)}/{stats.get('max_score', 21)}",
            "Racha actual": str(stats.get('streak', 0)),
            "Mejor racha": str(stats.get('best_streak', 0)),
            "Pistas usadas": str(stats.get('hints_used', 0)),
            "Reintentos": str(stats.get('retries', 0)),
            "Tiempo": stats.get('time_formatted', '00:00:00')
        }
        
        for label, value in mappings.items():
            if label in self.stats_labels:
                self.stats_labels[label].config(text=value)

    def update_achievements_display(self, achievements: List[str]):
        """Actualiza logros."""
        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)
        
        if achievements:
            for achievement in achievements[-5:]:
                self.achievements_text.insert(tk.END, f"🏆 {achievement}\n")
        else:
            self.achievements_text.insert(tk.END, "Completa misiones para desbloquear logros")
        
        self.achievements_text.config(state=tk.DISABLED)

    def type_story_effect(self, full_text: str, callback: callable = None):
        """Muestra texto inmediatamente."""
        self.story_text_var.set(full_text)
        if callback:
            callback()

    def show_tutorial(self):
        """Tutorial profesional."""
        tutorial_text = """
        GUÍA DE USUARIO - PROYECTO ALPHA

        OBJETIVO:
        Dominar conceptos fundamentales de Inteligencia Artificial 
        a través de 21 misiones educativas interactivas.

        INSTRUCCIONES:
        1. Lee cada misión cuidadosamente
        2. Selecciona la respuesta correcta
        3. Recibe retroalimentación detallada
        4. Usa pistas cuando sea necesario
        5. Monitorea tu progreso en tiempo real

        SISTEMA DE PUNTUACIÓN:
        • Respuesta correcta: +1 punto
        • Rachas consecutivas: Bonificaciones
        • Uso de pistas: Penalización mínima

        ¡Disfruta tu experiencia de aprendizaje!
        """
        messagebox.showinfo("Tutorial", tutorial_text)

    def show_about(self):
        """Información del producto."""
        about_text = """
        PROYECTO ALPHA v4.0
        Sistema de Aprendizaje de Inteligencia Artificial

        CARACTERÍSTICAS:
        ✓ 21 misiones educativas interactivas
        ✓ Sistema de métricas avanzado
        ✓ Interfaz profesional y moderna
        ✓ Retroalimentación educativa inmediata
        ✓ Sistema de logros y gamificación

        Desarrollado con estándares de calidad comercial
        para proporcionar la mejor experiencia educativa.
        """
        messagebox.showinfo("Acerca de Proyecto Alpha", about_text)

    def show_message(self, title: str, message: str, type: str = "info"):
        """Muestra mensaje."""
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)