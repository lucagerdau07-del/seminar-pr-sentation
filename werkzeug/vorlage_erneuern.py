#!/usr/bin/env python3
"""Erneuert die Kopie der Seite, die in der Präsentation selbst steckt.

Die Präsentation enthält sich selbst noch einmal als Base64-Text (VORLAGE). Damit kann sie sich
als Artifact mit eigenen Fotos neu speichern. Nach jeder Änderung an der HTML-Datei muss diese
Kopie neu erzeugt werden, sonst stellt „In Präsentation speichern“ den alten Stand wieder her.

Aufruf:  python3 werkzeug/vorlage_erneuern.py [Percy_Julians_Forschungsweg.html]
"""
import base64
import sys

M_FOTOS, M_VORLAGE = '__FOTOS_JSON__', '__VORLAGE_B64__'
A_FOTOS, E_FOTOS = '\n  var EMBED = ', '; // fest eingebaute Bilder'
A_VORLAGE, E_VORLAGE = "\n  var VORLAGE = '", "'; // die Seite selbst"


def teile(text, anfang, ende):
    """Zerlegt text in (davor, wert, danach); der Wert steht zwischen anfang und ende."""
    if text.count(anfang) != 1:
        sys.exit('Stelle nicht eindeutig gefunden: ' + anfang.strip())
    a = text.index(anfang) + len(anfang)
    e = text.index(ende, a)
    return text[:a], text[a:e], text[e:]


def main():
    pfad = sys.argv[1] if len(sys.argv) > 1 else 'Percy_Julians_Forschungsweg.html'
    seite = open(pfad, encoding='utf-8').read()
    davor, fotos, rest = teile(seite, A_FOTOS, E_FOTOS)
    mitte, _, danach = teile(rest, A_VORLAGE, E_VORLAGE)
    vorlage = davor + M_FOTOS + mitte + M_VORLAGE + danach
    if vorlage.count(M_FOTOS) != 1 or vorlage.count(M_VORLAGE) != 1:
        sys.exit('Die Platzhalter kommen im Seitentext selbst vor. Bitte dort umschreiben.')
    b64 = base64.b64encode(vorlage.encode('utf-8')).decode('ascii')
    neu = davor + fotos + mitte + b64 + danach
    if neu == seite:
        print('Vorlage ist aktuell.')
    else:
        open(pfad, 'w', encoding='utf-8').write(neu)
        print('Vorlage erneuert.')


if __name__ == '__main__':
    main()
