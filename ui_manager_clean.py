"""
UI Manager Limpio - Proyecto Alpha v4.0
Interfaz limpia sin problemas de padding.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Callable, List


class UIManager:
    """Gestor de interfaz limpia y funcional."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.configure(bg='white')
        self.root.geometry("1200x800")
        self.root.title("Proyecto Alpha - Sistema de Aprendizaje de IA")
        
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
        """Crea layout principal."""
        # Header
        header = tk.Frame(self.root, bg='#4a90e2', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🧠 PROYECTO ALPHA", font=("Arial", 20, "bold"),
                bg='#4a90e2', fg='white').pack(side=tk.LEFT)
        
        progress_frame = tk.Frame(header, bg='#4a90e2')
        progress_frame.pack(side=tk.RIGHT)
        
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_text_var,
                                      font=("Arial", 12, "bold"), bg='#4a90e2', fg='white')
        self.progress_label.pack()
        
        self.timer_label = tk.Label(progress_frame, textvariable=self.timer_text_var,
                                   font=("Arial", 10), bg='#4a90e2', fg='white')
        self.timer_label.pack()
        
        # Contenido
        content = tk.Frame(self.root, bg='white')
        content.pack(fill=tk.BOTH, expand=True)
        
        # Panel principal
        main_panel = tk.Frame(content, bg='white')
        main_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Panel lateral
        side_panel = tk.Frame(content, bg='#f0f0f0', width=250)
        side_panel.pack(side=tk.RIGHT, fill=tk.Y)
        side_panel.pack_propagate(False)
        
        self.create_main_content(main_panel)
        self.create_sidebar(side_panel)

    def create_main_content(self, parent):
        """Crea contenido principal."""
        # Título
        self.mission_title_label = tk.Label(parent, text="", font=("Arial", 18, "bold"),
                                           bg='white', fg='#333', wraplength=700, justify=tk.LEFT)
        self.mission_title_label.pack(anchor=tk.W)
        
        # Historia
        story_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.RAISED, bd=1)
        story_frame.pack(fill=tk.X)
        
        self.story_label = tk.Label(story_frame, textvariable=self.story_text_var,
                                   font=("Arial", 14), bg='#f8f9fa', fg='#333',
                                   wraplength=700, justify=tk.LEFT)
        self.story_label.pack(fill=tk.X)
        
        # Opciones
        tk.Label(parent, text="Selecciona tu respuesta:", font=("Arial", 14, "bold"),
                bg='white', fg='#333').pack(anchor=tk.W)
        
        self.options_frame = tk.Frame(parent, bg='white')
        self.options_frame.pack(fill=tk.X)
        
        # Feedback
        feedback_frame = tk.Frame(parent, bg='#e8f5e8', relief=tk.RAISED, bd=1)
        feedback_frame.pack(fill=tk.X)
        
        tk.Label(feedback_frame, text="Retroalimentación:", font=("Arial", 14, "bold"),
                bg='#e8f5e8', fg='#333').pack(anchor=tk.W)
        
        self.feedback_label = tk.Label(feedback_frame, textvariable=self.feedback_text_var,
                                      font=("Arial", 12), bg='#e8f5e8', fg='#333',
                                      wraplength=700, justify=tk.LEFT)
        self.feedback_label.pack(fill=tk.X)
        
        self.metrics_label = tk.Label(feedback_frame, textvariable=self.metrics_text_var,
                                     font=("Arial", 10), bg='#e8f5e8', fg='#666')
        self.metrics_label.pack(fill=tk.X)
        
        # Botones
        buttons = tk.Frame(parent, bg='white')
        buttons.pack(anchor=tk.W)
        
        self.next_button = tk.Button(buttons, text="Comenzar", font=("Arial", 12, "bold"),
                                    bg='#4a90e2', fg='white', relief=tk.FLAT, cursor="hand2")
        self.next_button.pack(side=tk.LEFT)
        
        self.hint_button = tk.Button(buttons, text="💡 Pista", font=("Arial", 12, "bold"),
                                    bg='#f5a623', fg='white', relief=tk.FLAT, cursor="hand2",
                                    state=tk.DISABLED)
        self.hint_button.pack(side=tk.LEFT)
        
        self.retry_button = tk.Button(buttons, text="🔄 Reintentar", font=("Arial", 12, "bold"),
                                     bg='#95a5a6', fg='white', relief=tk.FLAT, cursor="hand2",
                                     state=tk.DISABLED)
        self.retry_button.pack(side=tk.LEFT)

    def create_sidebar(self, parent):
        """Crea barra lateral."""
        tk.Label(parent, text="📊 Estadísticas", font=("Arial", 16, "bold"),
                bg='#f0f0f0', fg='#333').pack()
        
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
            frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X)
            
            tk.Label(frame, text=label, font=("Arial", 10), bg='white', fg='#333').pack(side=tk.LEFT)
            self.stats_labels[label] = tk.Label(frame, text=value, font=("Arial", 10, "bold"),
                                               bg='white', fg='#4a90e2')
            self.stats_labels[label].pack(side=tk.RIGHT)
        
        tk.Label(parent, text="🏆 Logros", font=("Arial", 16, "bold"),
                bg='#f0f0f0', fg='#333').pack()
        
        self.achievements_text = tk.Text(parent, height=8, font=("Arial", 10),
                                        bg='white', fg='#333', relief=tk.FLAT, wrap=tk.WORD)
        self.achievements_text.pack(fill=tk.BOTH, expand=True)
        self.achievements_text.insert(tk.END, "Completa misiones para desbloquear logros")
        self.achievements_text.config(state=tk.DISABLED)

    def create_side_panel(self):
        pass

    def create_animations_canvas(self):
        pass

    def setup_animations(self):
        pass

    def create_menu_bar(self, callbacks: Dict[str, Callable]):
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
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def create_option_buttons(self, mission_data: Dict[str, Any], callback: Callable):
        options = list(mission_data["options"].items())
        
        for i, (choice_key, choice_description) in enumerate(options):
            frame = tk.Frame(self.options_frame, bg='#e3f2fd', relief=tk.RAISED, bd=1, cursor="hand2")
            frame.pack(fill=tk.X)
            
            btn = tk.Button(frame, text=chr(65+i), font=("Arial", 16, "bold"),
                           bg='#4a90e2', fg='white', width=3, relief=tk.FLAT)
            btn.pack(side=tk.LEFT)
            
            content = tk.Frame(frame, bg='#e3f2fd')
            content.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            title = tk.Label(content, text=choice_key, font=("Arial", 12, "bold"),
                            bg='#e3f2fd', fg='#333', wraplength=500, justify=tk.LEFT, anchor=tk.W)
            title.pack(fill=tk.X)
            
            desc = tk.Label(content, text=choice_description, font=("Arial", 10),
                           bg='#e3f2fd', fg='#666', wraplength=500, justify=tk.LEFT, anchor=tk.W)
            desc.pack(fill=tk.X)
            
            def on_click(e, key=choice_key, f=frame):
                f.config(bg='#c8e6c9')
                callback(key, f)
            
            for widget in [frame, btn, title, desc]:
                widget.bind("<Button-1>", on_click)

    def update_progress_display(self, score: int, max_score: int):
        pass

    def update_stats_display(self, stats: Dict[str, Any]):
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
        self.achievements_text.config(state=tk.NORMAL)
        self.achievements_text.delete(1.0, tk.END)
        
        if achievements:
            for achievement in achievements[-5:]:
                self.achievements_text.insert(tk.END, f"🏆 {achievement}\n")
        else:
            self.achievements_text.insert(tk.END, "Completa misiones para desbloquear logros")
        
        self.achievements_text.config(state=tk.DISABLED)

    def type_story_effect(self, full_text: str, callback: callable = None):
        self.story_text_var.set(full_text)
        if callback:
            callback()

    def show_tutorial(self):
        messagebox.showinfo("Tutorial", 
                           "PROYECTO ALPHA\n\n"
                           "1. Lee cada misión\n"
                           "2. Selecciona la respuesta correcta\n"
                           "3. Recibe retroalimentación\n"
                           "4. Usa pistas si necesitas ayuda\n\n"
                           "¡Disfruta aprendiendo IA!")

    def show_about(self):
        messagebox.showinfo("Acerca de", 
                           "PROYECTO ALPHA v4.0\n"
                           "Sistema de Aprendizaje de IA\n\n"
                           "Interfaz limpia y funcional\n"
                           "para la mejor experiencia educativa.")

    def show_message(self, title: str, message: str, type: str = "info"):
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "error":
            messagebox.showerror(title, message)