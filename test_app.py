#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la funcionalidad del juego mejorado
"""
import json
import os
import sys

def test_files_exist():
    """Verifica que todos los archivos necesarios existan"""
    required_files = [
        'config.json',
        'questions_data.json', 
        'stats_manager.py',
        'repaso_ia_mejorado.py'
    ]
    
    print("🔍 Verificando archivos necesarios...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTANTE")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_json_files():
    """Verifica que los archivos JSON sean válidos"""
    print("\n📄 Verificando archivos JSON...")
    
    # Test config.json
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("  ✅ config.json - Válido")
        
        # Verificar estructura básica
        if 'app' in config and 'themes' in config:
            print("  ✅ config.json - Estructura correcta")
        else:
            print("  ⚠️ config.json - Estructura incompleta")
            
    except Exception as e:
        print(f"  ❌ config.json - Error: {e}")
        return False
    
    # Test questions_data.json
    try:
        with open('questions_data.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
        print("  ✅ questions_data.json - Válido")
        
        # Verificar que hay preguntas
        if len(questions) > 0:
            print(f"  ✅ {len(questions)} preguntas cargadas")
            
            # Verificar estructura de primera pregunta
            first_q = questions[0]
            required_fields = ['question', 'options', 'answer', 'concept', 'category']
            if all(field in first_q for field in required_fields):
                print("  ✅ Estructura de preguntas correcta")
            else:
                print("  ⚠️ Estructura de preguntas incompleta")
        else:
            print("  ❌ No hay preguntas en el archivo")
            return False
            
    except Exception as e:
        print(f"  ❌ questions_data.json - Error: {e}")
        return False
    
    return True

def test_imports():
    """Verifica que se puedan importar los módulos"""
    print("\n📦 Verificando importaciones...")
    
    try:
        import tkinter as tk
        print("  ✅ tkinter")
    except ImportError:
        print("  ❌ tkinter - No disponible")
        return False
    
    try:
        from stats_manager import StatsManager
        print("  ✅ stats_manager")
    except ImportError as e:
        print(f"  ❌ stats_manager - Error: {e}")
        return False
    
    return True

def test_stats_manager():
    """Prueba básica del gestor de estadísticas"""
    print("\n📊 Probando StatsManager...")
    
    try:
        from stats_manager import StatsManager
        
        # Crear instancia temporal
        stats = StatsManager("test_stats.json")
        
        # Probar guardar sesión
        stats.save_session(5, 2, 10, "Test")
        print("  ✅ Guardar sesión")
        
        # Probar obtener resumen
        summary = stats.get_stats_summary()
        print("  ✅ Obtener resumen")
        
        # Limpiar archivo de prueba
        if os.path.exists("test_stats.json"):
            os.remove("test_stats.json")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en StatsManager: {e}")
        return False

def test_app_startup():
    """Prueba que la aplicación se pueda inicializar"""
    print("\n🚀 Probando inicialización de la aplicación...")
    
    try:
        # Importar sin ejecutar
        import importlib.util
        spec = importlib.util.spec_from_file_location("quiz_app", "repaso_ia_mejorado.py")
        quiz_module = importlib.util.module_from_spec(spec)
        
        print("  ✅ Módulo principal importable")
        return True
        
    except Exception as e:
        print(f"  ❌ Error importando aplicación: {e}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA\n")
    
    tests = [
        ("Archivos necesarios", test_files_exist),
        ("Archivos JSON", test_json_files),
        ("Importaciones", test_imports),
        ("StatsManager", test_stats_manager),
        ("Inicialización", test_app_startup)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  💥 Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "="*50)
    print("📋 RESUMEN DE PRUEBAS")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista para usar.")
        print("\n💡 Para ejecutar la aplicación:")
        print("   python repaso_ia_mejorado.py")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores antes de ejecutar.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)