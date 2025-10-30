"""
Missions Module - Proyecto Alpha v4.0
Definición de misiones educativas y contenido pedagógico.
"""

from typing import Dict, Any, List

# =============================================================================
# DATA: ESTRUCTURA MODULAR DE MISIONES (Extraído Exhaustivamente del PDF)
# =============================================================================

MISSIONS: Dict[int, Dict[str, Any]] = {
    # --- FASES DE LA IA ---
    1: {
        "title": "Misión 1: ¡La Máquina que Aprende! (ML)",
        "story": "Imagina que tienes una máquina que mira muchos ejemplos del pasado para adivinar qué pasará después. Por ejemplo, mira fotos de perros y gatos para saber cuál es cuál. ¿Qué tipo de Inteligencia Artificial usa datos del pasado para aprender y hacer predicciones?",
        "concept_name": "La IA que aprende de ejemplos",
        "options": {
            "Aprendizaje Automático (Machine Learning)": "¡Es como cuando aprendes de tus errores! La máquina mira muchos ejemplos para aprender sola.",
            "Aprendizaje Profundo (Deep Learning)": "Es como el aprendizaje automático pero con capas más complicadas, como un cerebro gigante.",
            "IA Creadora (Generative AI)": "Esta IA crea cosas nuevas, como dibujos o historias, en lugar de aprender del pasado.",
        },
        "answer": "Aprendizaje Automático (Machine Learning)",
        "decisions": 1,
        "difficulty": "facil",
        "category": "fases_ia",
        "learning_objectives": ["Comprender ML básico", "Diferenciar tipos de IA"],
        "hints": ["Piensa en ejemplos del pasado", "No crea cosas nuevas"],
        "explanation": "El Machine Learning es la base de la IA moderna, permitiendo que las máquinas aprendan patrones de datos históricos."
    },
    2: {
        "title": "Misión 2: ¡El Cerebro de la Máquina! (DL)",
        "story": "Piensa en un cerebro gigante que mira miles de fotos para encontrar cosas muy pequeñas que los humanos no vemos. Como buscar un tesoro escondido en un montón de arena. ¿Qué tipo de IA usa muchas capas como un cerebro para entender cosas complicadas?",
        "concept_name": "La IA con cerebro de muchas capas",
        "options": {
            "Red Neuronal Simple": "Es como un cerebro pequeño, pero no puede ver cosas muy complicadas.",
            "Aprendizaje Profundo (Deep Learning)": "¡Es como un cerebro gigante con muchas capas! Puede ver patrones escondidos en fotos y datos grandes.",
            "Inteligencia Artificial General": "Es la IA en general, pero no es la que tiene capas como un cerebro.",
        },
        "answer": "Aprendizaje Profundo (Deep Learning)",
        "decisions": 1,
        "difficulty": "facil",
        "category": "fases_ia",
        "learning_objectives": ["Comprender Deep Learning", "Entender redes neuronales"],
        "hints": ["Muchas capas", "Como un cerebro gigante"],
        "explanation": "El Deep Learning utiliza redes neuronales profundas para procesar información compleja, inspirado en el cerebro humano."
    },
    3: {
        "title": "Misión 3: ¡La Máquina Creadora! (IA Gen)",
        "story": "Imagina que le pides a una máquina que dibuje un animal que nunca existió, o que escriba una historia completamente nueva. No copia nada, ¡lo inventa todo! ¿Qué tipo de IA crea cosas nuevas que parecen hechas por humanos?",
        "concept_name": "La IA que inventa cosas nuevas",
        "options": {
            "Aprendizaje Profundo (Deep Learning)": "Esta IA analiza y entiende cosas, pero no crea cosas nuevas.",
            "IA Creadora (Generative AI)": "¡Es como un artista mágico! Crea dibujos, historias y música nueva que parece hecha por personas.",
            "Aprendizaje Automático (Machine Learning)": "Esta IA aprende de ejemplos, pero no inventa cosas nuevas.",
        },
        "answer": "IA Creadora (Generative AI)",
        "decisions": 1,
        "difficulty": "facil",
        "category": "fases_ia",
        "learning_objectives": ["Comprender IA Generativa", "Diferenciar tipos de IA"],
        "hints": ["Crea cosas nuevas", "Como un artista"],
        "explanation": "La IA Generativa puede crear contenido original, desde imágenes hasta texto, aprendiendo patrones para generar nuevas creaciones."
    },

    # --- CLASIFICACIÓN Y TAXONOMÍA DE LA IA ---
    4: {
        "title": "Misión 4: ¡Reacción Rápida! (Reactiva)",
        "story": "Piensa en un robot guardián que ve un peligro y reacciona al instante, ¡sin pensar en peligros pasados! Solo mira lo que pasa ahora mismo. ¿Qué tipo de IA actúa solo con lo que ve en el momento, sin aprender del pasado?",
        "concept_name": "La IA que reacciona al instante",
        "options": {
            "IA con Memoria": "Esta IA recuerda cosas del pasado para tomar decisiones.",
            "IA Reactiva": "¡Es como un reflejo! Solo usa información del momento actual, sin recordar nada.",
            "IA Inteligente": "Esta IA puede pensar en lo que otros sienten, es muy avanzada.",
        },
        "answer": "IA Reactiva",
        "decisions": 1,
        "difficulty": "normal",
        "category": "clasificacion_ia",
        "learning_objectives": ["Comprender IA Reactiva", "Diferenciar tipos de IA"],
        "hints": ["Sin recordar el pasado", "Reacción instantánea"],
        "explanation": "La IA Reactiva responde únicamente a estímulos actuales, sin memoria histórica, similar a un reflejo automático."
    },
    5: {
        "title": "Misión 5: ¡El Auto que Recuerda un Poco! (Memoria Limitada)",
        "story": "Imagina un carrito que juega solo y recuerda lo que pasó en los últimos segundos para no chocar. Mira a los otros carros por un ratito y aprende. ¿Qué tipo de IA recuerda cosas por poco tiempo para tomar mejores decisiones?",
        "concept_name": "La IA que recuerda por un ratito",
        "options": {
            "IA Consciente": "Esta IA se conoce a sí misma, es muy avanzada.",
            "IA con Memoria Limitada": "¡Recuerda cosas por poco tiempo! Como cuando miras atrás para cruzar la calle.",
            "IA con Teoría de la Mente": "Esta IA entiende lo que piensan otros, pero no es lo que necesitamos aquí.",
        },
        "answer": "IA con Memoria Limitada",
        "decisions": 1,
        "difficulty": "normal",
        "category": "clasificacion_ia",
        "learning_objectives": ["Comprender memoria limitada", "Entender estado temporal"],
        "hints": ["Recuerda por poco tiempo", "Como mirar atrás"],
        "explanation": "La IA con memoria limitada mantiene información temporal corta para mejorar decisiones inmediatas."
    },
    6: {
        "title": "Misión 6: ¡El Doctor Robot! (Sistemas Expertos)",
        "story": "Piensa en un robot que sabe tanto como un doctor sobre una enfermedad. Usa reglas especiales para decidir qué hacer, como un libro de recetas médicas. ¿Qué tipo de IA copia el pensamiento de un experto humano usando reglas?",
        "concept_name": "La IA que imita a los expertos",
        "options": {
            "Entendimiento de Lenguaje": "Esta IA entiende lo que dices, pero no es como un doctor.",
            "Sistemas Expertos": "¡Es como un maestro robot! Copia cómo piensan los expertos usando reglas especiales.",
            "Visión por Computadora": "Esta IA mira fotos y videos, no piensa como un doctor.",
        },
        "answer": "Sistemas Expertos",
        "decisions": 1,
        "difficulty": "normal",
        "category": "clasificacion_ia",
        "learning_objectives": ["Comprender Sistemas Expertos", "Entender reglas expertas"],
        "hints": ["Reglas especiales", "Como un doctor robot"],
        "explanation": "Los Sistemas Expertos codifican el conocimiento de expertos humanos en reglas para resolver problemas específicos."
    },

    # --- TIPOS DE APRENDIZAJE DE ML ---
    7: {
        "title": "Misión 7: ¡Aprender con Ayuda! (Supervisado)",
        "story": "Quieres enseñar a una máquina a reconocer correos basura. Le das muchos ejemplos donde ya sabes cuáles son basura y cuáles no. ¿Qué tipo de aprendizaje usa ejemplos donde ya sabes las respuestas correctas?",
        "concept_name": "Aprender con respuestas ya sabidas",
        "options": {
            "Aprendizaje sin Ayuda": "La máquina busca patrones sola, sin saber las respuestas.",
            "Aprendizaje Supervisado": "¡Es como estudiar con un maestro! Tienes las respuestas correctas para aprender.",
            "Aprendizaje por Prueba y Error": "La máquina aprende probando cosas y recibiendo premios o castigos.",
        },
        "answer": "Aprendizaje Supervisado",
        "decisions": 1,
        "difficulty": "normal",
        "category": "tipos_aprendizaje",
        "learning_objectives": ["Comprender aprendizaje supervisado", "Diferenciar tipos de ML"],
        "hints": ["Respuestas correctas", "Como estudiar con maestro"],
        "explanation": "El aprendizaje supervisado utiliza datos etiquetados para entrenar modelos predictivos."
    },
    8: {
        "title": "Misión 8: ¡Descubrir Grupos Secretos! (No Supervisado)",
        "story": "Tienes muchos amigos y quieres agruparlos por cómo juegan. No sabes qué grupos hacer, ¡la máquina los descubre sola! ¿Qué tipo de aprendizaje deja que la máquina encuentre grupos escondidos sin decirle qué buscar?",
        "concept_name": "Descubrir patrones escondidos",
        "options": {
            "Aprendizaje No Supervisado": "¡Es como un detective! Encuentra grupos y patrones sin que le digas qué buscar.",
            "Aprendizaje Supervisado": "Necesita que le digas las respuestas correctas primero.",
            "Aprendizaje por Prueba y Error": "Necesita premios y castigos para aprender.",
        },
        "answer": "Aprendizaje No Supervisado",
        "decisions": 1,
        "difficulty": "normal",
        "category": "tipos_aprendizaje",
        "learning_objectives": ["Comprender aprendizaje no supervisado", "Entender clustering"],
        "hints": ["Sin respuestas correctas", "Descubre grupos sola"],
        "explanation": "El aprendizaje no supervisado encuentra patrones y estructuras ocultas en datos sin etiquetas previas."
    },
    9: {
        "title": "Misión 9: ¡Aprender Jugando! (Por Refuerzo)",
        "story": "Un robot juega en un laberinto nuevo. Cuando llega a la meta, ¡le dan una golosina! Cuando choca, ¡le quitan un punto! ¿Qué tipo de aprendizaje aprende probando cosas y recibiendo premios o castigos?",
        "concept_name": "Aprender con premios y castigos",
        "options": {
            "Aprendizaje Mezclado": "Es una mezcla de otros tipos de aprendizaje.",
            "Aprendizaje por Refuerzo": "¡Es como entrenar a un perrito! Aprende con premios y castigos del entorno.",
            "Aprendizaje Supervisado": "Necesita respuestas correctas desde el principio.",
        },
        "answer": "Aprendizaje por Refuerzo",
        "decisions": 1,
        "difficulty": "dificil",
        "category": "tipos_aprendizaje",
        "learning_objectives": ["Comprender reinforcement learning", "Entender recompensas"],
        "hints": ["Premios y castigos", "Como entrenar un perro"],
        "explanation": "El aprendizaje por refuerzo aprende mediante interacción con el entorno, maximizando recompensas acumuladas."
    },

    # --- MATRIZ DE CONFUSIÓN Y MÉTRICAS ---
    10: {
        "title": "Misión 10: ¡No Dejar Pasar Problemas! (Sensibilidad)",
        "story": "Un detector de humo está dejando pasar fuegos reales sin sonar la alarma. ¡Eso es peligroso! Necesitas una medida que cuente cuántos fuegos reales detecta, para que no se escape ninguno. ¿Qué métrica miras para asegurarte de que no falten alarmas importantes?",
        "concept_name": "Contar los aciertos importantes",
        "options": {
            "Precisión": "Mide si las alarmas que suenan son reales, no si faltan alarmas.",
            "Sensibilidad (Recall)": "¡Cuenta los fuegos que SÍ detecta! Alta sensibilidad significa que no se escapa casi ningún fuego real.",
            "Especificidad": "Cuenta las veces que NO hay fuego y no suena alarma.",
        },
        "answer": "Sensibilidad (Recall)",
        "decisions": 1,
        "difficulty": "dificil",
        "category": "metricas_ml",
        "learning_objectives": ["Comprender sensibilidad", "Entender matriz de confusión"],
        "hints": ["Cuenta fuegos detectados", "No dejar pasar problemas"],
        "explanation": "La sensibilidad mide la capacidad de detectar casos positivos verdaderos, crucial para problemas donde los falsos negativos son costosos."
    },
    11: {
        "title": "Misión 11: ¡Alarmas Falsas Molestas! (Precisión)",
        "story": "Un detector de humo suena por todo: humo de cigarro, vapor de ducha, ¡hasta por el polvo! La gente ya no le cree. Necesitas una medida que diga qué tan confiables son las alarmas cuando suenan. ¿Qué métrica miras para que las alarmas que suenen sean realmente importantes?",
        "concept_name": "Medir la confianza de las alarmas",
        "options": {
            "Sensibilidad (Recall)": "Cuenta si detecta todos los fuegos, no si las alarmas son confiables.",
            "Precisión": "¡Mide si las alarmas que suenan son REALES! Alta precisión significa menos alarmas falsas.",
            "Exactitud": "Cuenta todas las veces que acierta, sin importar cuáles.",
        },
        "answer": "Precisión",
        "decisions": 1,
        "difficulty": "dificil",
        "category": "metricas_ml",
        "learning_objectives": ["Comprender precisión", "Entender trade-offs"],
        "hints": ["Alarmas que suenan reales", "Confianza en las alarmas"],
        "explanation": "La precisión mide la proporción de predicciones positivas que son correctas, importante cuando los falsos positivos son problemáticos."
    },
    12: {
        "title": "Misión 12: ¡El Equilibrio Perfecto! (F-Score)",
        "story": "El capitán quiere una sola medida que combine lo mejor de dos mundos: detectar todos los problemas reales Y que las alarmas sean confiables. ¿Qué métrica mezcla la precisión y la sensibilidad en un número perfecto?",
        "concept_name": "Combinar dos medidas importantes",
        "options": {
            "Exactitud": "Cuenta todos los aciertos, pero no balancea las dos cosas importantes.",
            "F-Score (F1)": "¡Es como una nota promedio especial! Mezcla precisión y sensibilidad para un equilibrio perfecto.",
            "Especificidad": "Solo mira una parte, no el balance completo.",
        },
        "answer": "F-Score (F1)",
        "decisions": 1,
        "difficulty": "dificil",
        "category": "metricas_ml",
        "learning_objectives": ["Comprender F-Score", "Entender métricas balanceadas"],
        "hints": ["Mezcla precisión y sensibilidad", "Equilibrio perfecto"],
        "explanation": "El F-Score es la media armónica de precisión y sensibilidad, proporcionando una medida balanceada del rendimiento."
    },

    # --- ANÁLISIS DE DATOS Y ENCODERS ---
    13: {
        "title": "Misión 13: ¡Explorar el Tesoro de Datos! (EDA)",
        "story": "Acabas de encontrar un baúl lleno de información. Antes de usar cualquier herramienta especial, necesitas curiosear: mirar qué hay, dibujar gráficos y entender qué significa todo. ¿Qué fase del análisis de datos haces primero para conocer tus datos como un explorador?",
        "concept_name": "Mirar y entender los datos primero",
        "options": {
            "Análisis de Muchas Variables": "Es más complicado, mira muchas cosas a la vez.",
            "Análisis Exploratorio de Datos (EDA)": "¡Es como ser un detective de datos! Miras, dibujas y entiendes qué hay antes de usar herramientas complicadas.",
            "Análisis de Dos Variables": "Solo mira cómo se relacionan dos cosas.",
        },
        "answer": "Análisis Exploratorio de Datos (EDA)",
        "decisions": 1,
        "difficulty": "normal",
        "category": "analisis_datos",
        "learning_objectives": ["Comprender EDA", "Entender análisis inicial"],
        "hints": ["Primera fase", "Como un detective"],
        "explanation": "El EDA es el proceso inicial de explorar y entender los datos antes de aplicar técnicas estadísticas avanzadas."
    },
    14: {
        "title": "Misión 14: ¡Colores para Cada Tipo! (One-Hot Encoder)",
        "story": "Tienes caramelos de colores: rojo, azul y verde. No hay un orden (no es que rojo sea mejor que azul). ¿Qué herramienta convierte cada color en su propia banderita especial para que la máquina entienda?",
        "concept_name": "Convertir categorías sin orden",
        "options": {
            "Codificador Ordenado": "Es para cosas que tienen un orden, como tallas de zapatos.",
            "Codificador One-Hot": "¡Crea una banderita para cada color! Cada categoría tiene su propia columna especial.",
            "Codificador de Objetivo": "Usa el resultado final para codificar, no es para colores simples.",
        },
        "answer": "Codificador One-Hot",
        "decisions": 1,
        "difficulty": "normal",
        "category": "analisis_datos",
        "learning_objectives": ["Comprender One-Hot Encoding", "Entender variables categóricas"],
        "hints": ["Banderita para cada color", "Sin orden específico"],
        "explanation": "El One-Hot Encoding convierte variables categóricas en vectores binarios, donde cada categoría se representa con una columna separada."
    },
    15: {
        "title": "Misión 15: ¡Números con Orden! (Ordinal Encoder)",
        "story": "Tienes niveles de videojuego: Fácil, Normal, Difícil. El orden SÍ importa (Difícil es más que Fácil). ¿Qué herramienta convierte estas categorías en números que respetan el orden, como 1, 2, 3?",
        "concept_name": "Convertir categorías ordenadas",
        "options": {
            "Codificador de Etiquetas": "Convierte en números, pero no respeta el orden especial.",
            "Codificador Ordinal": "¡Respeta el orden! Convierte categorías ordenadas en números secuenciales.",
            "Codificador Binario": "Convierte cada categoría en código binario.",
        },
        "answer": "Codificador Ordinal",
        "decisions": 1,
        "difficulty": "normal",
        "category": "analisis_datos",
        "learning_objectives": ["Comprender Ordinal Encoding", "Entender variables ordinales"],
        "hints": ["Respeta el orden", "Números secuenciales"],
        "explanation": "El Ordinal Encoding asigna números enteros a categorías ordinales, preservando el orden inherente entre ellas."
    },

    # --- ALGORITMOS DE ML (Clasificación y Regresión) ---
    16: {
        "title": "Misión 16: ¡Sí o No? (Regresión Logística)",
        "story": "Quieres saber si un amigo te prestará su juguete favorito o no. Necesitas una herramienta que diga qué tan probable es que diga 'sí' (como 70% seguro) y luego decida. ¿Qué algoritmo calcula probabilidades para decidir entre dos opciones?",
        "concept_name": "Calcular probabilidades para decidir",
        "options": {
            "Regresión Lineal": "Predice números continuos, como cuánto mide algo.",
            "Vecinos Más Cercanos (KNN)": "Decide por cercanía, no por probabilidad.",
            "Regresión Logística": "¡Calcula qué tan probable es cada opción! Perfecto para decidir entre sí o no.",
        },
        "answer": "Regresión Logística",
        "decisions": 1,
        "difficulty": "dificil",
        "category": "algoritmos_ml",
        "learning_objectives": ["Comprender Regresión Logística", "Entender clasificación binaria"],
        "hints": ["Calcula probabilidades", "Para decidir sí o no"],
        "explanation": "La Regresión Logística es un algoritmo de clasificación que estima probabilidades de pertenencia a clases binarias."
    },
    17: {
        "title": "Misión 17: ¡Elegir lo Importante! (Lasso)",
        "story": "Tienes cien juguetes pero solo unos pocos son realmente útiles para jugar. Necesitas una herramienta que automáticamente esconda los juguetes que no sirven, dejándolos exactamente en cero. ¿Qué tipo de regresión elige sola cuáles variables son importantes?",
        "concept_name": "Elegir variables automáticamente",
        "options": {
            "Regresión Lineal Simple": "No elige ni esconde variables.",
            "Regresión Ridge (L2)": "Reduce las variables grandes pero no las esconde completamente.",
            "Regresión Lasso (L1)": "¡Esconde las variables inútiles poniéndolas en cero! Selecciona automáticamente lo importante.",
        },
        "answer": "Regresión Lasso (L1)",
        "decisions": 1,
        "difficulty": "experto",
        "category": "algoritmos_ml",
        "learning_objectives": ["Comprender Regularización L1", "Entender selección de features"],
        "hints": ["Esconde variables en cero", "Selecciona automáticamente"],
        "explanation": "La regularización Lasso (L1) puede forzar coeficientes a cero, realizando selección automática de características."
    },
    18: {
        "title": "Misión 18: ¡Calmar las Variables Rebeldes! (Ridge)",
        "story": "Tus variables están peleando entre ellas porque dicen lo mismo de diferentes maneras. Esto hace que las predicciones sean inestables. Necesitas una herramienta que calme a las variables más fuertes para que todas trabajen en equipo. ¿Qué regresión reduce las variables grandes sin eliminarlas?",
        "concept_name": "Reducir variables conflictivas",
        "options": {
            "Regresión Lasso (L1)": "Elimina variables completamente, no las calma.",
            "Regresión Ridge (L2)": "¡Calma las variables grandes reduciéndolas! Perfecto cuando las variables se confunden entre sí.",
            "Máquina de Vectores de Soporte (SVM)": "Separa grupos con líneas, no reduce coeficientes.",
        },
        "answer": "Regresión Ridge (L2)",
        "decisions": 1,
        "difficulty": "experto",
        "category": "algoritmos_ml",
        "learning_objectives": ["Comprender Regularización L2", "Entender multicolinealidad"],
        "hints": ["Reduce sin eliminar", "Calma variables grandes"],
        "explanation": "La regularización Ridge (L2) reduce la magnitud de los coeficientes sin eliminarlos, ayudando con multicolinealidad."
    },

    # --- METODOLOGÍAS Y PRINCIPIOS DE PROYECTOS ---
    19: {
        "title": "Misión 19: ¡Construir Paso a Paso! (Agile)",
        "story": "Tu amigo quiere un castillo de arena, pero cambia de idea todo el tiempo: más torres, menos foso, colores diferentes. Necesitas una forma de trabajar que entregue partes terminadas rápido y se adapte a los cambios. ¿Qué metodología construye poco a poco y se ajusta cuando cambian las ideas?",
        "concept_name": "Trabajar con cambios constantes",
        "options": {
            "Cascada (Waterfall)": "Hace todo en orden fijo, no se puede cambiar una vez empezado.",
            "Método de Ruta Crítica (CPM)": "Planifica tiempos, pero no es flexible.",
            "Agile": "¡Construye en pedacitos y se adapta! Entrega valor rápido y cambia cuando sea necesario.",
        },
        "answer": "Agile",
        "decisions": 1,
        "difficulty": "normal",
        "category": "metodologias",
        "learning_objectives": ["Comprender metodología Agile", "Entender desarrollo iterativo"],
        "hints": ["Se adapta a cambios", "Entrega partes terminadas"],
        "explanation": "Agile es una metodología de desarrollo iterativa e incremental que permite adaptarse a cambios durante el proyecto."
    },
    20: {
        "title": "Misión 20: ¡Lo Simple es Mejor! (Parsimonia)",
        "story": "Tienes dos formas de explicar por qué el cielo es azul: una simple dice 'porque la luz se dispersa' y otra complicada habla de fórmulas matemáticas raras. ¿Qué principio dice que siempre elijas la explicación más simple que funcione?",
        "concept_name": "Elegir lo simple sobre lo complicado",
        "options": {
            "Escalabilidad": "Que algo pueda crecer grande sin romperse.",
            "Principio de Parsimonia (Navaja de Occam)": "¡La explicación más simple es la mejor! No agregues complicaciones innecesarias.",
            "Interoperabilidad": "Que diferentes cosas puedan trabajar juntas.",
        },
        "answer": "Principio de Parsimonia (Navaja de Occam)",
        "decisions": 1,
        "difficulty": "normal",
        "category": "metodologias",
        "learning_objectives": ["Comprender principio de parsimonia", "Entender simplicidad"],
        "hints": ["Explicación más simple", "No complicaciones innecesarias"],
        "explanation": "El principio de parsimonia (Navaja de Occam) establece que la explicación más simple suele ser la mejor."
    },

    # --- RESULTADO FINAL ---
    21: {
        "title": "Misión Finalizada: Retorno a Casa",
        "story": "¡Has completado las **20 misiones críticas**! Has demostrado un dominio conceptual amplio y profundo de todo el material de repaso. El Proyecto Alpha es un éxito. Prepárate para el reporte final.",
        "concept_name": "Evaluación completada",
        "options": {
            "Finalizar Evaluación": "Completar la evaluación académica y ver resultados finales."
        },
        "answer": "Finalizar Evaluación",
        "decisions": 0,
        "difficulty": "final",
        "category": "final",
        "learning_objectives": ["Consolidar aprendizaje", "Evaluar comprensión"],
        "hints": ["Esta es la misión final - ¡has completado todo!"],
        "explanation": "Evaluación completada exitosamente."
    }
}

def get_missions_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Obtiene misiones filtradas por categoría.

    Args:
        category: Categoría de las misiones

    Returns:
        Lista de misiones de la categoría especificada
    """
    return [mission for mission in MISSIONS.values() if mission.get("category") == category]

def get_missions_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """
    Obtiene misiones filtradas por dificultad.

    Args:
        difficulty: Nivel de dificultad

    Returns:
        Lista de misiones del nivel especificado
    """
    return [mission for mission in MISSIONS.values() if mission.get("difficulty") == difficulty]

def get_total_missions() -> int:
    """
    Obtiene el número total de misiones disponibles.

    Returns:
        Número total de misiones
    """
    return len(MISSIONS)

def get_mission_ids() -> List[int]:
    """
    Obtiene lista de IDs de todas las misiones.

    Returns:
        Lista ordenada de IDs de misiones
    """
    return sorted(MISSIONS.keys())

def validate_missions() -> bool:
    """
    Valida que todas las misiones tengan la estructura correcta.

    Returns:
        True si todas las misiones son válidas
    """
    required_fields = ["title", "story", "concept_name", "options", "answer", "decisions"]

    for mission_id, mission in MISSIONS.items():
        for field in required_fields:
            if field not in mission:
                print(f"Misión {mission_id} falta campo requerido: {field}")
                return False

        # Validar que la respuesta esté en las opciones
        if mission["answer"] not in mission["options"]:
            print(f"Misión {mission_id}: respuesta '{mission['answer']}' no está en opciones")
            return False

    return True