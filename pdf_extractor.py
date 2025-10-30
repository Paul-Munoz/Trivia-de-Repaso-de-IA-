import fitz  # PyMuPDF library (install with: pip install PyMuPDF)
import os
import json
import logging
from datetime import datetime

# --- CONFIGURATION ---
NOMBRE_ARCHIVO_PDF = "Clase - Repaso de conceptos.pptx - Presentaciones de Google.pdf"
NOMBRE_ARCHIVO_SALIDA = "texto_repaso_completo.txt"
QUESTIONS_OUTPUT = "extracted_questions.json"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_extractor.log'),
        logging.StreamHandler()
    ]
)

class PDFExtractor:
    """Enhanced PDF text extractor with question generation capabilities"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extracted_text = []
        
    def extract_text_from_pdf(self):
        """Extract text from all PDF pages"""
        if not os.path.exists(self.pdf_path):
            logging.error(f"File not found: '{self.pdf_path}'")
            return None

        try:
            document = fitz.open(self.pdf_path)
            num_pages = document.page_count
            logging.info(f"Document opened. Total pages: {num_pages}")

            for page_num in range(num_pages):
                page = document.load_page(page_num)
                text = page.get_text("text")
                
                formatted_text = {
                    "page": page_num + 1,
                    "content": text.strip(),
                    "char_count": len(text.strip())
                }
                
                self.extracted_text.append(formatted_text)
                
            document.close()
            logging.info("Text extraction completed successfully")
            return self.extracted_text

        except Exception as e:
            logging.error(f"Error during extraction: {e}")
            return None

    def save_text_to_file(self, output_path):
        """Save extracted text to file"""
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                for page_data in self.extracted_text:
                    file.write(f"\n{'='*50}\n")
                    file.write(f"PAGE {page_data['page']}\n")
                    file.write(f"{'='*50}\n")
                    file.write(page_data['content'])
                    file.write("\n\n")
            
            logging.info(f"Text saved to: '{output_path}'")
            return True
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return False

    def generate_question_templates(self):
        """Generate question templates from extracted content"""
        questions = []
        
        for page_data in self.extracted_text:
            content = page_data['content']
            
            # Skip pages with minimal content
            if len(content) < 50:
                continue
                
            # Extract key concepts (simplified approach)
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            for line in lines:
                if len(line) > 20 and '?' not in line:
                    question_template = {
                        "source_page": page_data['page'],
                        "concept": line[:100] + "..." if len(line) > 100 else line,
                        "question": f"¿Qué se entiende por: {line[:50]}...?",
                        "category": "Conceptos Generales",
                        "difficulty": "medium"
                    }
                    questions.append(question_template)
        
        return questions

    def save_questions_template(self, questions, output_path):
        """Save question templates to JSON file"""
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(questions, file, ensure_ascii=False, indent=2)
            
            logging.info(f"Question templates saved to: '{output_path}'")
            return True
        except Exception as e:
            logging.error(f"Error saving questions: {e}")
            return False

    def get_statistics(self):
        """Get extraction statistics"""
        if not self.extracted_text:
            return None
            
        total_chars = sum(page['char_count'] for page in self.extracted_text)
        pages_with_content = len([p for p in self.extracted_text if p['char_count'] > 0])
        
        return {
            "total_pages": len(self.extracted_text),
            "pages_with_content": pages_with_content,
            "total_characters": total_chars,
            "average_chars_per_page": total_chars // len(self.extracted_text) if self.extracted_text else 0
        }

def main():
    """Main execution function"""
    print("--- PDF PROCESSING STARTED ---")
    
    # Initialize extractor
    extractor = PDFExtractor(NOMBRE_ARCHIVO_PDF)
    
    # Extract text
    extracted_data = extractor.extract_text_from_pdf()
    
    if extracted_data:
        # Save text file
        extractor.save_text_to_file(NOMBRE_ARCHIVO_SALIDA)
        
        # Generate question templates
        questions = extractor.generate_question_templates()
        extractor.save_questions_template(questions, QUESTIONS_OUTPUT)
        
        # Display statistics
        stats = extractor.get_statistics()
        print("\n--- EXTRACTION STATISTICS ---")
        print(f"Total pages: {stats['total_pages']}")
        print(f"Pages with content: {stats['pages_with_content']}")
        print(f"Total characters: {stats['total_characters']}")
        print(f"Question templates generated: {len(questions)}")
        
        # Preview first page
        if extracted_data:
            print("\n--- FIRST PAGE PREVIEW ---")
            print(extracted_data[0]['content'][:300] + "...")
        
        print("\n--- PROCESSING COMPLETED ---")
        print("Files ready for integration with trivia application")
        
    else:
        print("❌ Extraction failed. Check logs for details.")

if __name__ == "__main__":
    main()