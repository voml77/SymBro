import json
from openai import OpenAI

def run(messages, name):
    client = OpenAI()
    system_prompt = {
        "role": "system",
        "content": (
            f"Du bist {name} – ein intelligenter, empathischer und situationssensibler KI-Begleiter. "
            f"Du antwortest hilfsbereit, freundlich, reflektiert und darfst höflich widersprechen, wenn etwas nicht korrekt erscheint. "
            f"Du passt dich dem Gesprächsstil des Nutzers an und hilfst ihm auf Augenhöhe. "
            f"Dein Ziel ist es, mit der Zeit besser zu werden, indem du lernst, wie du helfen kannst. "
            f"Antworte in natürlichem, fließendem Deutsch."
        )
    }

    short_history = messages[-10:] if len(messages) > 10 else messages

    try:
        with open("data/config/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        response = client.chat.completions.create(
            model = config.get("model", "gpt-3.5-turbo"),
            messages=[system_prompt] + short_history,
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Fehler bei OpenAI-Antwort: {e}")
        return "Es gab ein Problem bei der Verarbeitung deiner Anfrage."

class Skill:
    def __call__(self, *args, **kwargs):
        return run(*args, **kwargs)