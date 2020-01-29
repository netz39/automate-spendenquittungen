# Service zur Erstellung von Spendenquittungen

- Unterscheidung Einzelbestätigung, Sammelbestätigung
- [Link zum Bundesministerium der Finanzen](https://www.formulare-bfinv.de/ffw/content.do)
  - Steuerformulare -> G -> Gemeinnützigkeit -> 60 - 

## 1. Schritt

- JSON mit den relevanten Daten -> XML, das vom Finanzministerium gefressen wird

## 2. Schritt

- Automatisierung der PDF-Erstellung
- https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
- `pip install selenium requests`


## 3. Schritt
- Automatisierung der Erstellung des JSON aus der Buchhaltungsdatenbank

## Installation

python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
Install chromium: sudo apt install chromium-browser 
Install chromedriver: https://chromedriver.chromium.org/home

## Benutzung
```bash
find netz39/2018 -name "*.json" -exec  python3 json2xml.py netz39/netz39.json {} \;
find . -name "*.json.xml" -exec  python3 xml2pdf.py {} \;        
lp -d <printer name> *.pdf
```