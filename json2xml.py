#! /usr/bin/env python3

import argparse
import datetime
import json
import os
from sys import exit

import xmltemplates
from num2str import num2str

parser = argparse.ArgumentParser(
    description='Convert JSON organization and donor files to XML Spendenquittungen')
parser.add_argument('jsonOrganization', type=str, nargs=1,
                    help='JSON file containing data on the organization')
parser.add_argument('jsonDonor', type=str, nargs=1,
                    help='JSON file containing data on the donor')

args = parser.parse_args()

try:
    dictVerein = json.load(open(os.path.abspath(args.jsonOrganization[0])))
except Exception as e:
    print(e)
    exit(1)
try:
    dictDonor = json.load(open(os.path.abspath(args.jsonDonor[0])))
except Exception as e:
    print(e)
    exit(1)

savePath = args.jsonDonor[0] + '.xml'


def isSingleDonation(dictDonor: dict) -> bool():
    return len(dictDonor['Betraege']) == 1


def createSingleDonationString(dictOrganization: dict, dictDonor: dict):
    template = xmltemplates.templateXMLsingle
    template = template.replace('$aussteller', '{0}\n{1} {2}\n{3} {4}'.format(
        dictOrganization['Name'],
        dictOrganization['Strasse'],
        dictOrganization['Hausnummer'],
        dictOrganization['PLZ'],
        dictOrganization['Stadt']
    ))
    template = template.replace(
        '$k3', dictOrganization['checkboxWegenFoerderung'])
    template = template.replace('$k4', dictOrganization['checkBoxEinhaltung'])
    template = template.replace(
        '$zwecke1', '\n'.join(dictOrganization['Zwecke']))
    template = template.replace(
        '$zwecke2b2', '\n'.join(dictOrganization['Zwecke']))
    template = template.replace(
        '$stnr2', dictOrganization['SteuerbescheidNummer'])
    template = template.replace('$finamt2', dictOrganization['Finanzamt'])
    template = template.replace(
        '$datum3', dictOrganization['SteuerbescheidDatum'])
    template = template.replace('$k5', dictOrganization['checkboxEstg'])
    template = template.replace('$ort_datum', '{0}, den {1}'.format(
        dictOrganization['Stadt'],
        datetime.date.today().strftime('%d.%m.%Y')
    ))

    template = template.replace('$name', '{0}\n{1} {2}\n{3} {4}'.format(
        dictDonor['Name'],
        dictDonor['Strasse'],
        dictDonor['Hausnummer'],
        dictDonor['PLZ'],
        dictDonor['Stadt']
    ))

    amount = float(dictDonor['Betraege'][0]['Betrag'])
    template = template.replace(
        '$wert1', '{0:.2f}'.format(amount))
    amountStr = '{0} Euro'.format(num2str(int(amount)))
    cents = int(100*(amount - int(amount)))
    if cents != 0:
        amountStr = amountStr + ' und {0} Cent'.format(num2str(cents))

    # amountStr must be at max 45 chars long, otherwise pdf generation fails
    amountStr = amountStr[:45]
    template = template.replace('$wert2', amountStr)
    dt = datetime.datetime.strptime(dictDonor['Betraege'][0]['Datum'], '%Y-%m-%d')
    template = template.replace('$datum1', dt.strftime('%d.%m.%Y %H:%M:%S'))

    if dictDonor['Betraege'][0]['VerzichtErstattung']:
        template = template.replace('$k1', 'true')
        template = template.replace('$k2', 'false')
    else:
        template = template.replace('$k1', 'false')
        template = template.replace('$k2', 'true')
    return template


def createMultiDonationString(dictOrganization: dict, dictDonor: dict):
    template = xmltemplates.templateXMLmulti
    template = template.replace('$aussteller', '{0}\n{1} {2}\n{3} {4}'.format(
        dictOrganization['Name'],
        dictOrganization['Strasse'],
        dictOrganization['Hausnummer'],
        dictOrganization['PLZ'],
        dictOrganization['Stadt']
    ))
    template = template.replace(
        '$k3', dictOrganization['checkboxWegenFoerderung'])
    template = template.replace('$k4', dictOrganization['checkBoxEinhaltung'])
    template = template.replace(
        '$zwecke1', '\n'.join(dictOrganization['Zwecke']))
    template = template.replace(
        '$zwecke2b2', '\n'.join(dictOrganization['Zwecke']))
    template = template.replace(
        '$stnr2', dictOrganization['SteuerbescheidNummer'])
    template = template.replace('$finamt2', dictOrganization['Finanzamt'])
    template = template.replace(
        '$datum3', dictOrganization['SteuerbescheidDatum'])
    template = template.replace('$k5', dictOrganization['checkboxEstg'])
    template = template.replace('$ort_datum', '{0}, {1}'.format(
        dictOrganization['Stadt'],
        datetime.date.today().strftime('%d.%m.%Y')
    ))

    template = template.replace('$name', '{0}\n{1} {2}\n{3} {4}'.format(
        dictDonor['Name'],
        dictDonor['Strasse'],
        dictDonor['Hausnummer'],
        dictDonor['PLZ'],
        dictDonor['Stadt']
    ))
    dt = datetime.datetime.strptime(
        dictDonor['Betraege'][0]['Datum'], '%Y-%m-%d')
    template = template.replace('$datum1', datetime.datetime(
        day=1, month=1, year=dt.year).strftime('%d.%m.%Y %H:%M:%S'))
    template = template.replace('$datum4', datetime.datetime(
        day=1, month=12, year=dt.year).strftime('%d.%m.%Y %H:%M:%S'))
    totalAmount = 0
    numBetraege = 0
    betraegeStr = ''
    for betrag in dictDonor['Betraege']:
        totalAmount = totalAmount + float(betrag['Betrag'])
        numBetraege = numBetraege + 1
        betraegeStr = betraegeStr + '\t\t\t<datarow>\n'
        betraegeStr = betraegeStr + \
            '\t\t\t\t<element id="ID_LINE">{0}</element>\n'.format(numBetraege)
        ds = datetime.datetime.strptime(
            betrag['Datum'], '%Y-%m-%d').strftime('%d.%m.%Y %H:%M:%S')
        betraegeStr = betraegeStr + \
            '\t\t\t\t<element id="dat1">{0}</element>\n'.format(
                ds)
        betraegeStr = betraegeStr + \
            '\t\t\t\t<element id="art">{0}</element>\n'.format(betrag['Art'])
        betraegeStr = betraegeStr + \
            '\t\t\t\t<element id="ja_nein">{0}</element>\n'.format(
                betrag['VerzichtErstattung'])
        betraegeStr = betraegeStr + \
            '\t\t\t\t<element id="betrag1">{0:.2f}</element>\n'.format(
                float(betrag['Betrag']))
        betraegeStr = betraegeStr + '\t\t\t</datarow>\n'
    template = template.replace('$betraege', betraegeStr)
    template = template.replace('$gesamtsumme', '{0:.2f}'.format(totalAmount))
    amountStr = '{0} Euro'.format(num2str(int(totalAmount)))
    cents = int(100*(float(totalAmount) - int(totalAmount)))
    if cents != 0:
        amountStr = amountStr + ' und {0} Cent'.format(num2str(cents))

    # amountStr must be at max 45 chars long, otherwise pdf generation fails
    amountStr = amountStr[:45]
    template = template.replace('$wert2', amountStr)

    return template


if isSingleDonation(dictDonor):
    foo = createSingleDonationString(dictVerein, dictDonor)
else:
    foo = createMultiDonationString(dictVerein, dictDonor)
with open(savePath, 'w') as outfile:
    outfile.write(foo)
