"""
Puzzle UI Module - Interfaz para Juegos Mentales
Interfaces específicas para diferentes tipos de puzzles y desafíos cognitivos.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Dict, List, Any, Callable
from puzzle_games import PuzzleChallenge

class PuzzleUI:
    """Interfaz de usuario para juegos mentales y puzzles."""
    
    def __init__(self, parent_frame: tk.Frame):
        self.parent_frame = parent_frame
        self.current_puzzle = None
        self.start_time = None
        self.timer_job = None
        self.memory_study_job = None
        self.callback_function = None
        
        # Variables de UI
        self.puzzle_frame = None
        self.timer_var = tk.StringVar(value="⏱️ 00:00")
        self.score_var = tk.StringVar(value="🎯 Puntuación: 0")
        self.hint_var = tk.StringVar(value="💡 Pista disponible")
        
        self.setup_puzzle_ui()
    
    def setup_puzzle_ui(self):
        """Configura la interfaz base para puzzles."""
        # Frame principal para puzzles
        self.puzzle_frame = tk.Frame(self.parent_frame, bg="#f0f8ff", relief=tk.RAISED, bd=2)
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header con información del puzzle
        header_frame = tk.Frame(self.puzzle_frame, bg="#e6f3ff", height=60)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        # Timer y puntuación
        info_frame = tk.Frame(header_frame, bg="#e6f3ff")
        info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.timer_label = tk.Label(info_frame, textvariable=self.timer_var, 
                                   font=("Arial", 12, "bold"), bg="#e6f3ff", fg="#2c3e50")
        self.timer_label.pack(side=tk.TOP, pady=2)
        
        self.score_label = tk.Label(info_frame, textvariable=self.score_var,
                                   font=("Arial", 10), bg="#e6f3ff", fg="#27ae60")
        self.score_label.pack(side=tk.TOP, pady=2)
        
        # Botones de control
        control_frame = tk.Frame(header_frame, bg="#e6f3ff")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        self.hint_button = tk.Button(control_frame, textvariable=self.hint_var,
                                    font=("Arial", 9), bg="#f39c12", fg="white",
                                    relief=tk.RAISED, bd=2, padx=10)
        self.hint_button.pack(side=tk.TOP, pady=2)
        
        self.skip_button = tk.Button(control_frame, text="⏭️ Saltar",
                                    font=("Arial", 9), bg="#e74c3c", fg="white",
                                    relief=tk.RAISED, bd=2, padx=10)
        self.skip_button.pack(side=tk.TOP, pady=2)
        
        # Área de contenido del puzzle
        self.content_frame = tk.Frame(self.puzzle_frame, bg="#ffffff", relief=tk.SUNKEN, bd=1)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inicialmente oculto
        self.puzzle_frame.pack_forget()
    
    def show_puzzle(self, puzzle: PuzzleChallenge, callback: Callable):
        """Muestra un puzzle específico."""
        self.current_puzzle = puzzle
        self.callback_function = callback
        self.start_time = time.time()
        
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostrar el frame del puzzle
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configurar según el tipo de puzzle
        if puzzle.type == "logic_puzzle":
            self._show_logic_puzzle(puzzle)
        elif puzzle.type == "memory_test":
            self._show_memory_test(puzzle)
        elif puzzle.type == "riddle":
            self._show_riddle(puzzle)
        elif puzzle.type == "pattern_puzzle":
            self._show_pattern_puzzle(puzzle)
        
        # Iniciar timer
        self._start_timer()
        
        # Configurar botones
        self.hint_button.config(command=self._show_hint)
        self.skip_button.config(command=self._skip_puzzle)
    
    def _show_logic_puzzle(self, puzzle: PuzzleChallenge):
        """Muestra un puzzle de lógica."""
        # Título
        title_label = tk.Label(self.content_frame, text=puzzle.title,
                              font=("Arial", 16, "bold"), bg="#ffffff", fg="#2c3e50")
        title_label.pack(pady=10)
        
        # Descripción
        desc_label = tk.Label(self.content_frame, text=puzzle.description,
                             font=("Arial", 12), bg="#ffffff", fg="#34495e", wraplength=500)
        desc_label.pack(pady=5)
        
        # Área de drag & drop simulada con botones
        sequence_frame = tk.Frame(self.content_frame, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        sequence_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(sequence_frame, text="🎯 Arrastra los elementos al orden correcto:",
                font=("Arial", 11, "bold"), bg="#ecf0f1").pack(pady=5)
        
        # Elementos desordenados
        self.draggable_items = []
        items_frame = tk.Frame(sequence_frame, bg="#ecf0f1")
        items_frame.pack(pady=10)
        
        scrambled = puzzle.content.get("scrambled", puzzle.solution)
        for i, item in enumerate(scrambled):
            btn = tk.Button(items_frame, text=f"{i+1}. {item}",
                           font=("Arial", 10), bg="#3498db", fg="white",
                           relief=tk.RAISED, bd=2, padx=15, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
            btn.config(command=lambda x=item: self._select_sequence_item(x))
            self.draggable_items.append(btn)
        
        # Área de secuencia ordenada
        self.sequence_area = tk.Frame(sequence_frame, bg="#ffffff", relief=tk.SUNKEN, bd=2, height=60)
        self.sequence_area.pack(fill=tk.X, padx=10, pady=10)
        self.sequence_area.pack_propagate(False)
        
        tk.Label(self.sequence_area, text="Secuencia ordenada aparecerá aquí...",
                font=("Arial", 10, "italic"), bg="#ffffff", fg="#7f8c8d").pack(expand=True)
        
        self.selected_sequence = []
        
        # Botones de acción
        action_frame = tk.Frame(sequence_frame, bg="#ecf0f1")
        action_frame.pack(pady=10)
        
        tk.Button(action_frame, text="🔄 Reiniciar", command=self._reset_sequence,
                 bg="#e67e22", fg="white", font=("Arial", 10), padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="✅ Verificar", command=self._check_logic_solution,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"), padx=15).pack(side=tk.LEFT, padx=5)
    
    def _show_memory_test(self, puzzle: PuzzleChallenge):
        """Muestra un test de memoria."""
        # Título
        title_label = tk.Label(self.content_frame, text=puzzle.title,
                              font=("Arial", 16, "bold"), bg="#ffffff", fg="#8e44ad")
        title_label.pack(pady=10)
        
        # Descripción
        desc_label = tk.Label(self.content_frame, text=puzzle.description,
                             font=("Arial", 12), bg="#ffffff", fg="#34495e", wraplength=500)
        desc_label.pack(pady=5)
        
        # Fase de estudio
        study_frame = tk.Frame(self.content_frame, bg="#f8f9fa", relief=tk.RAISED, bd=2)
        study_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.study_label = tk.Label(study_frame, text="🧠 FASE DE ESTUDIO - Memoriza esta información:",
                                   font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#8e44ad")
        self.study_label.pack(pady=10)
        
        # Mostrar elementos a memorizar
        self.memory_content = tk.Frame(study_frame, bg="#ffffff", relief=tk.SUNKEN, bd=1)
        self.memory_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        items = puzzle.content.get("items", puzzle.content.get("sequence", []))
        for i, item in enumerate(items):
            if isinstance(item, tuple):
                text = f"📌 {item[0]}: {item[1]}"
            else:
                text = f"📌 {i+1}. {item}"
            
            item_label = tk.Label(self.memory_content, text=text,
                                 font=("Arial", 11), bg="#ffffff", fg="#2c3e50",
                                 anchor="w", padx=20, pady=5)
            item_label.pack(fill=tk.X)
        
        # Countdown timer para estudio
        self.study_timer_var = tk.StringVar(value=f"⏰ Tiempo de estudio: {puzzle.time_limit}s")
        study_timer_label = tk.Label(study_frame, textvariable=self.study_timer_var,
                                    font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#e74c3c")
        study_timer_label.pack(pady=5)
        
        # Iniciar countdown de estudio
        self._start_memory_study_timer(puzzle.time_limit)
    
    def _show_riddle(self, puzzle: PuzzleChallenge):
        """Muestra una adivinanza."""
        # Título
        title_label = tk.Label(self.content_frame, text=puzzle.title,
                              font=("Arial", 16, "bold"), bg="#ffffff", fg="#e67e22")
        title_label.pack(pady=10)
        
        # Adivinanza
        riddle_frame = tk.Frame(self.content_frame, bg="#fef9e7", relief=tk.RAISED, bd=2)
        riddle_frame.pack(pady=20, padx=20, fill=tk.X)
        
        riddle_text = puzzle.content["riddle"]
        riddle_label = tk.Label(riddle_frame, text=riddle_text,
                               font=("Arial", 14), bg="#fef9e7", fg="#d68910",
                               wraplength=500, justify=tk.CENTER)
        riddle_label.pack(pady=20, padx=20)
        
        # Opciones de respuesta
        options_frame = tk.Frame(self.content_frame, bg="#ffffff")
        options_frame.pack(pady=20)
        
        tk.Label(options_frame, text="🤔 Selecciona tu respuesta:",
                font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
        
        self.riddle_var = tk.StringVar()
        options = puzzle.content["options"]
        
        for option in options:
            rb = tk.Radiobutton(options_frame, text=option, variable=self.riddle_var,
                               value=option, font=("Arial", 11), bg="#ffffff",
                               activebackground="#f8f9fa", padx=20, pady=5)
            rb.pack(anchor=tk.W, padx=50)
        
        # Botón de respuesta
        tk.Button(options_frame, text="🎯 Responder", command=self._check_riddle_solution,
                 bg="#e67e22", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5).pack(pady=15)
    
    def _show_pattern_puzzle(self, puzzle: PuzzleChallenge):
        """Muestra un puzzle de patrones."""
        # Título
        title_label = tk.Label(self.content_frame, text=puzzle.title,
                              font=("Arial", 16, "bold"), bg="#ffffff", fg="#9b59b6")
        title_label.pack(pady=10)
        
        # Descripción
        desc_label = tk.Label(self.content_frame, text=puzzle.description,
                             font=("Arial", 12), bg="#ffffff", fg="#34495e", wraplength=500)
        desc_label.pack(pady=5)
        
        # Patrón
        pattern_frame = tk.Frame(self.content_frame, bg="#f4f1fb", relief=tk.RAISED, bd=2)
        pattern_frame.pack(pady=20, padx=20, fill=tk.X)
        
        sequence_text = " → ".join(puzzle.content["sequence"])
        pattern_label = tk.Label(pattern_frame, text=sequence_text,
                                font=("Arial", 16, "bold"), bg="#f4f1fb", fg="#8e44ad")
        pattern_label.pack(pady=20)
        
        # Opciones de respuesta
        answer_frame = tk.Frame(self.content_frame, bg="#ffffff")
        answer_frame.pack(pady=20)
        
        tk.Label(answer_frame, text="🧩 ¿Qué sigue en el patrón?",
                font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
        
        self.pattern_var = tk.StringVar()
        options = puzzle.content["options"]
        
        for option in options:
            rb = tk.Radiobutton(answer_frame, text=option, variable=self.pattern_var,
                               value=option, font=("Arial", 11), bg="#ffffff",
                               activebackground="#f8f9fa", padx=20, pady=5)
            rb.pack(anchor=tk.W, padx=50)
        
        # Botón de respuesta
        tk.Button(answer_frame, text="🔍 Verificar Patrón", command=self._check_pattern_solution,
                 bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5).pack(pady=15)
    
    def _select_sequence_item(self, item: str):
        """Selecciona un elemento para la secuencia."""
        if item not in self.selected_sequence:
            self.selected_sequence.append(item)
            self._update_sequence_display()
    
    def _update_sequence_display(self):
        """Actualiza la visualización de la secuencia ordenada."""
        for widget in self.sequence_area.winfo_children():
            widget.destroy()
        
        if self.selected_sequence:
            sequence_text = " → ".join(self.selected_sequence)
            tk.Label(self.sequence_area, text=sequence_text,
                    font=("Arial", 11, "bold"), bg="#ffffff", fg="#27ae60").pack(expand=True)
        else:
            tk.Label(self.sequence_area, text="Secuencia ordenada aparecerá aquí...",
                    font=("Arial", 10, "italic"), bg="#ffffff", fg="#7f8c8d").pack(expand=True)
    
    def _reset_sequence(self):
        """Reinicia la secuencia seleccionada."""
        self.selected_sequence = []
        self._update_sequence_display()
    
    def _check_logic_solution(self):
        """Verifica la solución del puzzle de lógica."""
        if self.callback_function:
            self.callback_function(self.selected_sequence)
    
    def _check_riddle_solution(self):
        """Verifica la solución de la adivinanza."""
        answer = self.riddle_var.get()
        if answer and self.callback_function:
            self.callback_function(answer)
        else:
            messagebox.showwarning("Respuesta Requerida", "Por favor selecciona una respuesta.")
    
    def _check_pattern_solution(self):
        """Verifica la solución del puzzle de patrones."""
        answer = self.pattern_var.get()
        if answer and self.callback_function:
            self.callback_function(answer)
        else:
            messagebox.showwarning("Respuesta Requerida", "Por favor selecciona una respuesta.")
    
    def _start_timer(self):
        """Inicia el temporizador del puzzle."""
        self._update_timer()
    
    def _update_timer(self):
        """Actualiza el temporizador."""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_var.set(f"⏱️ {minutes:02d}:{seconds:02d}")
            
            # Continuar actualizando
            self.timer_job = self.content_frame.after(1000, self._update_timer)
    
    def _start_memory_study_timer(self, duration: int):
        """Inicia el temporizador de estudio para memory test."""
        self.study_time_left = duration
        self._update_study_timer()
    
    def _update_study_timer(self):
        """Actualiza el temporizador de estudio."""
        if self.study_time_left > 0:
            self.study_timer_var.set(f"⏰ Tiempo de estudio: {self.study_time_left}s")
            self.study_time_left -= 1
            self.memory_study_job = self.content_frame.after(1000, self._update_study_timer)
        else:
            self._start_memory_questions()
    
    def _start_memory_questions(self):
        """Inicia la fase de preguntas del memory test."""
        # Ocultar contenido de estudio
        self.memory_content.pack_forget()
        self.study_label.config(text="🧠 FASE DE PREGUNTAS - ¿Qué recuerdas?")
        
        # Mostrar preguntas
        questions_frame = tk.Frame(self.content_frame, bg="#ffffff")
        questions_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        questions = self.current_puzzle.content.get("questions", ["¿Qué elementos recuerdas?"])
        
        self.memory_answers = {}
        for i, question in enumerate(questions):
            q_frame = tk.Frame(questions_frame, bg="#f8f9fa", relief=tk.RAISED, bd=1)
            q_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(q_frame, text=f"❓ {question}",
                    font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor=tk.W, padx=10, pady=5)
            
            answer_entry = tk.Entry(q_frame, font=("Arial", 10), width=50)
            answer_entry.pack(padx=10, pady=5)
            
            self.memory_answers[question] = answer_entry
        
        # Botón para enviar respuestas
        tk.Button(questions_frame, text="🧠 Enviar Respuestas", command=self._check_memory_solution,
                 bg="#8e44ad", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5).pack(pady=15)
    
    def _check_memory_solution(self):
        """Verifica las respuestas del memory test."""
        answers = {}
        for question, entry in self.memory_answers.items():
            answers[question] = entry.get()
        
        if self.callback_function:
            self.callback_function(answers)
    
    def _show_hint(self):
        """Muestra una pista."""
        if self.current_puzzle and self.callback_function:
            # Llamar al callback con una señal especial para pista
            self.callback_function("__HINT_REQUEST__")
    
    def _skip_puzzle(self):
        """Salta el puzzle actual."""
        if self.callback_function:
            self.callback_function("__SKIP_PUZZLE__")
    
    def hide_puzzle(self):
        """Oculta la interfaz del puzzle."""
        if self.timer_job:
            self.content_frame.after_cancel(self.timer_job)
        if self.memory_study_job:
            self.content_frame.after_cancel(self.memory_study_job)
        
        self.puzzle_frame.pack_forget()
    
    def update_score(self, score: int):
        """Actualiza la puntuación mostrada."""
        self.score_var.set(f"🎯 Puntuación: {score}")
    
    def show_result(self, is_correct: bool, message: str):
        """Muestra el resultado del puzzle."""
        color = "#27ae60" if is_correct else "#e74c3c"
        icon = "✅" if is_correct else "❌"
        
        result_window = tk.Toplevel(self.content_frame)
        result_window.title("Resultado del Puzzle")
        result_window.geometry("400x200")
        result_window.configure(bg="#ffffff")
        result_window.transient(self.content_frame.winfo_toplevel())
        result_window.grab_set()
        
        # Centrar ventana
        result_window.geometry("+%d+%d" % (
            result_window.winfo_toplevel().winfo_rootx() + 100,
            result_window.winfo_toplevel().winfo_rooty() + 100
        ))
        
        tk.Label(result_window, text=f"{icon} Resultado",
                font=("Arial", 16, "bold"), bg="#ffffff", fg=color).pack(pady=20)
        
        tk.Label(result_window, text=message,
                font=("Arial", 11), bg="#ffffff", fg="#2c3e50",
                wraplength=350, justify=tk.CENTER).pack(pady=10, padx=20)
        
        tk.Button(result_window, text="Continuar", command=result_window.destroy,
                 bg=color, fg="white", font=("Arial", 12, "bold"), padx=20).pack(pady=20)
        
        # Auto-cerrar después de 3 segundos si es correcto
        if is_correct:
            result_window.after(3000, result_window.destroy)