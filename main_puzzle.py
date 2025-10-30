"""
Main Puzzle Game - Juego de Puzzles Mentales
Versión simplificada que funciona perfectamente.
"""

import tkinter as tk
from tkinter import messagebox
import time
from puzzle_game_simple import PuzzleGame
from ui_manager_clean import UIManager

class PuzzleController:
    """Controlador simplificado para puzzles mentales."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.ui_manager = UIManager(root)
        self.puzzle_game = PuzzleGame(self.ui_manager)
        
        # Estado del juego
        self.current_mission = 0
        self.total_missions = 8  # Número de puzzles
        self.session_start_time = time.time()
        self.hints_used = 0
        
        self.setup_ui()
        self.start_session()
    
    def setup_ui(self):
        """Configura la interfaz."""
        self.ui_manager.create_main_layout()
        
        # Conectar botones
        self.ui_manager.next_button.config(command=self.next_puzzle)
        self.ui_manager.hint_button.config(command=self.show_hint)
        self.ui_manager.retry_button.config(command=self.retry_puzzle)
        
        # Crear menú simple
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Juego", menu=file_menu)
        file_menu.add_command(label="Nuevo juego", command=self.restart_game)
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Cómo jugar", command=self.show_help)
    
    def start_session(self):
        """Inicia la sesión de puzzles."""
        self.ui_manager.mission_title_label.config(text="🧩 PUZZLES MENTALES DE IA")
        
        intro_text = (
            "¡Bienvenido a los Puzzles Mentales de IA! 🧠\n\n"
            "🎯 DESAFÍOS INCLUIDOS:\n\n"
            "🧠 Tests de Memoria - Memoriza y recuerda conceptos\n"
            "🧩 Rompecabezas Lógicos - Conecta ideas correctamente\n"
            "🎭 Adivinanzas - Resuelve acertijos creativos\n"
            "🔍 Patrones - Completa secuencias algorítmicas\n\n"
            "¡Cada puzzle ejercitará tu mente de forma diferente!"
        )
        
        self.ui_manager.story_text_var.set(intro_text)
        self.ui_manager.feedback_text_var.set("Haz clic en 'Comenzar' para empezar tu entrenamiento mental.")
        self.ui_manager.progress_text_var.set(f"🧩 Puzzle 0/{self.total_missions}")
        self.ui_manager.timer_text_var.set("⏱️ 00:00")
        
        self.ui_manager.next_button.config(text="🚀 Comenzar", state=tk.NORMAL)
        self.ui_manager.hint_button.config(state=tk.DISABLED)
        self.ui_manager.retry_button.config(state=tk.DISABLED)
        
        self.ui_manager.clear_options()
        self.start_timer()
    
    def next_puzzle(self):
        """Avanza al siguiente puzzle."""
        if self.current_mission < self.total_missions:
            self.current_mission += 1
            self.load_puzzle()
        else:
            self.complete_game()
    
    def load_puzzle(self):
        """Carga un puzzle."""
        self.puzzle_game.start_puzzle(self.current_mission - 1)
        
        # Actualizar UI
        self.ui_manager.progress_text_var.set(f"🧩 Puzzle {self.current_mission}/{self.total_missions}")
        self.ui_manager.next_button.config(state=tk.DISABLED)
        self.ui_manager.hint_button.config(state=tk.NORMAL)
        self.ui_manager.retry_button.config(state=tk.NORMAL, text="🔄 Nuevo Puzzle")
        
        # Actualizar estadísticas
        stats = self.puzzle_game.get_stats()
        self.update_stats_display(stats)
    
    def handle_puzzle_answer(self, selected_option: str, option_widget):
        """Maneja la respuesta del puzzle (llamado por PuzzleGame)."""
        is_correct = self.puzzle_game.handle_answer(selected_option, option_widget)
        
        # Habilitar siguiente puzzle
        if self.current_mission < self.total_missions:
            self.ui_manager.next_button.config(text=f"➡️ Puzzle {self.current_mission + 1}", state=tk.NORMAL)
        else:
            self.ui_manager.next_button.config(text="🏆 Finalizar", state=tk.NORMAL)
        
        # Deshabilitar hint
        self.ui_manager.hint_button.config(state=tk.DISABLED)
        
        # Actualizar estadísticas
        stats = self.puzzle_game.get_stats()
        self.update_stats_display(stats)
    
    def show_hint(self):
        """Muestra una pista."""
        hint = self.puzzle_game.get_hint()
        self.hints_used += 1
        
        self.ui_manager.feedback_text_var.set(f"💡 PISTA: {hint}")
        self.ui_manager.hint_button.config(state=tk.DISABLED)
    
    def retry_puzzle(self):
        """Reintenta el puzzle actual."""
        if self.current_mission > 0:
            # Cargar nuevo puzzle del mismo tipo
            new_puzzle_num = (self.current_mission - 1 + self.total_missions) % len(self.puzzle_game.puzzles)
            self.puzzle_game.start_puzzle(new_puzzle_num)
            
            self.ui_manager.next_button.config(state=tk.DISABLED)
            self.ui_manager.hint_button.config(state=tk.NORMAL)
            self.ui_manager.feedback_text_var.set("🔄 Nuevo puzzle cargado. ¡Inténtalo de nuevo!")
    
    def complete_game(self):
        """Completa el juego."""
        stats = self.puzzle_game.get_stats()
        total_time = time.time() - self.session_start_time
        
        result_text = (
            f"🎉 ¡PUZZLES COMPLETADOS! 🎉\n\n"
            f"🧩 Puzzles resueltos: {stats['completed']}/{stats['total']}\n"
            f"🏆 Puntuación total: {stats['score']} puntos\n"
            f"⏱️ Tiempo total: {int(total_time//60)}:{int(total_time%60):02d}\n"
            f"💡 Pistas usadas: {self.hints_used}\n\n"
            f"🧠 ¡Excelente entrenamiento mental!"
        )
        
        self.ui_manager.feedback_text_var.set(result_text)
        self.ui_manager.next_button.config(text="✅ Completado", state=tk.DISABLED)
        self.ui_manager.hint_button.config(state=tk.DISABLED)
        self.ui_manager.retry_button.config(state=tk.DISABLED)
        
        messagebox.showinfo("¡Felicitaciones!", 
                           f"Has completado todos los puzzles mentales!\n\n"
                           f"Puntuación: {stats['score']} puntos\n"
                           f"Tiempo: {int(total_time//60)}:{int(total_time%60):02d}")
    
    def update_stats_display(self, stats):
        """Actualiza las estadísticas en pantalla."""
        if hasattr(self.ui_manager, 'stats_labels'):
            mappings = {
                "Puntuación": f"{stats['score']} pts",
                "Completados": f"{stats['completed']}/{stats['total']}",
                "Pistas": str(self.hints_used),
                "Tiempo": self.format_time()
            }
            
            for label, value in mappings.items():
                if label in self.ui_manager.stats_labels:
                    self.ui_manager.stats_labels[label].config(text=value)
    
    def format_time(self) -> str:
        """Formatea el tiempo transcurrido."""
        elapsed = int(time.time() - self.session_start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def start_timer(self):
        """Inicia el temporizador."""
        def update_timer():
            self.ui_manager.timer_text_var.set(f"⏱️ {self.format_time()}")
            self.root.after(1000, update_timer)
        
        update_timer()
    
    def restart_game(self):
        """Reinicia el juego."""
        self.current_mission = 0
        self.hints_used = 0
        self.session_start_time = time.time()
        self.puzzle_game.puzzle_score = 0
        self.puzzle_game.puzzles_completed = 0
        self.start_session()
    
    def show_help(self):
        """Muestra ayuda."""
        help_text = (
            "🧩 CÓMO JUGAR PUZZLES MENTALES\n\n"
            "🎯 OBJETIVO:\n"
            "Resolver 8 puzzles diferentes sobre IA\n\n"
            "🧠 TIPOS DE PUZZLES:\n"
            "• Memoria: Memoriza y recuerda\n"
            "• Lógica: Conecta conceptos\n"
            "• Adivinanzas: Resuelve acertijos\n"
            "• Patrones: Completa secuencias\n\n"
            "💡 PISTAS:\n"
            "Usa el botón 'Pista' si necesitas ayuda\n\n"
            "🏆 PUNTUACIÓN:\n"
            "10 puntos por cada puzzle correcto"
        )
        messagebox.showinfo("Cómo Jugar", help_text)

def main():
    """Función principal."""
    root = tk.Tk()
    root.title("Puzzles Mentales de IA")
    root.geometry("1200x800")
    
    # Configurar el controlador
    controller = PuzzleController(root)
    
    # Conectar el manejador de respuestas
    original_create_options = controller.ui_manager.create_option_buttons
    
    def create_options_with_handler(mission_data, callback):
        def new_callback(selected_option, option_widget):
            controller.handle_puzzle_answer(selected_option, option_widget)
        return original_create_options(mission_data, new_callback)
    
    controller.ui_manager.create_option_buttons = create_options_with_handler
    
    root.mainloop()

if __name__ == "__main__":
    main()