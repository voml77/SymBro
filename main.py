from PySide6.QtWidgets import QApplication
from gui_pyside.main_window import MainWindow
from modules.skills.skill_manager import SkillManager
import sys

def main():
    skill_manager = SkillManager()  # Skills initialisieren
    app = QApplication(sys.argv)
    window = MainWindow(skill_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()