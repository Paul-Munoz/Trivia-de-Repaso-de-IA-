"""
Configuration Module - Proyecto Alpha v4.0
Configuraciones globales y constantes del sistema educativo.
"""

from typing import Dict, Any

# =============================================================================
# CONFIGURACIÓN GLOBAL Y CONSTANTES
# =============================================================================

# --- PALETA DE COLORES MODERNA Y PROFESIONAL ---
COLORS: Dict[str, str] = {
    # Tema principal moderno y profesional
    "bg_primary": "#FFFFFF",       # Blanco puro para fondo principal
    "bg_secondary": "#F8F9FA",     # Gris muy claro para secciones
    "bg_accent": "#E9ECEF",        # Gris claro para acentos sutiles
    "bg_card": "#FFFFFF",          # Blanco para tarjetas/cards
    "bg_overlay": "rgba(0,0,0,0.05)", # Overlay sutil para capas

    # Colores principales - Modern Professional Palette
    "primary": "#2563EB",          # Azul moderno profesional
    "primary_light": "#3B82F6",    # Azul claro para hover
    "primary_dark": "#1D4ED8",     # Azul oscuro para elementos activos
    "secondary": "#64748B",        # Gris moderno para texto secundario
    "accent": "#F59E0B",           # Ámbar moderno para acentos

    # Estados y feedback
    "success": "#10B981",          # Verde moderno para éxito
    "success_light": "#D1FAE5",    # Verde muy claro para fondos de éxito
    "warning": "#F59E0B",          # Ámbar para advertencias
    "warning_light": "#FEF3C7",    # Ámbar muy claro para fondos
    "error": "#EF4444",            # Rojo moderno para errores
    "error_light": "#FEE2E2",      # Rojo muy claro para fondos

    # Texto y contenido
    "text_primary": "#1F2937",     # Gris oscuro casi negro para títulos
    "text_secondary": "#6B7280",   # Gris medio para texto secundario
    "text_muted": "#9CA3AF",       # Gris claro para texto muted
    "text_white": "#FFFFFF",       # Blanco para texto sobre colores oscuros

    # Bordes y sombras
    "border_light": "lightgray",     # Gris muy claro para bordes sutiles
    "border_medium": "gray",    # Gris medio para bordes
    "shadow_light": "rgba(0,0,0,0.1)", # Sombra sutil
    "shadow_medium": "rgba(0,0,0,0.15)", # Sombra media

    # Elementos específicos
    "progress_bg": "lightgray",      # Fondo de barras de progreso
    "progress_fill": "blue",    # Relleno de progreso
    "button_primary": "#2563EB",   # Botones principales
    "button_secondary": "#6B7280", # Botones secundarios
    "input_bg": "#FFFFFF",         # Fondo de inputs
    "input_border": "#D1D5DB",     # Bordes de inputs

    # Tema oscuro opcional
    "dark_bg_primary": "#111827",  # Fondo oscuro principal
    "dark_bg_secondary": "#1F2937", # Fondo oscuro secundario
    "dark_text_primary": "#F9FAFB", # Texto claro para oscuro
    "dark_text_secondary": "#D1D5DB", # Texto secundario oscuro

    # Gradientes modernos
    "gradient_primary": "linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)",
    "gradient_success": "linear-gradient(135deg, #10B981 0%, #34D399 100%)",
    "gradient_accent": "linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)",
}

# --- CONSTANTES DEL SISTEMA ---
SAVE_FILE: str = "alpha_progress_v3.json"
CONFIG_FILE: str = "alpha_config.json"
LOG_FILE: str = "alpha_session.log"

# --- CONSTANTES DE PROFESIONALIZACIÓN ---
PROFESSIONAL_CONFIG: Dict[str, Any] = {
    "auto_save_interval": 30,  # segundos
    "max_session_time": 3600,  # 1 hora
    "performance_tracking": True,
    "detailed_logging": True,
    "accessibility_mode": True,
    "high_contrast_support": True,
    "keyboard_navigation": True,
    "screen_reader_support": True,
    "error_reporting": True,
    "user_feedback_system": True
}

# --- CONFIGURACIÓN ACADÉMICA ---
ACADEMIC_CONFIG: Dict[str, Any] = {
    "max_missions": 25,
    "time_limit_per_question": 60,  # segundos
    "hint_penalty_factor": 0.15,    # penalización por pista
    "retry_penalty_factor": 0.10,   # penalización por reintento
    "streak_bonus_multiplier": 0.05, # bonus por racha
    "mastery_threshold": 0.85,      # umbral de maestría (85%)
    "adaptive_difficulty_levels": ["facil", "normal", "dificil", "experto"],
}

# --- CONFIGURACIÓN DE UI MODERNA ---
UI_CONFIG: Dict[str, Any] = {
    # Dimensiones de ventana
    "window_width": 1400,
    "window_height": 900,
    "min_window_width": 1200,
    "min_window_height": 800,

    # Tipografía moderna - Arial como fuente principal
    "font_family": "Arial",
    "font_title": ("Arial", 28, "bold"),        # Títulos principales
    "font_header": ("Arial", 20, "bold"),       # Headers de sección
    "font_subheader": ("Arial", 18, "bold"),    # Subtítulos
    "font_body": ("Arial", 16, "normal"),       # Texto principal
    "font_caption": ("Arial", 14, "normal"),    # Texto secundario
    "font_small": ("Arial", 12, "normal"),      # Texto pequeño
    "font_button": ("Arial", 14, "bold"),       # Botones
    "font_metrics": ("Arial", 13, "normal"),    # Métricas

    # Espaciado moderno
    "spacing_xs": 4,
    "spacing_sm": 8,
    "spacing_md": 16,
    "spacing_lg": 24,
    "spacing_xl": 32,
    "spacing_xxl": 48,

    # Bordes y radios modernos
    "border_radius_sm": 6,
    "border_radius_md": 8,
    "border_radius_lg": 12,
    "border_radius_xl": 16,
    "border_width": 1,

    # Sombras modernas
    "shadow_sm": "0 1px 2px rgba(0,0,0,0.05)",
    "shadow_md": "0 4px 6px rgba(0,0,0,0.07)",
    "shadow_lg": "0 10px 15px rgba(0,0,0,0.1)",
    "shadow_xl": "0 20px 25px rgba(0,0,0,0.15)",

    # Layout moderno
    "sidebar_width": 320,
    "header_height": 80,
    "card_padding": 24,
    "content_max_width": 800,

    # Animaciones sutiles
    "animation_duration_fast": 150,  # ms
    "animation_duration_normal": 300, # ms
    "animation_duration_slow": 500,   # ms
    "animation_easing": "cubic-bezier(0.4, 0, 0.2, 1)",

    # Tema responsive
    "breakpoint_mobile": 768,
    "breakpoint_tablet": 1024,
    "breakpoint_desktop": 1440,
}

# --- CONFIGURACIÓN DE GAMIFICACIÓN ---
GAMIFICATION_CONFIG: Dict[str, Any] = {
    "max_streak_bonus": 2.0,
    "time_bonus_multiplier": 0.1,
    "hint_penalty_multiplier": 0.8,
    "retry_penalty_multiplier": 0.9,
    "achievement_points_multiplier": 1.0,
    "progress_visualization": True,
    "sound_effects": False,  # Deshabilitado por accesibilidad
    "animations": True,
}

# --- CONFIGURACIÓN DE ACCESIBILIDAD ---
ACCESSIBILITY_CONFIG: Dict[str, Any] = {
    "high_contrast_mode": False,
    "large_text_mode": False,
    "keyboard_navigation": True,
    "screen_reader_optimized": True,
    "reduced_motion": False,
    "color_blind_friendly": True,
    "focus_indicators": True,
    "tab_navigation": True,
}

def get_color_scheme(high_contrast: bool = False) -> Dict[str, str]:
    """
    Obtiene el esquema de colores apropiado.

    Args:
        high_contrast: Si se debe usar modo alto contraste

    Returns:
        Diccionario con esquema de colores
    """
    if high_contrast:
        return {
            "bg_primary": "#000000",
            "bg_secondary": "#1A1A1A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#CCCCCC",
            "accent": "#FFFF00",
            "success": "#00FF00",
            "error": "#FF0000",
            "warning": "#FFA500",
        }
    else:
        return COLORS.copy()

def validate_config() -> bool:
    """
    Valida que todas las configuraciones críticas estén presentes.

    Returns:
        True si la configuración es válida
    """
    required_configs = [
        COLORS,
        PROFESSIONAL_CONFIG,
        ACADEMIC_CONFIG,
        UI_CONFIG
    ]

    for config in required_configs:
        if not isinstance(config, dict) or len(config) == 0:
            return False

    # Validar valores críticos
    if ACADEMIC_CONFIG.get("time_limit_per_question", 0) <= 0:
        return False

    if PROFESSIONAL_CONFIG.get("auto_save_interval", 0) < 0:
        return False

    return True

def get_adaptive_settings(performance_level: str) -> Dict[str, Any]:
    """
    Obtiene configuraciones adaptativas basadas en el nivel de rendimiento.

    Args:
        performance_level: Nivel de rendimiento ("low", "medium", "high")

    Returns:
        Diccionario con configuraciones adaptativas
    """
    settings = {
        "low": {
            "hints_enabled": True,
            "time_limits": False,
            "detailed_feedback": True,
            "difficulty": "easy",
            "retry_limit": 3,
        },
        "medium": {
            "hints_enabled": True,
            "time_limits": True,
            "detailed_feedback": True,
            "difficulty": "normal",
            "retry_limit": 2,
        },
        "high": {
            "hints_enabled": False,
            "time_limits": True,
            "detailed_feedback": False,
            "difficulty": "hard",
            "retry_limit": 1,
        }
    }

    return settings.get(performance_level, settings["medium"])