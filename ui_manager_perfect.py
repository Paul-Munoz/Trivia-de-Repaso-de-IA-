"""
UI Manager Perfecto - Proyecto Alpha v4.0
Interfaz perfectamente ajustada y profesional.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Callable, List


class UIManager:
    """Gestor de interfaz perfectamente ajustada."""

    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Configuración perfecta de ventana
        self.root.configure(bg='#f5f5f5')
        self.root.geometry("1400x900")
        self.root.title("Proyecto Alpha - Sistema de Aprendizaje de IA")
        self.root.state('zoomed' if hasattr(self.root, 'state') else 'normal')
        
        # Colores perfectos
        self.colors = {
            "primary": "#4a90e2",
            "success": "#7ed321", 
            "warning": "#f5a623",
            "danger": "#d0021b",
            "dark": "#2c3e50",
            "light": "#ecf0f1",
            "white": "#ffffff",
            "gray": "#95a5a6",
            "text": "#2c3e50"
        }
        
        # Variables
        self.story_text_var = tk.StringVar()
        self.progress_text_var = tk.StringVar()
        self.feedback_text_var = tk.StringVar()
        self.timer_text_var = tk.StringVar()
        self.metrics_text_var = tk.StringVar()
        
        # Componentes
        self.mission_title_label = None
        self.story_label = None
        self.feedback_label = None
        self.metrics_label = None
        self.progress_label = None
        self.timer_label = None
        self.mode_indicator = None
        self.options_frame = None
        self.next_button = None
        self.hint_button = None
        self.retry_button = None
        self.stats_labels = {}
        self.achievements_text = None
        self.after_id = None

    def create_main_layout(self):
        """Crea layout principal perfectamente ajustado."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors["white"], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo y título
        tk.Label(header_frame, text="🧠 PROYECTO ALPHA", 
                font=("Arial", 24, "bold"), bg=self.colors["white"], 
                fg=self.colors["primary"]).pack(side=tk.LEFT)
        
        # Progreso en header
        progress_frame = tk.Frame(header_frame, bg=self.colors["white"])
        progress_frame.pack(side=tk.RIGHT)
        
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_text_var,
                                      font=("Arial", 14, "bold"), bg=self.colors["white"], 
                                      fg=self.colors["text"])
        self.progress_label.pack()
        
        self.timer_label = tk.Label(progress_frame, textvariable=self.timer_text_var,
                                   font=("Arial", 12), bg=self.colors["white"], 
                                   fg=self.colors["gray"])
        self.timer_label.pack()
        
        # Contenido principal
        content_frame = tk.Frame(main_frame, bg='#f5f5f5')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo (contenido)
        left_panel = tk.Frame(content_frame, bg=self.colors["white"])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Panel derecho (estadísticas)
        right_panel = tk.Frame(content_frame, bg=self.colors["white"], width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        self.create_content_panel(left_panel)
        self.create_stats_panel(right_panel)

    def create_content_panel(self, parent):
        """Crea panel de contenido."""
        # Título de misión
        self.mission_title_label = tk.Label(parent, text="", 
                                           font=("Arial", 20, "bold"),
                                           bg=self.colors["white"], 
                                           fg=self.colors["text"],
                                           wraplength=800, justify=tk.LEFT)
        self.mission_title_label.pack(anchor=tk.W, padx=40, pady=(30, 20))
        
        # Historia
        story_frame = tk.Frame(parent, bg=self.colors["light"], relief=tk.FLAT, bd=2)
        story_frame.pack(fill=tk.X, padx=40, pady=(0, 30))
        
        self.story_label = tk.Label(story_frame, textvariable=self.story_text_var,
                                   font=("Arial", 16), bg=self.colors["light"],
                                   fg=self.colors["text"], wraplength=800, 
                                   justify=tk.LEFT, padx=30, pady=30)
        self.story_label.pack(fill=tk.X)
        
        # Título de opciones
        tk.Label(parent, text="Selecciona tu respuesta:", 
                font=("Arial", 16, "bold"), bg=self.colors["white"], 
                fg=self.colors["text"]).pack(anchor=tk.W, padx=40, pady=(0, 15))
        
        # Opciones
        self.options_frame = tk.Frame(parent, bg=self.colors["white"])
        self.options_frame.pack(fill=tk.X, padx=40, pady=(0, 30))
        
        # Feedback
        feedback_frame = tk.Frame(parent, bg=self.colors["light"], relief=tk.FLAT, bd=2)
        feedback_frame.pack(fill=tk.X, padx=40, pady=(0, 30))
        
        tk.Label(feedback_frame, text="Retroalimentación:", 
                font=("Arial", 16, "bold"), bg=self.colors["light"], 
                fg=self.colors["text"]).pack(anchor=tk.W, padx=30, pady=(20, 10))
        
        self.feedback_label = tk.Label(feedback_frame, textvariable=self.feedback_text_var,
                                      font=("Arial", 14), bg=self.colors["light"],
                                      fg=self.colors["text"], wraplength=800, 
                                      justify=tk.LEFT, padx=30, pady=(0, 10))
        self.feedback_label.pack(fill=tk.X)
        
        self.metrics_label = tk.Label(feedback_frame, textvariable=self.metrics_text_var,
                                     font=("Arial", 12), bg=self.colors["light"],
                                     fg=self.colors["gray"], padx=30, pady=(0, 20))
        self.metrics_label.pack(fill=tk.X)
        
        # Botones
        buttons_frame = tk.Frame(parent, bg=self.colors["white"])
        buttons_frame.pack(anchor=tk.W, padx=40, pady=(0, 30))
        
        self.next_button = tk.Button(buttons_frame, text="Comenzar",
                                    font=("Arial", 14, "bold"), bg=self.colors["primary"],
                                    fg="white", padx=30, pady=12, relief=tk.FLAT,
                                    cursor="hand2")
        self.next_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.hint_button = tk.Button(buttons_frame, text="💡 Pista",
                                    font=("Arial", 14, "bold"), bg=self.colors["warning"],
                                    fg="white", padx=20, pady=12, relief=tk.FLAT,
                                    cursor="hand2", state=tk.DISABLED)
        self.hint_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.retry_button = tk.Button(buttons_frame, text="🔄 Reintentar",
                                     font=("Arial", 14, "bold"), bg=self.colors["gray"],
                                     fg="white", padx=20, pady=12, relief=tk.FLAT,
                                     cursor="hand2", state=tk.DISABLED)
        self.retry_button.pack(side=tk.LEFT)

    def create_stats_panel(self, parent):
        """Crea panel de estadísticas."""
        # Título
        tk.Label(parent, text="📊 Estadísticas", font=("Arial", 18, "bold"),
                bg=self.colors["white"], fg=self.colors["text"]).pack(pady=(30, 20))
        
        # Estadísticas
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
            stat_frame = tk.Frame(parent, bg=self.colors["light"], height=50)
            stat_frame.pack(fill=tk.X, padx=20, pady=5)
            stat_frame.pack_propagate(False)
            
            tk.Label(stat_frame, text=label, font=("Arial", 12),
                    bg=self.colors["light"], fg=self.colors["text"]).pack(side=tk.LEFT, padx=15, pady=15)
            
            self.stats_labels[label] = tk.Label(stat_frame, text=value, 
                                               font=("Arial", 12, "bold"),
                                               bg=self.colors["light"], fg=self.colors["primary"])
            self.stats_labels[label].pack(side=tk.RIGHT, padx=15, pady=15)
        
        # Logros
        tk.Label(parent, text="🏆 Logros", font=("Arial", 18, "bold"),
                bg=self.colors["white"], fg=self.colors["text"]).pack(pady=(30, 20))
        
        self.achievements_text = tk.Text(parent, height=8, font=("Arial", 11),
                                        bg=self.colors["light"], fg=self.colors["text"],
                                        relief=tk.FLAT, wrap=tk.WORD, padx=15, pady=15)
        self.achievements_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 30))
        self.achievements_text.insert(tk.END, "Completa misiones para desbloquear logros")
        self.achievements_text.config(state=tk.DISABLED)

    def create_side_panel(self):
        """Método requerido."""
        pass

    def create_animations_canvas(self):
        """Método requerido."""
        pass

    def setup_animations(self):
        """Método requerido."""
        pass

    def create_menu_bar(self, callbacks: Dict[str, Callable]):
        """Crea menú."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva sesión", command=callbacks.get("new_session"))
        file_menu.add_command(label="Guardar", command=callbacks.get("save_progress"))
        file_menu.add_command(label="Cargar", command=callbacks.get("load_progress"))
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=callbacks.get("exit"))
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Tutorial", command=callbacks.get("show_tutorial"))
        help_menu.add_command(label="Acerca de", command=callbacks.get("show_about"))

    def clear_options(self):
        """Limpia opciones."""
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def create_option_buttons(self, mission_data: Dict[str, Any], callback: Callable):
        """Crea opciones perfectamente ajustadas."""
        options = list(mission_data["options"].items())
        
        for i, (choice_key, choice_description) in enumerate(options):
            # Frame de opción
            option_frame = tk.Frame(self.options_frame, bg=self.colors["white"], 
                                   relief=tk.SOLID, bd=1, cursor="hand2")
            option_frame.pack(fill=tk.X, pady=8)
            
            # Botón de letra
            letter_btn = tk.Button(option_frame, text=chr(65+i), 
                                  font=("Arial", 18, "bold"), bg=self.colors["primary"],
                                  fg="white", width=3, height=1, relief=tk.FLAT)
            letter_btn.pack(side=tk.LEFT, padx=15, pady=15)
            
            # Contenido
            content_frame = tk.Frame(option_frame, bg=self.colors["white"])
            content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 20), pady=15)
            
            title_label = tk.Label(content_frame, text=choice_key, 
                                  font=("Arial", 14, "bold"), bg=self.colors["white"],
                                  fg=self.colors["text"], wraplength=600, justify=tk.LEFT, anchor=tk.W)
            title_label.pack(fill=tk.X)
            
            desc_label = tk.Label(content_frame, text=choice_description,
                                 font=("Arial", 12), bg=self.colors["white"],
                                 fg=self.colors["gray"], wraplength=600, justify=tk.LEFT, anchor=tk.W)
            desc_label.pack(fill=tk.X, pady=(5, 0))
            
            # Efectos
            def on_enter(e, frame=option_frame, btn=letter_btn):
                frame.config(bg=self.colors["light"])
                btn.config(bg=self.colors["success"])
                content_frame.config(bg=self.colors["light"])
                title_label.config(bg=self.colors["light"])
                desc_label.config(bg=self.colors["light"])
            
            def on_leave(e, frame=option_frame, btn=letter_btn):
                frame.config(bg=self.colors["white"])
                btn.config(bg=self.colors["primary"])
                content_frame.config(bg=self.colors["white"])
                title_label.config(bg=self.colors["white"])
                desc_label.config(bg=self.colors["white"])
            
            def on_click(e, key=choice_key, frame=option_frame):
                frame.config(bg=self.colors["success"])
                callback(key, frame)
            
            # Bind eventos
            for widget in [option_frame, letter_btn, title_label, desc_label]:
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
        """Muestra texto."""
        self.story_text_var.set(full_text)
        if callback:
            callback()

    def show_tutorial(self):
        """Tutorial."""
        messagebox.showinfo("Tutorial", 
                           "PROYECTO ALPHA\n\n"
                           "1. Lee cada misión\n"
                           "2. Selecciona la respuesta correcta\n"
                           "3. Recibe retroalimentación\n"
                           "4. Usa pistas si necesitas ayuda\n\n"
                           "¡Disfruta aprendiendo IA!")

    def show_about(self):
        """Acerca de."""
        messagebox.showinfo("Acerca de", 
                           "PROYECTO ALPHA v4.0\n"
                           "Sistema de Aprendizaje de IA\n\n"
                           "Interfaz perfectamente ajustada\n"
                           "para la mejor experiencia educativa.")

    def show_message(self, title: str, message: str, type: str = "info"):
        """Muestra mensaje."""
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)