import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QLineEdit, QSizePolicy, QSpacerItem, QListWidgetItem, QMenu
)
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QGuiApplication, QPixmap
from modules.namesoul import NameSoul
from modules.memory import Memory
import os
import datetime
import shutil

def clear_upload_folder():
    upload_dir = os.path.join("data", "uploads")
    if os.path.exists(upload_dir):
        for file in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Fehler beim Löschen der Upload-Datei: {file_path} – {e}")

class MainWindow(QMainWindow):
    def __init__(self, skill_manager):
        super().__init__()
        self.setAcceptDrops(True)
        clear_upload_folder()
        self.skill_manager = skill_manager
        
        self.name = NameSoul().get_name()
        self.theme_color = NameSoul().get_color()
        self.memory = Memory()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.selected_chat_id = None
        self.existing_titles = set()
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
        left_widget.setStyleSheet(f"background-color: {self.theme_color};")

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
        
        self.chat_list = QListWidget()
        self.chat_list.itemClicked.connect(self.chat_selected)
        left_layout.addWidget(self.chat_list)

        left_layout.addLayout(icon_layout)  # Add Icon Layout
        
        left_layout.addSpacing(10)

        self.chat_list.setContentsMargins(0, 0, 0, 0)
        self.chat_list.setStyleSheet(
            f"background-color: {self.theme_color}; color: white; border-radius: 10px; border: 2px solid #1a1a1a;"
            "font-size: 16px; font-family: 'Arial';"
        )
        self.chat_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chat_list.customContextMenuRequested.connect(self.show_chat_context_menu)

        # Existierende Chats laden
        for chat in self.memory.load_chats():
            item = QListWidgetItem("⭐ " + chat["title"] if chat.get("favorite") else chat["title"])
            item.setData(Qt.UserRole, chat["id"])
            item.setData(Qt.UserRole + 1, chat.get("favorite", False))  # Store favorite status
            self.chat_list.addItem(item)
            self.existing_titles.add(chat["title"])
            print(f"Added chat: {chat['title']}, ID: {chat['id']}")
             
        # Rechter Bereich
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #020202;")
        right_layout = QVBoxLayout(right_widget)

        self.welcome_label = QLabel(f"SymBro - {self.name} aktiv")
        self.welcome_label.setStyleSheet("color: white; font-size: 24px;")
        right_layout.addWidget(self.welcome_label)

        self.message_list = QListWidget()
        self.message_list.setAcceptDrops(True)
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

        icon_size = QSize(28, 28)
        
        send_pixmap = QPixmap("gui_pyside/icons/send_icon.png").scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        send_icon = QIcon(send_pixmap)
        send_action = self.input_field.addAction(send_icon, QLineEdit.TrailingPosition)
        send_action.setToolTip("Nachricht senden")
        send_action.triggered.connect(self.send_message)
        
        md_pixmap = QPixmap("gui_pyside/icons/md_icon.png").scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        md_icon = QIcon(md_pixmap)
        md_action = self.input_field.addAction(md_icon, QLineEdit.TrailingPosition)
        md_action.setToolTip("Chat als Markdown exportieren")
        md_action.triggered.connect(self.export_chat_to_markdown)
        
        plus_pixmap = QPixmap("gui_pyside/icons/plus_icon.png").scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        plus_icon = QIcon(plus_pixmap)
        plus_action = self.input_field.addAction(plus_icon, QLineEdit.TrailingPosition)
        plus_action.setToolTip("Datei hinzufügen (Upload)")
        plus_action.triggered.connect(self.handle_plus_icon_click)
        
        self.input_field.setStyleSheet("""
            background-color: #1a1a1a;
            color: white;
            border-radius: 10px;
            border: 2px solid #1f4449;
            padding-right: 90px;
        """)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        right_layout.addLayout(input_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        self.setCentralWidget(main_widget)
        self.input_field.returnPressed.connect(self.send_message)
        self.chat_list.itemDoubleClicked.connect(self.rename_chat)
        self.chat_list.itemChanged.connect(self.chat_title_changed)

    def change_color(self):
        from PySide6.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self.theme_color = color.name()
            NameSoul().set_color(self.theme_color)

            self.chat_list.setStyleSheet(
                f"background-color: {self.theme_color}; color: white; border-radius: 10px; border: 2px solid #1a1a1a;"
                "font-size: 16px; font-family: 'Arial';"
            )
            self.centralWidget().findChild(QWidget).setStyleSheet(f"background-color: {self.theme_color};")

    def new_chat(self):
        base_title = "Neuer Chat"
        counter = 1
        while f"{base_title} {counter}" in self.existing_titles:
            counter += 1
        chat_title = f"{base_title} {counter}"
        self.existing_titles.add(chat_title)
        
        chat_id = f"chat_{self.chat_list.count() + 1}"
        item = QListWidgetItem(chat_title)
        item.setData(Qt.UserRole, chat_id)
        self.chat_list.addItem(item)
        chat_data = {
            "id": chat_id,
            "title": chat_title,
            "messages": []  # Wichtig: Leere Nachrichtenliste hinzufügen
            }
        self.memory.save_chat(chat_data["id"], chat_data["title"], chat_data["messages"])
        
        self.selected_chat_id = chat_id
        self.message_list.clear()
        self.welcome_label.setText(f"SymBro - {self.name} aktiv")

    def delete_current_chat(self):
        item = self.chat_list.currentItem()
        if item:
            chat_id = item.data(Qt.UserRole)
            self.memory.delete_chat(chat_id)
            self.memory.remove_chat_from_list(chat_id)
            self.chat_list.takeItem(self.chat_list.row(item))
            self.message_list.clear()
            self.existing_titles.discard(item.text())
            
    def chat_selected(self, item):
        if item:
            for i in range(self.chat_list.count()):
                other_item = self.chat_list.item(i)
                if other_item != item:
                    other_item.setBackground(Qt.transparent)
                    other_item.setForeground(Qt.white)
                    font = other_item.font()
                    font.setBold(False)
                    other_item.setFont(font)
            item.setBackground(QColor("#2b6d72"))  # leicht helleres Cyan passend zum Hintergrund
            item.setForeground(Qt.white)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.selected_chat_id = item.data(Qt.UserRole)
            chat_data = self.memory.load_chat_by_id(self.selected_chat_id)
            if chat_data and "messages" in chat_data:
                self.message_list.clear()
                for msg in chat_data["messages"]:
                    prefix = f"🧑 Du ({msg.get('timestamp', '')}):\n" if msg["role"] == "user" else f"🤖 {self.name} ({msg.get('timestamp', '')}):\n"
                    item_msg = QListWidgetItem()
                    item_msg.setText(f"{prefix}{msg['content']}")
                    item_msg.setTextAlignment(Qt.AlignLeft)
                    if msg["role"] == "user":
                        item_msg.setBackground(QColor("#2b6d72"))
                    else:
                        item_msg.setBackground(QColor("#444444"))
                    item_msg.setForeground(Qt.white)
                    self.message_list.addItem(item_msg)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
        else:
            print("Kein Item ausgewählt!")

    def send_message(self):
        message = self.input_field.text().strip()
        if message:
            user_item = QListWidgetItem(f"🧑 Du ({datetime.datetime.now().strftime('%H:%M')}): {message}")
            self.message_list.addItem(user_item)
            elias_item = QListWidgetItem(f"🤖 Elias ({datetime.datetime.now().strftime('%H:%M')}): Ich habe deine Nachricht erhalten.")
            self.message_list.addItem(elias_item)
            self.input_field.clear()
            print(self.selected_chat_id)

            if self.selected_chat_id is not None:
                chat_id = self.selected_chat_id
                new_title = message[:30] + "..." if len(message) > 30 else message
                try:# Finde das Item in der Liste und aktualisiere den Titel
                    for i in range(self.chat_list.count()):
                        item = self.chat_list.item(i)
                        if item.data(Qt.UserRole) == chat_id:
                            item.setText(new_title)
                            item.setFlags(item.flags() | Qt.ItemIsEditable)
                            self.memory.update_chats_list(chat_id, new_title)
                            break
                
                    # Speichere den Chatverlauf in einer Datei
                    messages = []
                    for index in range(self.message_list.count()):
                        text = self.message_list.item(index).text()
                        if text.startswith("🧑 Du"):
                            role = "user"
                        elif text.startswith(f"🤖 {self.name}"):
                            role = "elias"
                        else:
                            role = "elias"
                        messages.append({"role": role, "content": text})
                    self.memory.save_chat(chat_id, new_title, messages)
                    self.message_list.scrollToBottom()
                    self.existing_titles.add(new_title)
                
                except Exception as e:
                    print(f"Fehler beim Speichern des Chats: {e}")
                    import traceback
                    traceback.print_exc()  
            
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
        favorite_action = menu.addAction("Als Favorit markieren")
        unfavorite_action = menu.addAction("Favorit entfernen")
        action = menu.exec_(self.chat_list.viewport().mapToGlobal(position))
        if action == delete_action:
            self.delete_current_chat()
        elif action == favorite_action:
            item = self.chat_list.currentItem()
            if item:
                item.setText("⭐ " + item.text() if not item.text().startswith("⭐ ") else item.text())
                item.setData(Qt.UserRole + 1, True)
        elif action == unfavorite_action:
            item = self.chat_list.currentItem()
            if item:
                if item.text().startswith("⭐ "):
                    item.setText(item.text()[2:])
                item.setData(Qt.UserRole + 1, False)
    
    def rename_chat(self, item):
        old_title = item.text()
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.chat_list.editItem(item)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        item.setSelected(True)
        self.chat_list.setCurrentItem(item)
        self.chat_list.editItem(item)

    def chat_title_changed(self, item):
        if item:
            chat_id = item.data(Qt.UserRole)
            new_title = item.text()
            is_favorite = item.data(Qt.UserRole + 1)
            self.memory.update_chats_list(chat_id, new_title, is_favorite)

            # Automatisch auch den Chatverlauf speichern mit neuem Titel
            messages = []
            for index in range(self.message_list.count()):
                text = self.message_list.item(index).text()
                if text.startswith("🧑 Du"):
                    role = "user"
                elif text.startswith(f"🤖 {self.name}"):
                    role = "elias"
                else:
                    role = "elias"
                messages.append({
                    "role": role,
                    "content": text.split("): ", 1)[-1]
                })
            self.memory.save_chat(chat_id, new_title, messages)

    def export_chat_to_markdown(self):
        if not self.selected_chat_id:
            print("Kein Chat ausgewählt zum Export.")
            return

        chat_data = self.memory.load_chat_by_id(self.selected_chat_id)
        if not chat_data:
            print("Kein Chatverlauf vorhanden.")
            return

        title = chat_data["title"]
        messages = chat_data.get("messages", [])
        lines = [f"## Chat: {title}", ""]

        for msg in messages:
            role = msg.get("role", "elias")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", datetime.datetime.now().strftime('%H:%M'))
            sender = "🧑 Du" if role == "user" else f"🤖 {self.name}"
            lines.append(f"**{sender} ({timestamp}):**\n{content}\n\n---")

        markdown_content = "\n\n".join(lines)

        export_dir = os.path.join("data", "exports")
        os.makedirs(export_dir, exist_ok=True)
        file_path = os.path.join(export_dir, f"{title.replace(' ', '_')}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Chat erfolgreich exportiert nach: {file_path}")
        self.message_list.addItem(QListWidgetItem(f"✅ Chat exportiert nach: {file_path}"))


    def save_uploaded_file(self, file_path):
        try:
            filename = os.path.basename(file_path)
            target_dir = os.path.join("data", "uploads")
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, filename)
            shutil.copy(file_path, target_path)
            print(f"Datei erfolgreich gespeichert: {target_path}")
            return target_path
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")
            return None

    def handle_plus_icon_click(self):
        from PySide6.QtWidgets import QFileDialog
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                saved_path = self.save_uploaded_file(file_path)
                if saved_path:
                    ext = os.path.splitext(saved_path)[1].lower()
                    if ext in [".png", ".jpg", ".jpeg", ".gif"]:
                        file_icon = "🖼"
                    elif ext in [".mp3", ".wav", ".ogg"]:
                        file_icon = "🎵"
                    else:
                        file_icon = "📄"
                    self.message_list.addItem(QListWidgetItem(f"{file_icon} Datei hinzugefügt: {os.path.basename(saved_path)}"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                saved_path = self.save_uploaded_file(file_path)
                if saved_path:
                    self.message_list.addItem(QListWidgetItem(f"📎 Datei hinzugefügt: {os.path.basename(saved_path)}"))

# Ausführen, wenn Datei direkt gestartet wird
if __name__ == "__main__":
    from modules.skills.skill_manager import SkillManager
    app = QApplication(sys.argv)
    skill_manager = SkillManager()
    window = MainWindow(skill_manager)
    window.show()
    sys.exit(app.exec())
