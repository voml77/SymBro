from modules.skills.file_handler import FileHandler
import os
import importlib

class SkillManager:
    def __init__(self):
        self.skills = {}
        self.register_skills()

    def register_skills(self):
        """Registriert alle verfügbaren Skills aus dem Verzeichnis."""
        skills_dir = os.path.dirname(__file__)
        for filename in os.listdir(skills_dir):
            if filename.endswith(".py") and filename not in ("__init__.py", "skill_manager.py"):
                module_name = f"modules.skills.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, "Skill"):
                        skill_instance = module.Skill()
                        self.skills[filename[:-3]] = skill_instance
                        print(f"Skill '{filename[:-3]}' erfolgreich geladen.")
                    else:
                        print(f"Modul '{filename}' enthält keine 'Skill'-Klasse.")
                except Exception as e:
                    print(f"Fehler beim Laden von Skill '{filename}': {e}")

    def get_skill(self, skill_name):
        """Gibt eine Skill-Instanz basierend auf dem Namen zurück."""
        skill = self.skills.get(skill_name)
        if not skill:
            print(f"Skill '{skill_name}' nicht gefunden.")
        return skill

    def run(self, skill_name, *args, **kwargs):
        skill = self.skills.get(skill_name)
        if not skill:
            print(f"Skill '{skill_name}' ist nicht aufrufbar.")
            return None
        try:
            result = skill(*args, **kwargs)

            # Optionales RLHF-Logging für jeden Skill
            try:
                import modules.rlhf.rlhf_engine as rlhf
                if hasattr(rlhf, "log_interaction"):
                    rlhf.log_interaction(
                        state=args[0] if args else None,
                        action=skill_name,
                        reward="PENDING",
                        next_state=result
                    )
            except Exception as log_error:
                print(f"RLHF-Logging fehlgeschlagen: {log_error}")

            return result
        except Exception as e:
            print(f"Fehler beim Ausführen von Skill '{skill_name}': {e}")
            return None
