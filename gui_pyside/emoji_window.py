from PySide6.QtWidgets import QDialog, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PySide6.QtCore import Signal, Qt, QPoint

class EmojiWindow(QDialog):
    emoji_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Emoji auswählen")
        self.setFixedSize(380, 370)
        self.setStyleSheet("background-color: #1f4449; border-radius: 20px;") 

        self.all_emojis = {
            "Alle": [
                "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
                "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙", "😚", "😋",
                "😜", "😝", "😛", "🤑", "🤗", "🤔", "😐", "😑", "😶", "🙄",
                "😏", "😣", "😥", "😮", "🤐", "😯", "😪", "😫", "😴", "😌"
            ],
            "Fröhlich": ["😀", "😃", "😄", "😁", "😊", "😍", "😘", "😋"],
            "Neutral": ["😐", "😑", "😶", "😏", "🙃", "🙂"],
            "Traurig": ["😣", "😥", "😪", "😫", "😴", "😯"],
            "Sonstige": ["🤔", "🤗", "🙄", "🤐", "🤑"]
        }
        
        self.current_category = "Alle"

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Kategorienauswahl
        category_layout = QHBoxLayout()
        for category in self.all_emojis.keys():
            btn = QPushButton(category)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2f5d62;
                    color: white;
                    border-radius: 6px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #3e7b80;
                }
            """)
            btn.clicked.connect(lambda _, c=category: self.load_emojis(c))
            category_layout.addWidget(btn)
        main_layout.addLayout(category_layout)

        # Emoji-Grid
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)
        self.load_emojis("Alle")

    def select_emoji(self, emoji):
        self.emoji_selected.emit(emoji)
        self.close()

    def load_emojis(self, category):
        self.current_category = category
        # Grid leeren
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        # Emojis neu laden
        emojis = self.all_emojis.get(category, [])
        rows, cols = 8, 5
        for idx, emoji in enumerate(emojis):
            button = QPushButton(emoji)
            button.setFixedSize(36, 36)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 22px;
                    border-radius: 8px;
                    background-color: #2f5d62;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #3e7b80;
                }
            """)
            button.clicked.connect(lambda _, e=emoji: self.select_emoji(e))
            self.grid_layout.addWidget(button, idx // cols, idx % cols)

if __name__ == "__main__":
    app = QApplication([])
    window = EmojiWindow()
    window.show()
    app.exec()