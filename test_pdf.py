#!/usr/bin/env python3
"""Test script for PDF extractor without requiring actual PDF file"""

import json
import os
from pdf_extractor import PDFExtractor

def create_mock_pdf_data():
    """Create mock data to simulate PDF extraction"""
    mock_data = [
        {
            "page": 1,
            "content": "Introducción a la Inteligencia Artificial\nLa IA es una rama de la informática que busca crear sistemas capaces de realizar tareas que requieren inteligencia humana.",
            "char_count": 150
        },
        {
            "page": 2, 
            "content": "Tipos de Inteligencia Artificial\n- IA Débil: Sistemas especializados\n- IA Fuerte: Sistemas con capacidades generales",
            "char_count": 120
        },
        {
            "page": 3,
            "content": "Machine Learning\nAprendizaje automático mediante algoritmos que mejoran con la experiencia.",
            "char_count": 95
        }
    ]
    return mock_data

def test_extractor_methods():
    """Test extractor methods with mock data"""
    print("🧪 Testing PDF Extractor Methods...")
    
    # Create extractor instance
    extractor = PDFExtractor("mock_file.pdf")
    
    # Set mock data
    extractor.extracted_text = create_mock_pdf_data()
    
    # Test statistics
    stats = extractor.get_statistics()
    print(f"✅ Statistics: {stats}")
    
    # Test question generation
    questions = extractor.generate_question_templates()
    print(f"✅ Generated {len(questions)} question templates")
    
    # Test file saving
    if extractor.save_text_to_file("test_output.txt"):
        print("✅ Text file saved successfully")
    
    if extractor.save_questions_template(questions, "test_questions.json"):
        print("✅ Questions template saved successfully")
    
    return True

def test_integration():
    """Test integration helper"""
    print("\n🔗 Testing Integration Helper...")
    
    from integration_helper import TriviaIntegrator
    
    integrator = TriviaIntegrator("questions_data.json", "test_questions.json")
    
    # Test loading
    existing = integrator.load_existing_questions()
    templates = integrator.load_extracted_templates()
    
    print(f"✅ Loaded {len(existing)} existing questions")
    print(f"✅ Loaded {len(templates)} templates")
    
    return True

def cleanup_test_files():
    """Clean up test files"""
    test_files = ["test_output.txt", "test_questions.json", "merged_questions.json", "pdf_extractor.log"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Cleaned up {file}")

if __name__ == "__main__":
    print("🚀 Starting PDF Extractor Tests\n")
    
    try:
        # Run tests
        test_extractor_methods()
        test_integration()
        
        print("\n✅ All tests passed successfully!")
        print("📋 Test files created - check the output")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up test files...")
        cleanup_test_files()
        print("✨ Tests completed!")