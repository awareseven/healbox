# healbox

Die healBox ist ein Low-Tech Projekt. Sie soll Privatpersonen, Einzelunternehmern und kleinen Betrieben beziehungsweise Organisationen helfen, sich vor aktuellen Schadsoftware-Wellen zu schützen.

## Notwendige Hardware

Die healBox kann mit vorhandenem Equipment und günstiger Hardware auch von Laien in Betrieb genommen werden. Alles was Sie brauchen ist in der folgenden Liste aufgeführt und ist ab 105 Euro zusammen zu kaufen, wenn keine Hardware vorhanden ist. 

* Raspberry Pi Model 3 oder 4 (~35 Euro)
* SD Karte mit vorinstalliertem Raspbian (~ 10 Euro)
* Maus und Tastatur mit USB-Anschluss (~15 Euro)
* Bildschirm mit HMDI Ausgang ( ab 40 Euro oder vorhanden)
* HDMI-Kabel (5 Euro)

Um die healBox in Betrieb zu nehmen muss der Raspberry Pi mit dem Stromnetz verbunden werden und die SD Karte eingelegt werden. Maus, Tastatur und Bildschirm werden an die entsprechenden Anschlüsse gesteckt und der Pi gestartet. Anschließend loggen Sie sich mit dem Nutzername "pi" und der Passwort "raspberry" ein. Anschließend befolgen Sie die untenstehenden Setup-Anweisungen.

## Setup

- Öffnen Sie das Terminal des Pi's und geben Sie folgenden Befehl ein:
` git clone https://github.com/awareseven/healbox `
- Anschließend geben Sie folgenden Befehl ein:
` cd healbox `
- Danach geben Sie folgenden Befehl ein:
`sudo ./healbox.sh`
Wenn Sie nach dem Passwort gefragt werden, tippen Sie "raspberry" ein.
- Folgen Sie der Installation und geben Sie an den entsprechenden Stellen Informationen ein, beispielweise Ihr neues Passwort.



Verwendetes Raspbian Image: 2019-07-10-raspbian-buster.img

Das Skript healbox.sh nimmt Veränderungen an der Standard Installation vor:

* Bluetooth wird deaktiviert
* Setzen eines neuen Hostname
* Zusätzliche Pakete werden entfernt
* Automatische Anmelden am System ist deaktiviert
* Login für root gesperrt
* Neuer Nutzer wird angelegt und Nutzer pi am folgenden Tag gesperrt
* sudo muss mit Password genutzt werden
* Upgrades der installierten Pakete werden automatisch installiert 
* Firewall eingerichtet
* SSH entfernt
* Thunderbird und Libreoffice werden installiert
* Thunderbird startet automatisch nach dem Einloggen
