
import json
from pathlib import Path

def run(messages, name):
    insight_path = Path("data/config/user_insight.json")
    if not insight_path.exists():
        return "Ich habe bisher keine Informationen über dich gespeichert. Du kannst mich trainieren, indem du mir Feedback gibst!"

    with open(insight_path, "r", encoding="utf-8") as f:
        insights = json.load(f)

    user_style = insights.get("user_style", "nicht näher beschrieben")
    positives = insights.get("belohnte_tendenzen", [])
    negatives = insights.get("vermeidbare_tendenzen", [])

    response = f"Ich lerne durch dein Feedback. Bisher habe ich folgende Dinge über dich gespeichert:\n\n"
    response += f"🧠 Dein Stil: {user_style}\n"
    if positives:
        response += f"✅ Du belohnst oft: {', '.join(positives)}\n"
    if negatives:
        response += f"⚠️ Du vermeidest eher: {', '.join(negatives)}\n"
    response += "\nDiese Infos helfen mir, besser auf dich einzugehen."

    return response

class Skill:
    def __call__(self, *args, **kwargs):
        return run(*args, **kwargs)