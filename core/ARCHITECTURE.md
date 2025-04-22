# 🏗️ SymBro – Architekturübersicht

## 📂 Projektstruktur

```
SymBro/
├── core/
│   └── ARCHITECTURE.md           # → Architekturübersicht (dieses Dokument)
├── data/
│   └── rlhf/
│       └── logs/
│           └── interactions.json # → User-Interaktionen (Feedback + Rewards)
├── gui_pyside/                   # → GUI auf Basis von PySide6
├── modules/
│   └── rlhf_engine.py            # → RLHF-Logik (Q-Learning, Replay Buffer, Prioritäten)
│   └── replay_buffer.py          # → Prioritized Experience Replay Buffer
├── utils/
│   └── embedding_analyzer.py     # → Embedding-Analyse & Outlier Detection
│   └── intent_selector.py        # → Intent-Erkennung & semantisches Routing
│   └── duplicate_remover.py      # → Duplikat-Entferner für interactions.json
├── tests/                        # → Unittests (aktuell in Planung)
├── README.md                     # → Projektbeschreibung & Setup
```

---

## 🧠 Kernkomponenten

### 1. RLHF-Engine (Reinforcement Learning from Human Feedback)
- **Replay Buffer:** Prioritized Experience Replay (PER) mit TD-Error als Priorität.
- **TD-Berechnung:** Simple Q-Learning-Ansatz (Plan: Ausbau zu DDQN + LSTM).
- **Feedback-Integration:** Positive/negative User-Bewertungen steuern die Reward-Logik.
- **Belohnungsberechnung:**  
  - Manuelles Feedback: `Daumen hoch/runter`
  - Geplante Erweiterung: Automatisierte Rewards via semantisches Matching, Confidence, Embedding-Distanz.

---

## 💬 Dialogsystem & GPT-Integration

- GPT-3.5-Turbo Integration für dynamische Antworten.
- Kontextlogik: Übergabe der letzten 10 relevanten Interaktionen.
- System-Prompt unterstützt:
  - Situativen Stil
  - Höflichen Widerspruch
  - Anpassung an Emoji-Stimmung und User-Präferenzen (z. B. Lieblingsfarbe)

---

## 🧩 Zusätzliche Module

| Modul                    | Funktion                                |
|--------------------------|-----------------------------------------|
| `embedding_analyzer.py`   | Outlier Detection für Interaktionsdaten (VAE geplant) |
| `intent_selector.py`      | Skill-Routing auf Basis semantischer Analyse |
| `duplicate_remover.py`    | Entfernt doppelte Einträge aus `interactions.json`   |

---

## 🚀 Geplante Weiterentwicklung

- Deep Q-Network (DDQN) + LSTM Agent.
- Prioritized Experience Replay mit TD-Error und Zeitgewichtung.
- Outlier Filtering via Variational Autoencoder (VAE).
- Random Network Distillation (RND) zur Unsicherheitsmessung.
- Reward-Optimierung durch semantisches Matching & Confidence Scores.
- GUI-Feintuning (runde Sprechblasen, kleinere Icons).
- Reinforcement Learning from Human Feedback (RLHF) mit wachsendem Mitspracherecht des Bots.
- Persönliches Profiling via `user_insight.json`.

---

## 🧩 Zielbild

SymBro soll langfristig ein smarter, lernfähiger Desktop-Begleiter werden, der:
- Entscheidungen situativ und kontextabhängig trifft.
- Feedback aktiv in sein Lernverhalten einbezieht.
- Eine echte Mensch-KI-Symbiose anstrebt.
