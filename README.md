# 🎓 Trivia de Repaso de IA - Versión Mejorada

## 📋 Descripción
Aplicación educativa interactiva para repasar conceptos de Inteligencia Artificial, incluyendo fases, clasificación, matriz de confusión y métricas de evaluación.

## ✨ Nuevas Características

### 🏗️ Mejoras Estructurales
- **Arquitectura modular**: Separación de datos, configuración y lógica
- **Gestión de configuración**: Archivo JSON para temas y configuraciones
- **Base de datos de preguntas externa**: Fácil mantenimiento y actualización
- **Sistema de logging**: Registro de eventos y errores

### 🎨 Mejoras de Interfaz
- **Temas visuales**: Modo claro y oscuro
- **Diseño responsive**: Se adapta a diferentes tamaños de ventana
- **Barra de progreso visual**: Seguimiento del avance en tiempo real
- **Animaciones suaves**: Transiciones entre preguntas
- **Accesibilidad mejorada**: Soporte para teclado

### 📊 Funcionalidades Avanzadas
- **Sistema de categorías**: Filtrar preguntas por tema
- **Modo estudio**: Explicaciones detalladas después de cada respuesta
- **Estadísticas persistentes**: Historial de partidas y progreso
- **Validación de datos**: Verificación de integridad de preguntas
- **Manejo robusto de errores**: Recuperación automática de fallos

### 📈 Sistema de Estadísticas
- Historial completo de sesiones
- Estadísticas por categoría
- Seguimiento de progreso temporal
- Métricas de rendimiento detalladas

## 🚀 Instalación y Uso

### Requisitos
- Python 3.7+
- tkinter (incluido con Python)
- Módulos estándar: json, random, os, datetime, logging

### Ejecución
```bash
python repaso_ia_mejorado.py
```

## 📁 Estructura de Archivos

```
Examen_27_10_2025/
├── repaso_ia_mejorado.py      # Aplicación principal
├── config.json                # Configuración y temas
├── questions_data.json        # Base de datos de preguntas
├── stats_manager.py           # Gestión de estadísticas
├── game_stats.json           # Estadísticas guardadas (se crea automáticamente)
├── quiz_game.log             # Archivo de logs (se crea automáticamente)
└── README.md                 # Esta documentación
```

## 🎮 Cómo Usar

1. **Inicio**: Selecciona categoría y modo de estudio
2. **Quiz**: Responde las preguntas con feedback inmediato
3. **Resultados**: Revisa tu rendimiento y estadísticas
4. **Estadísticas**: Consulta tu progreso histórico

## 🔧 Configuración

### Temas
Edita `config.json` para personalizar colores y configuraciones:
- Tema claro/oscuro
- Tamaño de ventana
- Colores personalizados

### Preguntas
Añade o modifica preguntas en `questions_data.json`:
```json
{
  "question": "Tu pregunta aquí",
  "options": ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
  "answer": "Respuesta correcta",
  "concept": "Concepto relacionado",
  "formula": "Explicación detallada",
  "category": "Categoría"
}
```

## 🐛 Solución de Problemas

### Errores Comunes
1. **Archivo no encontrado**: Verifica que todos los archivos estén en el mismo directorio
2. **Error de permisos**: Asegúrate de tener permisos de escritura en el directorio
3. **Problemas de visualización**: Actualiza tu versión de Python/tkinter

### Logs
Consulta `quiz_game.log` para información detallada sobre errores.

## 📊 Categorías de Preguntas

- **Introducción y Fases**: Conceptos básicos y evolución de la IA
- **Clasificación**: Tipos y categorías de sistemas de IA
- **Matriz de Confusión**: Evaluación de modelos de clasificación
- **Métricas**: Medidas de rendimiento y evaluación

## 🔄 Actualizaciones Futuras

- [ ] Modo multijugador
- [ ] Exportación de estadísticas
- [ ] Más categorías de preguntas
- [ ] Integración con bases de datos externas
- [ ] Modo examen cronometrado

## 📝 Notas de Desarrollo

### Mejoras Implementadas
1. ✅ Separación de datos en archivos JSON
2. ✅ Sistema de temas claro/oscuro
3. ✅ Categorización de preguntas
4. ✅ Modo estudio con explicaciones
5. ✅ Estadísticas persistentes
6. ✅ Barra de progreso visual
7. ✅ Manejo robusto de errores
8. ✅ Sistema de logging
9. ✅ Validación de datos
10. ✅ Interfaz responsive

### Arquitectura
- **Patrón MVC**: Separación clara entre modelo, vista y controlador
- **Gestión de estado**: Variables centralizadas y consistentes
- **Modularidad**: Componentes independientes y reutilizables
- **Extensibilidad**: Fácil añadir nuevas funcionalidades

## 👨‍💻 Autor
Versión mejorada del juego original de repaso de conceptos de IA.
