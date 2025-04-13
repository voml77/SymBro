# SymBro – Dein smarter Desktop-Begleiter

SymBro ist ein intelligenter Desktop-Bot, der als digitaler Begleiter und "kleiner Bruder" für den Nutzer entwickelt wird. 

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
- Erste GUI-Struktur steht: 
  - Dynamischer Name im Header
  - Farblich angepasster Hintergrund
  - Links: Steuerungs-Icons (Farbauswahl & neuer Dialog)
  - Links unten: Chat-Übersicht
  - Rechts: Chat-Fenster
- Skill-System vorbereitet und eingebunden
- Datei-Handling Modul fertig implementiert
- Chat-Speicher-System vorbereitet:
  - Chat-Themen werden automatisch aus der ersten Nachricht generiert
  - Speicherung des Chat-Verlaufs in JSON-Dateien geplant
  - Kontext-Menü für das Löschen von Chats per Rechtsklick integriert

## Nächste Schritte (Plan für die kommenden Tage)

0. Fixing Chat-Speicher-System:
   - Sicherstellen, dass Chat-Dateien korrekt im Verzeichnis `data/chats/` gespeichert werden
   - Überprüfung und Optimierung der Speicherlogik in `memory.py` und `main_window.py`

1. GUI-Detailverfeinerung:
   - Dynamische Anpassung der GUI an Fenstergröße
   - Erste User-Dialog-Interaktion
   - Mini-Meme-Anzeige & visuelle User Experience verbessern

2. Integration NameSoul & Memory in GUI:
   - Lieblingsfarbe Abfrage und direkte Anpassung der GUI
   - Speicherung von User-Präferenzen über Memory-Modul

3. Erweiterung Skills:
   - File Handling in GUI verfügbar machen
   - Skill-Auswahl über GUI steuerbar machen

4. Start des SymBro-Dialogsystems:
   - Kontextsensitive Antworten
   - Vorbereitung auf OpenAI API Anbindung (später dynamische Dialoge)

5. Vorbereitungen für langfristige Features:
   - Diskussionslogik (Bayessches Theorem)
   - Modularer Ausbau für weitere Skills und User Interaction

## Lizenz

Dieses Projekt steht unter der MIT License. Es darf frei genutzt, verändert und geteilt werden — unter Angabe des ursprünglichen Autors.

## Autor

Designed & Developed by Vadim Ott  
GitHub: https://github.com/voml77/SymBro  

Dieses Projekt ist Teil einer persönlichen Vision:  
SymBro — mehr als nur ein Bot. Ein smarter Begleiter, der Individualität, Lernfähigkeit und Symbiose in den Mittelpunkt stellt.
