Daten für User bereitlegen/Dummy-Daten

Sicherheitsbackup erstellen vom Projekt

Dockercontainer für Ollama?

Stichwort Docker Modelrunnner

Moounten von Uni und Ollama


Abgabetemplate; 


Systemprompt-Rolle: Antworten nur anhand der Daten)=KI
User-Prompt= Prompt den wir eingeben.Zouia Alkurdi, an Alle, response = ollama.chat( model=modell_name, messages=[ { "role": "system", "content": ( "Du bist ein Assistent, der Fragen ausschließlich auf Grundlage des bereitgestellten Kontextes beantwortet. " "Wenn die Antwort nicht eindeutig im Kontext steht, antworte exakt mit: NOT_FOUND. " "Füge keine weiteren Informationen hinzu." ), }, { "role": "user", "content": _build_prompt(frage, kontext_text), }, ],, 16:40,
Zu einem Eintrag gelangen Sie mit den Pfeiltasten.


Kubernetis bis Samstag implementieren: 2 Service und 2 Deployment Dateien, einmal für Core und einmal für Ollama. Config-map.