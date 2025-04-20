from PySide6.QtWidgets import QApplication
from gui_pyside.main_window import MainWindow
from modules.skills.skill_manager import SkillManager
import sys
from modules.rlhf.replay_buffer import PrioritizedReplayBuffer
from modules.rlhf.rlhf_engine import load_logs_to_replay_buffer, summarize_log_rewards, clear_interaction_log

def main():
    skill_manager = SkillManager()  # Skills initialisieren
    # RLHF ReplayBuffer mit bestehenden Logs synchronisieren
    #clear_interaction_log()
    buffer = PrioritizedReplayBuffer(capacity=1000)
    load_logs_to_replay_buffer(buffer)
    summarize_log_rewards()
    app = QApplication(sys.argv)
    window = MainWindow(skill_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()