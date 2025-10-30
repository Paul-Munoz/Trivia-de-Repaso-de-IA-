#!/usr/bin/env python3
"""
Proyecto Alpha v4.0 - Sistema Educativo de IA Avanzada
Archivo principal de entrada a la aplicación.
"""

import sys
import traceback

# Importar módulos refactorizados
from repaso_ia_refactored import main as run_application

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Manejador global de excepciones no capturadas."""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Excepción crítica no manejada:\n{error_msg}")

    # Intentar mostrar mensaje al usuario si tkinter está disponible
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error Crítico del Sistema",
                            f"Se ha producido un error crítico:\n\n{str(exc_value)}\n\n"
                            "La aplicación se cerrará. Por favor, contacte al soporte técnico.")
        root.destroy()
    except:
        print("No se pudo mostrar mensaje de error al usuario.")

    sys.exit(1)

if __name__ == "__main__":
    # Configurar manejo de excepciones global
    sys.excepthook = global_exception_handler

    # Ejecutar la aplicación
    run_application()