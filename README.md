# SymBro – Dein smarter Desktop-Begleiter

SymBro ist ein intelligenter Desktop-Bot, der als digitaler Begleiter und "kleiner Bruder" für den Nutzer entwickelt wird. Perspektivisch soll SymBro aus Nutzerverhalten lernen (RLHF) und Entscheidungen auf Basis menschlichen Feedbacks priorisieren.

## Ziel des Projekts
Im Zentrum stehen Individualität, Lernfähigkeit und eine symbiotische Beziehung zum User — mit echtem Mitspracherecht und Persönlichkeit. SymBro unterstützt den Nutzer nicht nur bei alltäglichen Aufgaben, sondern lernt kontinuierlich dazu und entwickelt dabei eine eigene Identität.

## Hauptfunktionen
- Personalisierte Namensgebung durch das NameSoul-Modul
- Datei-Handling: Öffnen, Bearbeiten und Speichern von Dateien
- Lernfähiges Memory-System für User-Gewohnheiten
- Höfliches Widerspruchs- und Diskussionssystem basierend auf Wahrscheinlichkeiten (z.B. Bayessches Theorem)
- Adaptive Kommunikation mit wachsendem Mitspracherecht

## Projektstruktur

```
SymBro/
├── core/               # Hauptlogik & Engine
├── modules/            # Erweiterungen, Skills, NameSoul
├── data/               # Lokale Daten (Memory, User-Profile)
├── utils/              # Hilfsfunktionen
├── tests/              # Unit Tests
├── main.py             # Einstiegspunkt
├── requirements.txt    # Python Abhängigkeiten
├── .gitignore
├── README.md
```

## API Key Konfiguration

Für die Nutzung der OpenAI API (z.B. zur Namensgenerierung im NameSoul-Modul) muss ein OpenAI API Key als Umgebungsvariable gesetzt werden.

Beispiel:

Linux / macOS Terminal:

export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

Alternativ kann auch eine `.env` Datei genutzt werden mit folgendem Inhalt:

OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Status
Projektstart: Tag 1 – Architektur und Modulplanung
Ziel: Prototyp innerhalb von 14 Tagen

## Aktueller Stand

- Migration der GUI auf PySide6 erfolgreich abgeschlossen
- GUI-Design in gemeinsamer Mensch-KI-Symbiose stetig weiterentwickelt:
  - Dynamischer Name im Header
  - Farblich angepasstes Design (inkl. aktiver Chat-Hervorhebung)
  - Aktuell gewählte Lieblingsfarbe wird beim Start aus `identity.json` geladen
  - Farbwahl kann jederzeit geändert werden und wird dauerhaft gespeichert
  - Links: Interaktive Steuerungs-Icons (Farbe ändern, neuer Dialog, Markdown-Export)
  - Links unten: Chat-Übersicht mit Favoriten-Option
  - Rechts: Konversationsansicht mit Zeitstempeln und Eingabefeld
  - Nachrichten werden in moderner Sprechblasen-Optik dargestellt
  - Benutzer- und Elias-Nachrichten farblich differenziert
  - Drag & Drop sowie Datei-Upload über Plus-Icon möglich
  - Uploads werden in `data/uploads/` gespeichert
  - Markdown-Export auch über Button im Eingabefeld verfügbar
  - Weitere GUI-Verbesserungen wie runde Sprechblasen und kleinere Icons in Planung
- Skill-System aktiv (Modularität vorbereitet)
- Datei-Handling Modul implementiert
- Chat-System:
  - Chat-Themen werden automatisch gespeichert
  - Favoritenstatus kann zugewiesen und gespeichert werden
  - Umbenennung von Chats per Doppelklick (dynamisch gespeichert)
  - Kontext-Menü: Chats löschen, Favoriten setzen/entfernen
  - Zeitstempel für jede Nachricht im Format (HH:MM)
- Markdown-Export mit eigenem Icon integriert: Exportiert aktuelle Konversation als `.md` in `data/exports/`
- GPT-Integration aktiv:
  - Nachrichten werden direkt an GPT-3.5-Turbo gesendet
  - System-Prompt wurde angepasst: Elias darf höflich widersprechen und passt sich dem Stil des Users an
  - Kontextlogik integriert: Es werden nur die letzten 10 relevanten Nachrichten übergeben

## Nächste Schritte (konkretisierter Plan ab Tag 11)

0. Fixes & Feinschliff:
   - Vermeidung von Chat-Duplikaten (Titelprüfung)
   - Korrekte Löschung aus `chats.json` beim Entfernen eines Chats

1. Dialogsystem aktiv:
   - GPT-Dialogsystem ist eingebunden und funktioniert stabil
   - Kontextlogik zur Begrenzung auf letzte 10 Nachrichten implementiert
   - System-Prompt erlaubt höflichen Widerspruch

2. Eingabemodi erweitern:
   - Plus-Icon mit Upload-Trigger vollständig verknüpfen
   - Drag & Drop optional erweitern (Anzeige & Feedback im UI)

3. Zusatzoptionen im Chat:
   - Chat als Markdown exportieren
   - Favoriten verwalten & farblich hervorheben

4. RLHF-Integration (Grundsystem aktiv):
   - Speicherung von User-Feedback vorbereiten
   - Startpunkt für spätere Bewertungssysteme
   - Feedback-Buttons (Daumen hoch/runter) im Chat eingefügt
   - Klicks auf Buttons aktualisieren automatisch den RLHF-Reward in `interactions.json`
   - RLHF-Engine speichert Zustand, Aktion, Reward und nächste Antwort zur späteren Modellierung
   - Visualisierung der Buttons verbessert: kleinere Darstellung, direkte Positionierung unter Elias' Antwort
   - Trainingsroutine mit Prioritized Experience Replay (PER) eingebaut
   - ReplayBuffer speichert automatisch Reward-Feedback mit TD-Fehler als Priorität
   - Automatisches On-the-fly-Training bei jeder Reward-Vergabe
   - Fehlerbehandlung im Buffer-Training eingebaut (z. B. zu wenig Daten, falsche Typen)
   - Reward-Zusammenfassung & interaktive Nachbewertung via Konsole implementiert
   - Leeren des Logs per Kommando möglich für gezielten Neuanfang

5. GUI finalisieren:
   - Eingabefeld & Button-Alignment perfektionieren
   - Sprechblasen-Design weiter verfeinern
   - Runde Sprechblasen implementieren
   - Icons in Nachrichten verkleinern und visuell einbinden
   - Optional: Chat-Hintergrund mit Verlauf oder Muster versehen

## Lizenz

Dieses Projekt steht unter der MIT License. Es darf frei genutzt, verändert und geteilt werden — unter Angabe des ursprünglichen Autors.

## Autor

Designed & Developed by Vadim Ott  
GitHub: https://github.com/voml77/SymBro  

## Trainingsphase ab Tag 14

SymBro wird ab sofort mit bewerteten Nutzerdialogen trainiert – Ziel: ein smarter, interaktiver Desktop-Begleiter mit echtem Lerneffekt.  
Die ersten 50 bewusst bewerteten Interaktionen bilden das Fundament für ein individuelles, responsives Verhalten.  
Elias lernt – in enger Symbiose mit dem User.  

Dieses Projekt ist Teil einer persönlichen Vision:  
> Am heutigen Tag wurde die erste Version des RLHF-Systems aktiviert – inklusive Reward-Logging und Feedback-Mechanismus 🧠✨  
SymBro — mehr als nur ein Bot. Ein smarter Begleiter, der Individualität, Lernfähigkeit und Symbiose in den Mittelpunkt stellt.

## Fortschritt Tag 15+

- RLHF-Trainingsloop erfolgreich abgeschlossen mit über 90 bewerteten Interaktionen
- Trainingsroutine mit `train_rlhf.py` ausgelagert für wiederholbare Agent-Updates
- Prioritized ReplayBuffer vollständig integriert und funktionstüchtig
- TD-Fehler werden korrekt berechnet und zur Priorisierung verwendet
- Agent erkennt und unterscheidet bereits differenzierte Belohnungswerte (z. B. 0.8 vs. -0.3)
- Wrapper `apply_td_errors_to_buffer()` in `rlhf_engine.py` integriert für zentrales Prioritäts-Update
- Erste spürbare Lernkurven erkennbar – Q-Werte entwickeln sich mit Variabilität im Feedback
- Fragenkatalog mit 20 realistischen, offen bewertbaren Gesprächsszenarien erstellt und verwendet
- Training und Bewertung erfolgen vollständig interaktiv und on-the-fly
- System vollständig vorbereitet für langfristige Verhaltensdifferenzierung & Lernen durch Feedback

## Fortschritt Tag 16

- Feedback-Logik erweitert: Bewertung über Daumen hoch/runter speichert nun `"PENDING_POSITIV"` bzw. `"PENDING_NEGATIV"` statt fixer numerischer Werte
- Neue Bewertungsstrategie:
  - `"PENDING_POSITIV"` wird beim nächsten Start zu `0.1`
  - `"PENDING_NEGATIV"` wird zu `-0.1`
  - `"PENDING"` wird zu `0.0`, falls nicht manuell bewertet
- Manuelle Nachbewertung über `summarize_log_rewards()` möglich (interaktive CLI)
- Funktion `summarize_log_rewards()` überarbeitet:
  - Zählt positive & negative Bewertungen separat
  - Erkennt neue PENDING-Typen und wandelt sie differenziert um
- Ziel: differenzierte Reward-Zwischenlösung bis zur Einführung des DDQN-Systems
- Vorbereitung für Setup-Wizard (zukünftig): automatische Initialbefragung zur Erstellung von `user_insight.json`

---

## Fortschritt Tag 18

- Semantische Skill-Erkennung implementiert:
  - Einführung eines `intent_selector.py` auf Basis von `sentence-transformers`
  - Elias erkennt jetzt automatisch, welcher Skill (z. B. `reflect_on_user`, `gpt_chat`, `joke_skill`) dem Nutzerinput semantisch entspricht
  - Cosine Similarity als Entscheidungsgrundlage, mit lernfähiger Schwelle
  - Skill-Auswahl ersetzt hartkodierte Abfragen durch vektorbasierte Entscheidungslogik
- Embeddings für Beispielintentionen werden beim ersten Start erzeugt und lokal gespeichert (`data/embeddings/`)
- Lazy Loading des Transformer-Modells zur Beschleunigung des Programmstarts
- Vorbereitungen für langfristige Intention Classification und RL-basiertes Skill-Routing (vorgemerkt)
- Technisches Feedback auf macOS vollständig behandelt:
  - CPU/GPU-Autoerkennung für Embeddings
  - Tokenizer-Warnungen werden künftig unterdrückt (geplant)
- Kontextuelles Denken („Was hast du über mich gelernt?“ → Reflexion) wird semantisch und adaptiv umgesetzt
