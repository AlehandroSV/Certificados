import os
import sys
import re


from pypdf import PdfReader

def debug_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        
        print(f"--- TEXT START ({pdf_path}) ---")
        print(text)
        print("--- TEXT END ---")
        
        patterns = [
            r"carga horária de (\d+)\s*horas",
            r"(\d+)\s*horas",
            r"carga horária:?\s*(\d+)",
            r"duration:?\s*(\d+)",
            r"(\d+)h\b"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                print(f"Match found with pattern '{pattern}': {match.group(1)}")
            else:
                print(f"No match for pattern '{pattern}'")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "./JavaScript/[DIO] Dominando Funções em JavaScript.pdf"
    debug_pdf(path)
