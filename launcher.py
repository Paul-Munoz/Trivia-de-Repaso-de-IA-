"""
Launcher - Selector de Modo de Juego
Permite elegir entre el juego original y los puzzles mentales.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class GameLauncher:
    """Lanzador de juegos."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Proyecto Alpha - Selector de Modo")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")
        
        self.create_ui()
    
    def create_ui(self):
        """Crea la interfaz del launcher."""
        # Título principal
        title_frame = tk.Frame(self.root, bg="#4a90e2", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🧠 PROYECTO ALPHA", 
                font=("Arial", 24, "bold"), bg="#4a90e2", fg="white").pack(expand=True)
        
        # Contenido principal
        content_frame = tk.Frame(self.root, bg="#f0f8ff")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(content_frame, text="Selecciona tu modo de aprendizaje:", 
                font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333").pack(pady=10)
        
        # Opción 1: Juego Original
        original_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=2)
        original_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(original_frame, text="📚 MODO TRADICIONAL", 
                font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=5)
        
        tk.Label(original_frame, 
                text="• 21 misiones educativas sobre IA\n• Preguntas de opción múltiple\n• Sistema de logros y métricas\n• Explicaciones detalladas", 
                font=("Arial", 11), bg="white", fg="#34495e", justify=tk.LEFT).pack(pady=5)
        
        tk.Button(original_frame, text="🚀 Jugar Modo Tradicional", 
                 font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                 command=self.launch_original, padx=20, pady=5).pack(pady=10)
        
        # Opción 2: Puzzles Mentales
        puzzle_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=2)
        puzzle_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(puzzle_frame, text="🧩 MODO PUZZLES MENTALES", 
                font=("Arial", 14, "bold"), bg="white", fg="#8e44ad").pack(pady=5)
        
        tk.Label(puzzle_frame, 
                text="• 8 desafíos cognitivos únicos\n• Tests de memoria y lógica\n• Adivinanzas y patrones\n• Entrenamiento mental intensivo", 
                font=("Arial", 11), bg="white", fg="#34495e", justify=tk.LEFT).pack(pady=5)
        
        tk.Button(puzzle_frame, text="🧠 Jugar Puzzles Mentales", 
                 font=("Arial", 12, "bold"), bg="#9b59b6", fg="white",
                 command=self.launch_puzzles, padx=20, pady=5).pack(pady=10)
        
        # Información adicional
        info_frame = tk.Frame(content_frame, bg="#e8f5e8", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(info_frame, text="💡 RECOMENDACIÓN", 
                font=("Arial", 12, "bold"), bg="#e8f5e8", fg="#27ae60").pack(pady=5)
        
        tk.Label(info_frame, 
                text="¿Primera vez? Prueba el Modo Tradicional para aprender conceptos.\n¿Quieres un desafío mental? Los Puzzles ejercitarán tu cerebro.", 
                font=("Arial", 10), bg="#e8f5e8", fg="#2c3e50", justify=tk.CENTER).pack(pady=5)
        
        # Botón de salir
        tk.Button(content_frame, text="❌ Salir", 
                 font=("Arial", 11), bg="#e74c3c", fg="white",
                 command=self.root.quit, padx=15, pady=3).pack(pady=20)
    
    def launch_original(self):
        """Lanza el juego original."""
        try:
            self.root.destroy()
            subprocess.run([sys.executable, "main.py"], cwd=os.getcwd())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el juego original:\n{str(e)}")
    
    def launch_puzzles(self):
        """Lanza los puzzles mentales."""
        try:
            self.root.destroy()
            subprocess.run([sys.executable, "main_puzzle.py"], cwd=os.getcwd())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar los puzzles:\n{str(e)}")
    
    def run(self):
        """Ejecuta el launcher."""
        self.root.mainloop()

def main():
    """Función principal."""
    launcher = GameLauncher()
    launcher.run()

if __name__ == "__main__":
    main()