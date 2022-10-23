# Pipeline



## Warum eine Pipeline zur Datenaufbereitung?

Um die Daten leichter unterscheidbar zu machen, so dass bessere Suchergebnisse und ein besseres Benutzererlebnis zu geschaffen werden kann, werden die Daten beim scrapen direkt interpretiert.

### Folgende Felder werden hinzugefügt:
* laufende Nummer
* Entropie (Mass für den Informationsgehalt)
* Wiener Sachtextformel (Lesbarkeitsindex,  gibt an, für welche Schulstufe ein Sachtext geeignet ist. Die Skala beginnt bei Schulstufe 4 und endet bei 15)
* Sentimentanalyse
* englische Keywords


### Verwendete Tools
* Textacy mit "de_core_news_lg" (Entropy und Wienersachtextformel)
* TextBlob für Sentimentanalyse
* ntlk zur Stopwordextraktion
* yake zur Keyword-Extraktion
* HannoverTagger, um Keywords zu Lemmatisieren
* Deutsch-Englisch Wörterbuch von freedict für selbst programmierte "Übersetzungsmaschine :raised_hands:" der Keyword-Lemmas

