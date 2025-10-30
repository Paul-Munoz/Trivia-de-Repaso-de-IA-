# -*- coding: utf-8 -*-
"""
EL ENIGMA DEL PROYECTO 'ALPHA'
Juego de Aventura de Texto Interactivo para el Aprendizaje Indirecto.

MEJORAS IMPLEMENTADAS:
- Sistema de progreso visual mejorado con barra de progreso
- Efectos de sonido simulados (visuales)
- Estadísticas detalladas de rendimiento
- Sistema de logros y recompensas
- Mejor feedback educativo con ejemplos prácticos
- Navegación más intuitiva
- Diseño responsive mejorado
"""
import tkinter as tk
from tkinter import messagebox
import random
import time

# --- PALETA DE COLORES Y ESTILOS MEJORADA ---
COLORS = {
    "bg_primary": "#0A192F",
    "bg_secondary": "#1E3A5F",
    "option_bg": "#0D2038",
    "primary_glow": "#64FFDA",
    "secondary_glow": "#FFC74D",
    "error_red": "#FF6B6B",
    "success_green": "#4CAF50",
    "text_dark_accent": "#B0C4DE",
    "text_white": "#FFFFFF",
    "progress_bg": "#2D3748",
    "progress_fill": "#4299E1",
}

# --- ESTADO DEL JUEGO MEJORADO ---
GAME_STATE = {
    "mission": 1,
    "score": 0,
    "max_score": 0,
    "current_choices": [],
    "feedback": "",
    "current_story_idx": 0,
    "story_full_text": "",
    "correct_answers": 0,
    "total_answers": 0,
    "concept_mastery": {},  # Seguimiento de conceptos aprendidos
    "achievements": [],     # Logros desbloqueados
    "start_time": time.time(),
}

# --- NARRATIVA EXPANDIDA CON MÁS CONCEPTOS ---
MISSIONS = {
    1: {
        "title": "Misión 1: Arquitectura del Motor 'Hyperion'",
        "story": "¡Atención, Comandante! La primera fase del Proyecto Alpha requiere tu pericia. Debemos elegir la tecnología central para el motor de navegación 'Hyperion'. La tarea es crítica: debe **analizar patrones visuales de nebulosas extremadamente complejos** y ajustar el rumbo en milisegundos. ¿Qué enfoque de IA propones para una tarea tan intensiva en reconocimiento de patrones visuales profundos?",
        "concept_name": "Fase de IA / Técnica de Procesamiento",
        "concept_key": "deep_learning",
        "options": {
            "Machine Learning (ML)": "Utiliza algoritmos estadísticos y matemáticos. Eficiente para datos estructurados, pero puede quedarse corto con la complejidad visual del espacio profundo.",
            "Neural Network (NN)": "Modelos inspirados en el cerebro humano con capas de neuronas. Funciona bien para ciertos patrones, pero el Hyperion necesita una comprensión 'más profunda' de las imágenes.",
            "Deep Learning (DL)": "Redes neuronales con múltiples capas ocultas que permiten aprender representaciones jerárquicas de datos. **Ideal para la identificación profunda y abstracta de patrones visuales complejos**.",
            "IA Generativa (IA Gen)": "Se enfoca en crear nuevos datos (texto, imágenes, etc.). Su función principal no es el análisis puro y duro de patrones existentes."
        },
        "answer": "Deep Learning (DL)",
        "feedback": {
            "correct": "¡Elección vital! El **Deep Learning (DL)** es la única Fase de IA capaz de extraer características complejas y abstractas de datos no estructurados como las imágenes del espacio profundo. Su arquitectura de capas permite una comprensión jerárquica de la información visual. ¡Has asegurado la capacidad de navegación del Hyperion!",
            "incorrect": "Decisión de alto riesgo. Aunque todas son Fases de IA, el **Deep Learning (DL)** es el más adecuado para el análisis profundo de patrones visuales complejos. ML se queda corto, y NN no es tan 'profundo' como DL. IA Gen tiene otro propósito. ¡Recuerda las capacidades específicas de cada fase!"
        },
        "decisions": 1
    },
    2: {
        "title": "Misión 2: Configuración de la IA de Bordo 'Orion'",
        "story": "El motor Hyperion está operativo. Ahora nos centramos en el copiloto robótico, 'Orion'. Necesitamos que Orion pueda **recordar la trayectoria de los asteroides y naves aliadas de los últimos 5 minutos** para predecir colisiones y planificar rutas seguras. Sin embargo, no necesitamos que entienda o simule emociones humanas. ¿Qué clasificación de IA define mejor esta capacidad requerida?",
        "concept_name": "Clasificación de la IA / Tipo de Conciencia",
        "concept_key": "memoria_limitada",
        "options": {
            "Máquina Reactiva": "Solo reacciona al instante presente sin memoria. Sería incapaz de predecir o aprender de movimientos pasados.",
            "Memoria Limitada": "Puede almacenar datos recientes del pasado (como la trayectoria reciente de objetos). **Perfecto para un comportamiento contextual y predictivo a corto plazo**.",
            "Teoría de la Mente": "Implica inferir deseos, creencias y emociones. Sobrepasa la necesidad y podría introducir inestabilidad en la navegación.",
            "Inteligencia General (AGI)": "Capacidad cognitiva humana total en múltiples dominios. Un riesgo innecesario y tecnológicamente prematuro para una nave."
        },
        "answer": "Memoria Limitada",
        "feedback": {
            "correct": "Correcto. La clasificación **Memoria Limitada** es la elección óptima. Permite a Orion un comportamiento contextual (recordar el pasado reciente) crucial para la predicción de movimientos, a diferencia de una Máquina Reactiva (solo presente). ¡Orion ahora es un copiloto fiable!",
            "incorrect": "Elección arriesgada. La **Memoria Limitada** es fundamental aquí. Una Máquina Reactiva carece de memoria, mientras que 'Teoría de la Mente' o AGI son innecesarias y demasiado complejas para esta tarea. ¡Comprender la capacidad de memoria es clave para el control de la nave!"
        },
        "decisions": 1
    },
    3: {
        "title": "CRISIS DE ENERGÍA: Análisis del Sistema Auxiliar",
        "story": "¡Alerta Roja! El sistema de energía auxiliar ha reportado un fallo crítico. El equipo de ingenieros te presenta los datos del sistema de diagnóstico de IA: Hay un grave problema de **Falsos Negativos (FN)**, lo que significa que **fallos reales están pasando desapercibidos**, poniendo en riesgo la tripulación. Necesitas una métrica que priorice detectar cada fallo, aunque eso implique algunas falsas alarmas. ¿Qué métrica debemos optimizar para minimizar los riesgos reales?",
        "concept_name": "Métrica Clave para Optimización",
        "concept_key": "sensibilidad",
        "options": {
            "Precisión (Precision)": "Prioriza la fiabilidad de las predicciones positivas (VP / (VP+FP)). Disminuiría las falsas alarmas, pero podría aumentar los FN.",
            "Especificidad": "Mide cuántos negativos reales (no fallos) se clasifican correctamente (VN / (VN+FP)). No es el foco principal aquí.",
            "Sensibilidad (Recall)": "Mide cuántos fallos REALES (positivos) detectamos (VP / (VP+FN)). **Maximizarla es crucial para no dejar ningún fallo sin identificar.**",
            "F-Score": "Busca un balance entre Precisión y Sensibilidad. En una crisis de seguridad, puede que no sea el momento de balancear, sino de priorizar la detección."
        },
        "answer": "Sensibilidad (Recall)",
        "feedback": {
            "correct": "¡Decisión de un experto! Para minimizar los **Falsos Negativos (FN)** y asegurar que no se pase por alto ningún fallo real, debes maximizar la **Sensibilidad**. Esto garantiza que la mayoría de los eventos positivos (fallos) sean detectados. ¡Has salvado la nave de un posible apagón catastrófico!",
            "incorrect": "Decisión peligrosa. En este escenario, minimizar los **Falsos Negativos (FN)** es la prioridad absoluta. La **Sensibilidad** es la métrica que nos asegura detectar todos los fallos reales. La Precisión se enfoca en no tener Falsos Positivos, lo cual es importante, pero no en el coste de un fallo real no detectado."
        },
        "decisions": 1
    },
    4: {
        "title": "Misión Finalizada: Retorno a Casa",
        "story": "Has demostrado un dominio excepcional en la aplicación de conceptos de IA bajo presión. El Proyecto Alpha es un éxito rotundo gracias a tus decisiones de arquitectura y optimización. ¡La tripulación regresa a salvo a casa y eres aclamado como un héroe de la IA!",
        "concept_name": "",
        "concept_key": "",
        "options": {},
        "answer": "",
        "feedback": {"correct": "", "incorrect": ""},
        "decisions": 0
    }
}

# --- SISTEMA DE LOGROS ---
ACHIEVEMENTS = {
    "first_blood": {"name": "Primera Sangre", "desc": "Completaste tu primera misión", "unlocked": False},
    "perfectionist": {"name": "Perfeccionista", "desc": "Respondiste todas las preguntas correctamente", "unlocked": False},
    "speed_runner": {"name": "Velocista", "desc": "Completaste el juego en menos de 5 minutos", "unlocked": False},
    "ia_master": {"name": "Maestro de IA", "desc": "Dominaste todos los conceptos clave", "unlocked": False},
}

# Calcular el puntaje máximo
GAME_STATE["max_score"] = sum(mission.get("decisions", 0) for mission in MISSIONS.values())

class AITextAdventure(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El Enigma del Proyecto 'Alpha' - Edición Mejorada")
        self.geometry("1100x800")
        self.configure(bg=COLORS["bg_primary"])
        
        # Fuentes mejoradas
        self.font_title = ('Orbitron', 24, 'bold')
        self.font_header = ('Roboto Mono', 16, 'bold')
        self.font_story = ('Roboto Mono', 12, 'normal')
        self.font_button_title = ('Roboto Mono', 11, 'bold')
        self.font_button_desc = ('Roboto Mono', 9, 'normal')
        self.font_feedback = ('Roboto Mono', 11, 'italic')
        self.font_stats = ('Roboto Mono', 10, 'normal')

        self.story_text_var = tk.StringVar()
        self.progress_text_var = tk.StringVar()
        self.feedback_text_var = tk.StringVar()
        self.stats_text_var = tk.StringVar()
        
        self.after_id = None
        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        """Crea la interfaz mejorada con más elementos visuales."""
        main_frame = tk.Frame(self, bg=COLORS["bg_primary"], padx=25, pady=25)
        main_frame.pack(pady=15, padx=15, fill="both", expand=True)

        # Header con título y estadísticas
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        header_frame.pack(fill="x", pady=(0, 15))

        # Título
        title_label = tk.Label(header_frame, text="🚀 EL ENIGMA DEL PROYECTO 'ALPHA'", 
                              font=self.font_title, bg=COLORS["bg_primary"], fg=COLORS["primary_glow"])
        title_label.pack(side="left")

        # Estadísticas en tiempo real
        self.stats_label = tk.Label(header_frame, textvariable=self.stats_text_var, 
                                   font=self.font_stats, bg=COLORS["bg_primary"], fg=COLORS["secondary_glow"])
        self.stats_label.pack(side="right")

        # Barra de progreso
        self.progress_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        self.progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_label = tk.Label(self.progress_frame, textvariable=self.progress_text_var, 
                                      font=self.font_header, bg=COLORS["bg_primary"], fg=COLORS["secondary_glow"])
        self.progress_label.pack(pady=(0, 5))

        # Barra de progreso visual
        self.progress_canvas = tk.Canvas(self.progress_frame, width=800, height=12, bg=COLORS["progress_bg"], highlightthickness=0)
        self.progress_canvas.pack(pady=5)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 12, fill=COLORS["progress_fill"], outline="")

        # Área de Historia
        story_frame = tk.Frame(main_frame, bg=COLORS["bg_secondary"], padx=20, pady=20, relief=tk.FLAT, bd=1)
        story_frame.pack(fill="x", pady=10)
        
        self.story_label = tk.Label(story_frame, textvariable=self.story_text_var, wraplength=950, justify=tk.LEFT, 
                                    font=self.font_story, bg=COLORS["bg_secondary"], fg=COLORS["text_white"])
        self.story_label.pack(fill='x')

        # Área de Feedback
        feedback_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        feedback_frame.pack(fill="x", pady=10)
        
        self.feedback_label = tk.Label(feedback_frame, textvariable=self.feedback_text_var, wraplength=950, justify=tk.LEFT, 
                                      font=self.font_feedback, bg=COLORS["bg_primary"], fg=COLORS["primary_glow"])
        self.feedback_label.pack(fill='x')

        # Área de Opciones
        self.options_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        self.options_frame.pack(pady=20, fill="both", expand=True)
        
        # Configurar grid responsive
        for i in range(3):
            self.options_frame.grid_columnconfigure(i, weight=1)

        # Botón de control
        self.control_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        self.control_frame.pack(fill="x", pady=10)
        
        self.next_button = tk.Button(self.control_frame, text="Iniciar Misión", command=self.process_choice, 
                                    bg=COLORS["primary_glow"], fg=COLORS["bg_primary"], font=self.font_button_title, 
                                    relief=tk.FLAT, bd=0, padx=25, pady=12, 
                                    activebackground=COLORS["primary_glow"], activeforeground=COLORS["bg_primary"])
        self.next_button.pack(pady=10)

        # Botón de skip para teletipo
        self.skip_button = tk.Button(self.control_frame, text="⏩ Saltar Animación", 
                                    command=self.skip_animation, bg=COLORS["bg_secondary"], 
                                    fg=COLORS["text_white"], font=('Roboto Mono', 9),
                                    relief=tk.FLAT, padx=10, pady=5)
        self.skip_button.pack()
        self.skip_button.pack_forget()

    def skip_animation(self):
        """Salta la animación de teletipo."""
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.story_text_var.set(GAME_STATE["story_full_text"])
        self.skip_button.pack_forget()

    def update_stats(self):
        """Actualiza las estadísticas en tiempo real."""
        accuracy = (GAME_STATE["correct_answers"] / GAME_STATE["total_answers"] * 100) if GAME_STATE["total_answers"] > 0 else 0
        elapsed_time = time.time() - GAME_STATE["start_time"]
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        stats_text = f"Puntuación: {GAME_STATE['score']}/{GAME_STATE['max_score']} | Precisión: {accuracy:.1f}% | Tiempo: {minutes:02d}:{seconds:02d}"
        self.stats_text_var.set(stats_text)

    def update_progress_bar(self):
        """Actualiza la barra de progreso visual."""
        progress = (GAME_STATE["mission"] - 1) / len(MISSIONS)
        self.progress_canvas.coords(self.progress_bar, 0, 0, 800 * progress, 12)

    def type_story_effect(self):
        """Efecto de escritura con mejor control."""
        full_text = GAME_STATE["story_full_text"]
        if GAME_STATE["current_story_idx"] < len(full_text):
            current_text = full_text[:GAME_STATE["current_story_idx"] + 1]
            self.story_text_var.set(current_text)
            GAME_STATE["current_story_idx"] += 1
            self.after_id = self.after(25, self.type_story_effect)
        else:
            self.after_id = None
            self.skip_button.pack_forget()

    def start_game(self):
        """Inicializa el juego con mejor feedback."""
        if self.after_id:
            self.after_cancel(self.after_id)
        
        GAME_STATE.update({
            "mission": 0,
            "score": 0,
            "correct_answers": 0,
            "total_answers": 0,
            "concept_mastery": {},
            "achievements": [],
            "start_time": time.time(),
            "current_story_idx": 0,
        })

        self.progress_text_var.set("ESTADO: INICIANDO SECUENCIA CRÍTICA")
        self.next_button.config(text="Iniciar Misión", command=lambda: self.next_mission())
        
        intro_text = (
            "Bienvenido, Comandante. \n\n"
            "El destino del Proyecto Alpha y la tripulación depende de tu conocimiento en Inteligencia Artificial. "
            "Cada decisión es una elección de diseño, arquitectura o métrica. "
            "No hay tiempo para fallos, solo para la **aplicación experta** de conceptos.\n\n"
            "🎯 OBJETIVO: Dominar los conceptos clave de IA a través de decisiones críticas.\n"
            "📊 SISTEMA: Tu progreso y precisión serán monitoreados en tiempo real."
        )
        
        GAME_STATE["story_full_text"] = intro_text
        self.story_text_var.set("")
        self.skip_button.pack()
        self.type_story_effect()
        
        self.feedback_text_var.set("Preparando sistemas de aprendizaje...")
        self.clear_options()
        self.update_stats()
        self.update_progress_bar()

    def clear_options(self):
        """Limpia las opciones de manera más eficiente."""
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def next_mission(self):
        """Avanza a la siguiente misión con mejor transición."""
        if self.after_id:
            self.after_cancel(self.after_id)
        GAME_STATE["mission"] += 1
        self.load_mission(GAME_STATE["mission"])

    def load_mission(self, mission_id):
        """Carga la misión con mejor presentación."""
        if mission_id > len(MISSIONS):
            self.show_results()
            return
            
        mission_data = MISSIONS[mission_id]
        self.clear_options()
        self.next_button.pack_forget()
        self.skip_button.pack_forget()

        self.progress_text_var.set(f"MISIÓN {mission_id}: {mission_data['title']}")
        self.update_progress_bar()

        # Preparar historia con efecto teletipo
        full_story = f"🔍 CONCEPTO: {mission_data['concept_name']}\n\n{mission_data['story']}"
        GAME_STATE["story_full_text"] = full_story
        GAME_STATE["current_story_idx"] = 0
        self.story_text_var.set("")
        self.skip_button.pack()
        self.type_story_effect()
        
        self.feedback_text_var.set("Analiza las opciones y elige la estrategia óptima...")

        # Crear botones de opción mejorados
        options = list(mission_data["options"].items())
        random.shuffle(options)
        
        for i, (choice_key, choice_description) in enumerate(options):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(self.options_frame, bg=COLORS["option_bg"], bd=1, relief=tk.RAISED)
            btn_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            btn_frame.grid_columnconfigure(0, weight=1)

            # Título de la opción
            title_label = tk.Label(btn_frame, text=choice_key, font=self.font_button_title, 
                                 bg=COLORS["option_bg"], fg=COLORS["primary_glow"], pady=8)
            title_label.grid(row=0, column=0, sticky="ew", padx=10)

            # Descripción
            desc_label = tk.Label(btn_frame, text=choice_description, font=self.font_button_desc, 
                                bg=COLORS["option_bg"], fg=COLORS["text_dark_accent"], 
                                wraplength=400, justify=tk.LEFT, padx=10, pady=8)
            desc_label.grid(row=1, column=0, sticky="ew")

            # Hacer todo clickeable
            for widget in [btn_frame, title_label, desc_label]:
                widget.bind("<Button-1>", lambda e, key=choice_key: self.process_choice(key))
                widget.bind("<Enter>", lambda e, b=btn_frame: b.config(bg=COLORS["bg_secondary"]))
                widget.bind("<Leave>", lambda e, b=btn_frame: b.config(bg=COLORS["option_bg"]))

    def process_choice(self, user_choice=None):
        """Procesa la elección con mejor feedback educativo."""
        if GAME_STATE["mission"] == 0:
            self.next_mission()
            return

        if self.after_id:
            self.after_cancel(self.after_id)

        mission_data = MISSIONS[GAME_STATE["mission"]]
        GAME_STATE["total_answers"] += 1

        correct_answer_full = mission_data["answer"]
        user_choice_concept = user_choice.split(" (")[0]
        correct_answer_concept = correct_answer_full.split(" (")[0]
        
        is_correct = user_choice_concept == correct_answer_concept

        self.clear_options()
        self.next_button.pack(pady=10)
        self.skip_button.pack_forget()

        # Actualizar mastery de conceptos
        concept_key = mission_data.get("concept_key", "")
        if concept_key:
            GAME_STATE["concept_mastery"][concept_key] = is_correct

        if is_correct:
            GAME_STATE["score"] += 1
            GAME_STATE["correct_answers"] += 1
            feedback_symbol = "🎯 DECISIÓN ÓPTIMA"
            feedback_color = COLORS["success_green"]
            feedback_message = mission_data["feedback"]["correct"]
            
            # Logro por primera respuesta correcta
            if GAME_STATE["correct_answers"] == 1 and "first_blood" not in GAME_STATE["achievements"]:
                GAME_STATE["achievements"].append("first_blood")
                self.show_achievement("first_blood")
                
        else:
            feedback_symbol = "⚠️ DECISIÓN DE RIESGO"
            feedback_color = COLORS["error_red"]
            feedback_message = f"{mission_data['feedback']['incorrect']}\n\n💡 La elección correcta era: **{correct_answer_full}**"

        # Feedback mejorado
        full_feedback_display = (
            f"=== ANÁLISIS DE LA DECISIÓN ===\n"
            f"Tu elección: {user_choice}\n"
            f"Resultado: {feedback_symbol}\n\n"
            f"{feedback_message}"
        )
        
        self.feedback_text_var.set(full_feedback_display)
        self.next_button.config(
            text=f"Continuar a Misión {GAME_STATE['mission'] + 1}" if GAME_STATE["mission"] < len(MISSIONS) - 1 else "Ver Resultados Finales",
            command=self.next_mission,
            bg=feedback_color
        )

        self.update_stats()

    def show_achievement(self, achievement_key):
        """Muestra un logro desbloqueado."""
        achievement = ACHIEVEMENTS[achievement_key]
        messagebox.showinfo(
            "🎉 LOGRO DESBLOQUEADO", 
            f"{achievement['name']}\n\n{achievement['desc']}"
        )

    def show_results(self):
        """Muestra resultados finales mejorados."""
        if self.after_id:
            self.after_cancel(self.after_id)
            
        self.clear_options()
        self.next_button.pack_forget()
        self.skip_button.pack_forget()

        total_points = GAME_STATE["max_score"]
        percentage = (GAME_STATE["score"] / total_points) * 100 if total_points > 0 else 0
        accuracy = (GAME_STATE["correct_answers"] / GAME_STATE["total_answers"] * 100) if GAME_STATE["total_answers"] > 0 else 0
        elapsed_time = time.time() - GAME_STATE["start_time"]

        self.progress_text_var.set("MISIÓN CUMPLIDA: REPORTE FINAL")
        self.update_progress_bar()

        # Verificar logros
        if percentage == 100 and "perfectionist" not in GAME_STATE["achievements"]:
            GAME_STATE["achievements"].append("perfectionist")
            self.show_achievement("perfectionist")
            
        if elapsed_time < 300 and "speed_runner" not in GAME_STATE["achievements"]:  # 5 minutos
            GAME_STATE["achievements"].append("speed_runner")
            self.show_achievement("speed_runner")

        # Historia final
        final_story = MISSIONS[4]["story"]
        GAME_STATE["story_full_text"] = final_story
        GAME_STATE["current_story_idx"] = 0
        self.story_text_var.set("")
        self.type_story_effect()

        # Resultados detallados
        if percentage >= 90:
            message_result = "🏆 MAESTRÍA LEGENDARIA! Dominas completamente los conceptos de IA aplicada."
            color_result = COLORS["primary_glow"]
        elif percentage >= 70:
            message_result = "⭐ COMANDANTE EXPERTO! Buen dominio con áreas de mejora específicas."
            color_result = COLORS["secondary_glow"]
        else:
            message_result = "📚 APRENDIZ ENTRENAMIENTO! Revisa los conceptos y vuelve a intentarlo."
            color_result = COLORS["error_red"]

        results_text = (
            f"📊 INFORME DE DESEMPEÑO FINAL\n\n"
            f"• Puntuación: {GAME_STATE['score']}/{total_points} ({percentage:.1f}%)\n"
            f"• Precisión General: {accuracy:.1f}%\n"
            f"• Tiempo Total: {int(elapsed_time//60)}m {int(elapsed_time%60)}s\n"
            f"• Logros Desbloqueados: {len(GAME_STATE['achievements'])}\n\n"
            f"{message_result}"
        )
        
        self.feedback_text_var.set(results_text)

        # Botones finales
        button_frame = tk.Frame(self.control_frame, bg=COLORS["bg_primary"])
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="🔄 Reiniciar Misión", command=self.restart_app,
                 bg=COLORS["primary_glow"], fg=COLORS["bg_primary"], font=self.font_button_title,
                 padx=20, pady=10).pack(side="left", padx=10)

        tk.Button(button_frame, text="📊 Ver Estadísticas", command=self.show_detailed_stats,
                 bg=COLORS["secondary_glow"], fg=COLORS["bg_primary"], font=self.font_button_title,
                 padx=20, pady=10).pack(side="left", padx=10)

    def show_detailed_stats(self):
        """Muestra estadísticas detalladas."""
        concepts_learned = sum(1 for mastered in GAME_STATE["concept_mastery"].values() if mastered)
        total_concepts = len(GAME_STATE["concept_mastery"])
        
        stats_message = (
            "📈 ESTADÍSTICAS DETALLADAS\n\n"
            f"• Conceptos Dominados: {concepts_learned}/{total_concepts}\n"
            f"• Tasa de Aciertos: {GAME_STATE['correct_answers']}/{GAME_STATE['total_answers']}\n"
            f"• Eficiencia de Tiempo: {(GAME_STATE['correct_answers']/GAME_STATE['total_answers']*100):.1f}%\n"
            f"• Logros: {', '.join([ACHIEVEMENTS[a]['name'] for a in GAME_STATE['achievements']]) or 'Ninguno'}"
        )
        
        messagebox.showinfo("Análisis de Desempeño", stats_message)

    def restart_app(self):
        """Reinicia la aplicación."""
        if self.after_id:
            self.after_cancel(self.after_id)
        self.destroy()
        AITextAdventure().mainloop()

if __name__ == "__main__":
    try:
        app = AITextAdventure()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar: {str(e)}")