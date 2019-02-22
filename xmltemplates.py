#! /usr/bin/env python3

templateXMLsingle = '<?xml version="1.0" encoding="UTF-8"?> \
<xml-data xmlns="http://www.lucom.com/ffw/xml-data-1.0.xsd">\
	<form>catalog://Steuerformulare/gemein/034122</form>\
	<instance>\
		<datarow>\
			<element id="aussteller">Musterverein\
Musterstraße 1\
12345 Musterstadt</element>\
			<element id="name">Max Mustermann\
Musterstraße 1\
12345 Musterstadt</element>\
			<!-- Zuwendungsbetrag -->\
			<element id="wert">100,00</element>\
			<element id="wert2">einhundert</element>\
			<!-- Datum der Zuwendung -->\
			<element id="datum">01.1.1970 00:00:00</element>\
			<!-- Verzicht auf die Erstattung von Aufwendungen? Ja -->\
			<element id="k1">false</element>\
			<!-- Verzicht auf die Erstattung von Aufwendungen? Nein -->\
			<element id="k2">true</element>\
			<!-- Wir sind wegen Förderung... -->\
			<element id="k3">false</element>\
			<!-- Die Einhaltung der satzungsmäßigen Voraussetzungen -->\
			<element id="k4">true</element>\
			<element id="zwecke">Musterzweck 1\
Musterzweck 2</element>\
			<element id="stnr2">000/000/00000</element>\
			<element id="finamt2">Musterstadt</element>\
			<element id="datum3">01.01.1970 00:00:00</element>\
			<element id="zwecke2b2">Musterzweck 1\
Musterzweck 2</element>\
			<element id="k5">false</element>\
			<!-- Ausstellungsdatum/Ort -->\
			<element id="ort_datum">Musterstadt, 01.01.1970</element>\
		</datarow>\
	</instance>\
</xml-data>'

templateXMLmulti = '<?xml version="1.0" encoding="UTF-8"?>\
<xml-data xmlns="http://www.lucom.com/ffw/xml-data-1.0.xsd">\
	<form>catalog://Steuerformulare/gemein/034132</form>\
	<instance>\
		<datarow>\
			<element id="aussteller">Musterverein\
Musterstraße 1\
12345 Musterstadt</element>\
			<element id="name">Max Mustermann\
Musterstraße 1\
12345 Musterstadt</element>\
			<element id="gesamtsumme">60.00</element>\
			<element id="wert2">sechzig</element>\
			<!-- Zuwendungsbeginn/Ende -->\
			<element id="datum">01.01.1970 00:00:00</element>\
			<element id="datum4">01.12.1970 00:00:00</element>\
			<!-- Wir sind wegen Förderung... -->\
			<element id="k3">false</element>\
			<!-- Die Einhaltung der satzungsmäßigen Voraussetzungen -->\
			<element id="k4">true</element>\
			<element id="zwecke">Musterzweck 1\
Musterzweck 2</element>\
			<element id="stnr2">000/000/00000</element>\
			<element id="finamt2">Musterstadt</element>\
			<element id="datum3">01.06.1970 00:00:00</element>\
			<element id="zwecke2b2">Musterzweck 1\
Musterzweck 2</element>\
			<element id="k5">false</element>\
			<!-- Ausstellunsort/Datum -->\
			<element id="ort_datum">Musterstadt, 01.01.1970</element>\
		</datarow>\
		<dataset id="betraege">\
			<datarow>\
				<element id="ID_LINE">1</element>\
				<element id="dat1">01.01.1970 00:00:00</element>\
				<element id="art">Mitgliedsbeitrag</element>\
				<element id="ja_nein">nein</element>\
				<element id="betrag1">30.00</element>\
			</datarow>\
			<datarow>\
				<element id="ID_LINE">2</element>\
				<element id="dat1">01.04.1970 00:00:00</element>\
				<element id="art">Mitgliedsbeitrag</element>\
				<element id="ja_nein">nein</element>\
				<element id="betrag1">30.00</element>\
			</datarow>\
		</dataset>\
	</instance>\
</xml-data>'