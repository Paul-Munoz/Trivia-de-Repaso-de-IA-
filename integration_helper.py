import json
import logging
from datetime import datetime

class TriviaIntegrator:
    """Helper class to integrate PDF extracted content with trivia application"""
    
    def __init__(self, questions_file="questions_data.json", extracted_file="extracted_questions.json"):
        self.questions_file = questions_file
        self.extracted_file = extracted_file
        
    def load_existing_questions(self):
        """Load existing questions from trivia database"""
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.warning(f"Questions file {self.questions_file} not found")
            return []
        except Exception as e:
            logging.error(f"Error loading questions: {e}")
            return []
    
    def load_extracted_templates(self):
        """Load extracted question templates"""
        try:
            with open(self.extracted_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.warning(f"Extracted file {self.extracted_file} not found")
            return []
        except Exception as e:
            logging.error(f"Error loading extracted templates: {e}")
            return []
    
    def convert_template_to_question(self, template):
        """Convert extracted template to trivia question format"""
        return {
            "question": template.get("question", ""),
            "options": [
                "Opción A (completar)",
                "Opción B (completar)", 
                "Opción C (completar)",
                "Opción D (completar)"
            ],
            "answer": "Respuesta correcta (completar)",
            "concept": template.get("concept", ""),
            "formula": f"Extraído de página {template.get('source_page', 'N/A')}",
            "category": template.get("category", "Conceptos Generales")
        }
    
    def merge_questions(self):
        """Merge extracted templates with existing questions"""
        existing = self.load_existing_questions()
        templates = self.load_extracted_templates()
        
        new_questions = []
        for template in templates:
            question = self.convert_template_to_question(template)
            new_questions.append(question)
        
        # Combine with existing questions
        all_questions = existing + new_questions
        
        return all_questions
    
    def save_merged_questions(self, output_file="merged_questions.json"):
        """Save merged questions to file"""
        try:
            merged = self.merge_questions()
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(merged, file, ensure_ascii=False, indent=2)
            
            logging.info(f"Merged questions saved to {output_file}")
            return True
        except Exception as e:
            logging.error(f"Error saving merged questions: {e}")
            return False

def main():
    """Integration helper main function"""
    integrator = TriviaIntegrator()
    
    print("--- TRIVIA INTEGRATION ---")
    
    # Load and display counts
    existing = integrator.load_existing_questions()
    templates = integrator.load_extracted_templates()
    
    print(f"Existing questions: {len(existing)}")
    print(f"Extracted templates: {len(templates)}")
    
    # Create merged file
    if integrator.save_merged_questions():
        print("✅ Questions merged successfully")
        print("📝 Review 'merged_questions.json' and complete the templates")
    else:
        print("❌ Integration failed")

if __name__ == "__main__":
    main()