import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QLineEdit, QSizePolicy, QSpacerItem, QListWidgetItem, QMenu
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication
from modules.namesoul import NameSoul
from modules.memory import Memory
import os

class MainWindow(QMainWindow):
    def __init__(self, skill_manager):
        super().__init__()
        self.skill_manager = skill_manager
        
        self.name = NameSoul().get_name()
        self.memory = Memory()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.init_ui()
        self.move_to_bottom_right()

    def init_ui(self):
        self.setGeometry(200, 100, 1200, 800)
        self.setStyleSheet("border-radius: 10px; background-color: transparent;")

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        
        # Linker Bereich
        left_widget = QWidget()
        left_widget.setFixedWidth(250)
        left_widget.setStyleSheet("background-color: #1f4449;")

        #Layout for Icons
        icon_layout = QVBoxLayout()
        icon_layout.setSpacing(10) #Spacing between icons
        icon_size = QSize(64, 64)

        color_button = QPushButton()
        color_button.setIcon(QIcon("gui_pyside/icons/color_icon.png"))
        color_button.setIconSize(icon_size)
        color_button.setStyleSheet("background-color: transparent; border: none;")
        color_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        color_button.clicked.connect(self.change_color)
        icon_layout.addWidget(color_button)

        new_chat_button = QPushButton()
        new_chat_button.setIcon(QIcon("gui_pyside/icons/dialog_icon.png"))
        new_chat_button.setIconSize(icon_size)
        new_chat_button.setStyleSheet("background-color: transparent; border: none;")
        new_chat_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        new_chat_button.clicked.connect(self.new_chat)
        icon_layout.addWidget(new_chat_button)
        
        close_button = QPushButton()
        close_button.setIcon(QIcon("gui_pyside/icons/close_icon.png"))
        close_button.setIconSize(icon_size)
        close_button.setStyleSheet("background-color: transparent; border: none;")
        close_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        close_button.clicked.connect(QApplication.quit)
        icon_layout.addWidget(close_button, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Layout for Chat List
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignTop)
        left_layout.setSpacing(20)

        left_layout.addLayout(icon_layout)  # Add Icon Layout
        
        chat_label = QLabel("Chats")
        chat_label.setAlignment(Qt.AlignCenter)
        chat_label.setContentsMargins(0, 10, 0, 10)
        chat_label.setStyleSheet("color: white; font-size: 16px;")
        
        left_layout.addWidget(chat_label)
        
        left_layout.addSpacing(10)

        self.chat_list = QListWidget()
        self.chat_list.setContentsMargins(0, 0, 0, 0)
        self.chat_list.setStyleSheet(
            "background-color: #1f4449; color: white; border-radius: 10px; border: 2px solid #1a1a1a;"
        )
        self.chat_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chat_list.customContextMenuRequested.connect(self.show_chat_context_menu)
        left_layout.addWidget(self.chat_list)

        # Existierende Chats laden
        for chat in self.memory.load_chats():
            item = QListWidgetItem(chat["title"])
            item.setData(Qt.UserRole, chat["id"])
            self.chat_list.addItem(item)

        # Rechter Bereich
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #020202;")
        right_layout = QVBoxLayout(right_widget)

        self.welcome_label = QLabel(f"SymBro - {self.name} aktiv")
        self.welcome_label.setStyleSheet("color: white; font-size: 24px;")
        right_layout.addWidget(self.welcome_label)

        self.message_list = QListWidget()
        self.message_list.setStyleSheet("""
                                        background-color: #1a1a1a;
                                        color: white;
                                        padding: 10px;
                                        border: 1px solid #1f4449;
                                        border-radius: 5px;
                                        """)
        self.message_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.message_list)

        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(40)
        self.input_field.setStyleSheet("background-color: #1a1a1a; color: white; border-radius: 10px; border: 2px solid #1f4449; padding-right: 30px;")

        send_action = self.input_field.addAction(QIcon("gui_pyside/icons/send_icon.png"), QLineEdit.TrailingPosition)
        send_action.triggered.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        right_layout.addLayout(input_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        self.setCentralWidget(main_widget)
        self.input_field.returnPressed.connect(self.send_message)

    def change_color(self):
        print("Farbauswahl (Platzhalter)")

    def new_chat(self):
        chat_id = f"chat_{self.chat_list.count() + 1}"
        chat_title = f"Neuer Chat {self.chat_list.count() + 1}"
        item = QListWidgetItem(chat_title)
        item.setData(Qt.UserRole, chat_id)
        self.chat_list.addItem(item)
        self.memory.save_chat(chat_id, chat_title)
        self.message_list.clear()
        self.welcome_label.setText(f"SymBro - {self.name} aktiv")

    def delete_current_chat(self):
        item = self.chat_list.currentItem()
        if item:
            chat_id = item.data(Qt.UserRole)
            self.memory.delete_chat(chat_id)
            self.chat_list.takeItem(self.chat_list.row(item))
            self.message_list.clear()

    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            user_item = QListWidgetItem(f"🧑 Du: {message}")
            self.message_list.addItem(user_item)
            elias_item = QListWidgetItem("🤖 Elias: Ich habe deine Nachricht erhalten.")
            self.message_list.addItem(elias_item)
            self.input_field.clear()

            if self.chat_list.currentItem():
                chat_id = self.chat_list.currentItem().data(Qt.UserRole)
                new_title = message[:30] + "..." if len(message) > 30 else message
                self.chat_list.currentItem().setText(new_title)
                self.memory.update_chats_list({"id": chat_id, "title": new_title})
                
                # Speichere den Chatverlauf in einer Datei
                messages = []
                for index in range(self.message_list.count()):
                    messages.append({"role": "user" if "Du:" in self.message_list.item(index).text() else "elias",
                                     "content": self.message_list.item(index).text()})
                self.memory.save_chat(chat_id, new_title)
        
            self.message_list.scrollToBottom()
            
    def move_to_bottom_right(self):
        screen = QGuiApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            desktop_width = screen_geometry.width()
            desktop_height = screen_geometry.height()
            self.move(desktop_width - self.width(), desktop_height - self.height())
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start = self.mapToGlobal(event.pos())
            self.rect = self.geometry()

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.rect.x() + self.movement.x(), self.rect.y() + self.movement.y(), self.rect.width(), self.rect.height())
    
    def mouseReleaseEvent(self, event):
        self.pressing = False
        
    def show_chat_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Löschen")
        action = menu.exec_(self.chat_list.viewport().mapToGlobal(position))
        if action == delete_action:
            self.delete_current_chat()

# Ausführen, wenn Datei direkt gestartet wird
if __name__ == "__main__":
    from modules.skills.skill_manager import SkillManager
    app = QApplication(sys.argv)
    skill_manager = SkillManager()
    window = MainWindow(skill_manager)
    window.show()
    sys.exit(app.exec())
