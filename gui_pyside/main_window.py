import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QTextEdit
from PySide6.QtGui import QIcon, QColor, QPalette
from PySide6.QtCore import Qt, QSize
from modules.namesoul import NameSoul

class MainWindow(QMainWindow):
    def __init__(self, skill_manager):
        super().__init__()
        self.skill_manager = skill_manager
        self.name = NameSoul().get_name()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{self.name} – Dein smarter Begleiter")
        self.setGeometry(100, 100, 900, 600)

        self.bg_color = "#225f63"
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.bg_color))
        palette.setColor(QPalette.WindowText, QColor("#225f63"))  # Titelbereich Hintergrundfarbe anpassen
        self.setPalette(palette)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QVBoxLayout()  # Für untereinander
        left_layout.setSpacing(10)
        left_widget.setLayout(left_layout)

        icon_size = QSize(64, 64)

        color_button = QPushButton()
        color_button.setIcon(QIcon("gui_pyside/icons/color_icon.png"))
        color_button.setIconSize(icon_size)
        color_button.setStyleSheet("background-color: transparent; border: none;")
        color_button.clicked.connect(self.change_color)
        left_layout.addWidget(color_button)

        new_chat_button = QPushButton()
        new_chat_button.setIcon(QIcon("gui_pyside/icons/dialog_icon.png"))
        new_chat_button.setIconSize(icon_size)
        new_chat_button.setStyleSheet("background-color: transparent; border: none;")
        new_chat_button.clicked.connect(self.new_chat)
        left_layout.addWidget(new_chat_button)

        self.chat_list = QListWidget()
        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)

        content_layout.addWidget(left_widget, 0)
        content_layout.addWidget(self.chat_list, 1)
        content_layout.addWidget(self.chat_view, 3)

        main_layout.addLayout(content_layout)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def change_color(self):
        print("Farbauswahl (Platzhalter)")

    def new_chat(self):
        print("Neuer Dialog (Platzhalter)")

if __name__ == "__main__":
    from modules.skills.skill_manager import SkillManager
    app = QApplication(sys.argv)
    skill_manager = SkillManager()
    window = MainWindow(skill_manager)
    window.show()
    sys.exit(app.exec())
