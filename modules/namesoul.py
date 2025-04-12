import json
import os
import openai

class NameSoul:
    def __init__(self):
        self.identity_file = 'data/identity.json'
        self.name = None
        self.load_name()

    def load_name(self):
        if os.path.exists(self.identity_file) and os.path.getsize(self.identity_file) > 0:
            with open(self.identity_file, 'r') as f:
                data = json.load(f)
                self.name = data.get('name')

    def name_exists(self):
        return self.name is not None

    def get_name(self):
        return self.name

    def greet_and_create_name(self):
        print("Hallo! Es freut mich wirklich, dich kennenzulernen.")
        print("Bevor wir gemeinsam loslegen, brauche ich noch etwas von dir.")
        print("Wie möchtest du mich nennen? Oder soll ich dir Vorschläge machen?")

        user_input = input("Gib mir deinen Wunsch-Namen oder schreibe 'vorschlag': ")

        if user_input.lower() == 'vorschlag':
            chosen_name = self.get_name_suggestion_from_openai()
            print(f"Wie wäre es mit '{chosen_name}'?")
            user_input = input("Oder hast du selbst einen Vorschlag?: ")
            if user_input.strip():
                chosen_name = user_input
        else:
            chosen_name = user_input

        self.name = chosen_name
        self.save_name()
        print(f"Perfekt! Von nun an heiße ich {self.name}. Schön, dich an meiner Seite zu haben.")

    def get_name_suggestion_from_openai(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = "Bitte schlage mir einen kurzen, freundlichen und einzigartigen Namen für einen intelligenten digitalen Desktop-Begleiter vor."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
        )
        return response.choices[0].message['content'].strip()

    def save_name(self):
        os.makedirs(os.path.dirname(self.identity_file), exist_ok=True)
        with open(self.identity_file, 'w') as f:
            json.dump({'name': self.name}, f)
