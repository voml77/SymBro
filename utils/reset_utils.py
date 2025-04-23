# utils/file_utils.py

import os

def reset_embeddings(file_path="data/rlhf/embeddings.json"):
    """
    Setzt die embeddings.json Datei zurück, indem sie geleert wird.
    """
    with open(file_path, "w") as f:
        f.write("[]")
    print(f"✅ {file_path} wurde erfolgreich zurückgesetzt.")
    
if __name__ == "__main__":
    reset_embeddings()