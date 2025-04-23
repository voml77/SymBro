from PySide6.QtWidgets import QApplication
from gui_pyside.main_window import MainWindow
from modules.skills.skill_manager import SkillManager
import sys, os
from modules.rlhf.replay_buffer import PrioritizedReplayBuffer
from modules.rlhf.rlhf_engine import load_logs_to_replay_buffer, summarize_log_rewards, clear_interaction_log
from utils.duplicate_remover import remove_duplicates_from_interactions
from modules.rlhf.rlhf_auto_manager import start_rlhf_pipeline
from utils.embedding_generator import generate_and_save_embedding, auto_sync_embeddings_to_buffer

# Im Hauptablauf (nach dem Setup etc.)

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    skill_manager = SkillManager()  # Skills initialisieren
    remove_duplicates_from_interactions()
    buffer = PrioritizedReplayBuffer(capacity=1000)
    auto_sync_embeddings_to_buffer(buffer)
    # RLHF ReplayBuffer mit bestehenden Logs synchronisieren
    #clear_interaction_log()
    from utils.embedding_generator import generate_and_save_embedding
    import uuid
    import json
    logs_path = os.path.join("data", "rlhf", "logs", "interactions.json")
    if os.path.exists(logs_path):
        with open(logs_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
        for entry in logs:
            sample_id = entry.get("id") or str(uuid.uuid4())
            state = entry.get("state")
            if state:
                generate_and_save_embedding(state, sample_id)
    load_logs_to_replay_buffer(buffer)
    app = QApplication(sys.argv)
    window = MainWindow(skill_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    summarize_log_rewards()
    main()