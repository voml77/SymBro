from modules.skills.file_handler import FileHandler

class SkillManager:
    def __init__(self):
        self.skills = {}
        self.register_skills()

    def register_skills(self):
        """Registriert alle verfügbaren Skills."""
        self.skills['file_handler'] = FileHandler()

    def get_skill(self, skill_name):
        """Gibt eine Skill-Instanz basierend auf dem Namen zurück."""
        skill = self.skills.get(skill_name)
        if not skill:
            print(f"Skill '{skill_name}' nicht gefunden.")
        return skill
