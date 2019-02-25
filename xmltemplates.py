#! /usr/bin/env python3

templateXMLsingle = '<?xml version="1.0" encoding="UTF-8"?> \n\
<xml-data xmlns="http://www.lucom.com/ffw/xml-data-1.0.xsd">\n\
	<form>catalog://Steuerformulare/gemein/034122</form>\n\
	<instance>\n\
		<datarow>\n\
			<element id="aussteller">$aussteller</element>\n\
			<element id="name">$name</element>\n\
			<!-- Zuwendungsbetrag -->\n\
			<element id="wert">$wert1</element>\n\
			<element id="wert2">$wert2</element>\n\
			<!-- Datum der Zuwendung -->\n\
			<element id="datum">$datum1</element>\n\
			<!-- Verzicht auf die Erstattung von Aufwendungen? Ja -->\n\
			<element id="k1">$k1</element>\n\
			<!-- Verzicht auf die Erstattung von Aufwendungen? Nein -->\n\
			<element id="k2">$k2</element>\n\
			<!-- Wir sind wegen Förderung... -->\n\
			<element id="k3">$k3</element>\n\
			<!-- Die Einhaltung der satzungsmäßigen Voraussetzungen -->\n\
			<element id="k4">$k4</element>\n\
			<element id="zwecke">$zwecke1</element>\n\
			<element id="stnr2">$stnr2</element>\n\
			<element id="finamt2">$finamt2</element>\n\
			<element id="datum3">$datum3</element>\n\
			<element id="zwecke2b2">$zwecke2b2</element>\n\
			<element id="k5">$k5</element>\n\
			<!-- Ausstellungsdatum/Ort -->\n\
			<element id="ort_datum">$ort_datum</element>\n\
		</datarow>\n\
	</instance>\n\
</xml-data>'

templateXMLmulti = '<?xml version="1.0" encoding="UTF-8"?>\n\
<xml-data xmlns="http://www.lucom.com/ffw/xml-data-1.0.xsd">\n\
	<form>catalog://Steuerformulare/gemein/034132</form>\n\
	<instance>\n\
		<datarow>\n\
			<element id="aussteller">$aussteller</element>\n\
			<element id="name">$name</element>\n\
			<element id="gesamtsumme">$gesamtsumme</element>\n\
			<element id="wert2">$wert2</element>\n\
			<!-- Zuwendungsbeginn/Ende -->\n\
			<element id="datum">$datum1</element>\n\
			<element id="datum4">$datum4</element>\n\
			<!-- Wir sind wegen Förderung... -->\n\
			<element id="k3">$k3</element>\n\
			<!-- Die Einhaltung der satzungsmäßigen Voraussetzungen -->\n\
			<element id="k4">$k4</element>\n\
			<element id="zwecke">$zwecke1</element>\n\
			<element id="stnr2">$stnr2</element>\n\
			<element id="finamt2">$finamt2</element>\n\
			<element id="datum3">$datum3</element>\n\
			<element id="zwecke2b2">$zwecke2b2</element>\n\
			<element id="k5">$k5</element>\n\
			<!-- Ausstellunsort/Datum -->\n\
			<element id="ort_datum">$ort_datum</element>\n\
		</datarow>\n\
		<dataset id="betraege">\n\
$betraege\n\
		</dataset>\n\
	</instance>\n\
</xml-data>'