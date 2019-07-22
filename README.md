# healbox

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