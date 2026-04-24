import json

with open("certificados.json", "r", encoding="utf-8") as f:
    data = json.load(f)

stats = {}
for c in data["certificates"]:
    cat = c["category"]
    h = c["hours"]
    stats[cat] = stats.get(cat, 0) + h

# Mapping folder names to the names in README.md
mapping = {
    "JavaScript": "JavaScript",
    "Banco-de-Dados": "Banco de Dados",
    "Fundamentos": "Fundamentos",
    "Linux-DevOps": "Linux & DevOps",
    "React": "React",
    "HTML-CSS": "HTML & CSS",
    "Python": "Python",
    "TypeScript": "TypeScript",
    "Git-GitHub": "Git & GitHub",
    "CSharp": "C#",
    "Java": "Java",
    "Node.js": "Node.js",
    "Inteligencia-Artificial": "Inteligência Artificial",
    "_Meta": "_Meta"
}

print("| Tecnologia | Horas |")
print("|---|---|")
for folder, name in mapping.items():
    h = stats.get(folder, 0)
    print(f"| {name} | {h}h |")

print(f"\nTotal: {data['total_hours']}h")
