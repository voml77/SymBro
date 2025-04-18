from modules.skills.file_handler import FileHandler
from modules.skills.gpt_chat import Skill

class SkillManager:
    def __init__(self):
        self.skills = {}
        self.register_skills()
        self.skills["gpt_chat"] = Skill()

    def register_skills(self):
        """Registriert alle verfügbaren Skills."""
        self.skills['file_handler'] = FileHandler()

    def get_skill(self, skill_name):
        """Gibt eine Skill-Instanz basierend auf dem Namen zurück."""
        skill = self.skills.get(skill_name)
        if not skill:
            print(f"Skill '{skill_name}' nicht gefunden.")
        return skill

    def run(self, skill_name, *args, **kwargs):
        skill = self.get_skill(skill_name)
        if callable(skill):
            return skill(*args, **kwargs)
        else:
            print(f"Skill '{skill_name}' ist nicht aufrufbar.")
            return None
