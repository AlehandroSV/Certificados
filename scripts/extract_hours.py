import os
import sys
import json
import re

# Add local libs to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, "python_libs"))

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not found. Please install it first.")
    sys.exit(1)

def extract_hours(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        
        # Pattern 1: "X horas"
        # Pattern 2: "carga horária de X"
        # Pattern 3: "Xh"
        
        # Try to find common patterns
        # DIO: "com carga horária de 2 horas"
        # DevSamurai: "carga horária de 10 horas"
        
        patterns = [
            r"carga horária de ([\d.,]+)\s*hora",
            r"carga horária de:?\s*([\d.,]+)",
            r"([\d.,]+)\s*hora",
            r"carga horária:?\s*([\d.,]+)",
            r"duration:?\s*([\d.,]+)",
            r"total de ([\d.,]+)\s*hora",
            r"([\d.,]+)h\b",
            r"([\d.,]+)\s*hrs"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val = match.group(1).replace(",", ".")
                try:
                    return float(val)
                except:
                    continue
        
        return 0
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return 0

def main():
    base_dir = "."
    results = []
    total_hours = 0
    
    # Categories to skip
    skip_dirs = ["python_libs", ".git", "_Meta"] # Skipping _Meta as they are non-technical usually, but user might want them?
    # User said "abrir os cursos", usually technical. But I'll include everything and let the user decide.
    # Actually, I'll include _Meta too but skip the script folder.
    skip_dirs = ["python_libs", ".git"]

    for root, dirs, files in os.walk(base_dir):
        # Filter out skip_dirs
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)
                category = os.path.basename(root)
                
                hours = extract_hours(full_path)
                
                results.append({
                    "file": file,
                    "path": full_path,
                    "category": category,
                    "hours": hours
                })
                total_hours += hours
                print(f"Found {hours}h in {file}")

    output_data = {
        "total_hours": total_hours,
        "certificates_count": len(results),
        "certificates": results
    }
    
    with open("certificados.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nDone! Total hours: {total_hours}")
    print(f"Results saved to certificados.json")

if __name__ == "__main__":
    main()
