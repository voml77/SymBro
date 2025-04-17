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
- GUI-Design in gemeinsamer Mensch-KI-Symbiose stetig weiterentwickelt:
  - Dynamischer Name im Header
  - Farblich angepasstes Design (inkl. aktiver Chat-Hervorhebung)
  - Links: Interaktive Steuerungs-Icons (Farbe ändern, neuer Dialog, Markdown-Export)
  - Links unten: Chat-Übersicht mit Favoriten-Option
  - Rechts: Konversationsansicht mit Zeitstempeln und Eingabefeld
- Skill-System aktiv (Modularität vorbereitet)
- Datei-Handling Modul implementiert
- Chat-System:
  - Chat-Themen werden automatisch gespeichert
  - Favoritenstatus kann zugewiesen und gespeichert werden
  - Umbenennung von Chats per Doppelklick (dynamisch gespeichert)
  - Kontext-Menü: Chats löschen, Favoriten setzen/entfernen
- Markdown-Export mit eigenem Icon integriert: Exportiert aktuelle Konversation als `.md` in `data/exports/`

## Nächste Schritte (Plan für die kommenden Tage)

0. Fixes & Finetuning:
   - Verfeinerung der Chat-Speicherung & Favoriten-Logik
   - Fehlerfreies Handling von Duplikaten und Umbenennungen

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

6. Export- und Dateimanagement erweitern:
   - Markdown-Export verbessern (z.B. Zeitformatierung, Exportdialog)
   - Vorbereitung auf Drag & Drop Upload und Verarbeitung von Dateien im Chat

## Lizenz

Dieses Projekt steht unter der MIT License. Es darf frei genutzt, verändert und geteilt werden — unter Angabe des ursprünglichen Autors.

## Autor

Designed & Developed by Vadim Ott  
GitHub: https://github.com/voml77/SymBro  

Dieses Projekt ist Teil einer persönlichen Vision:  
SymBro — mehr als nur ein Bot. Ein smarter Begleiter, der Individualität, Lernfähigkeit und Symbiose in den Mittelpunkt stellt.
