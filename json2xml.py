#! /usr/bin/env python3

import json
import xml.etree.ElementTree as ET
import argparse
import os
from sys import exit
from num2str import num2str
import datetime
import xmltemplates

# templates und ersetzen oder lieber XML dokument komplett programmatisch bauen
parser = argparse.ArgumentParser(description='Convert JSON organization and donor files to XML Spendenquittungen')
parser.add_argument('jsonOrganization', type=str, nargs=1, help='JSON file containing data on the organization')
parser.add_argument('jsonDonor', type=str, nargs=1, help='JSON file containing data on the donor')

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

savePath = args.jsonDonor[0] + 'xml'

def isSingleDonation(dictDonor: dict) -> bool():
    return not 'Betraege' in dictDonor.keys()

def createSingleDonationString(dictOrganization: dict, dictDonor: dict):
    et = ET.XML(xmltemplates.templateXMLsingle)
    et.find('aussteller').text = '{0}\n{1} {2}\n{3} {4}'.format(
        dictOrganization['Name'], 
        dictOrganization['Strasse'],
        dictOrganization['Hausnummer'],
        dictOrganization['PLZ'],
        dictOrganization['Stadt']
    )
    et.find('k3').text = dictOrganization['checkboxWegenFoerderung']
    et.find('k4').text = dictOrganization['checkBoxEinhaltung']
    et.find('zwecke').text = '\n'.join(dictOrganization['Zwecke'])
    et.find('zwecke2b2').text = '\n'.join(dictOrganization['Zwecke'])
    et.find('stnr2').text = dictOrganization['SteuerbescheidNummer']
    et.find('finamt2').text = dictOrganization['Finanzamt']
    et.find('datum3').text = dictOrganization['SteuerbescheidDatum']
    et.find('k5').text = dictOrganization['checkboxEstg']
    et.find('ort_datum').text = '{0}, {1}'.format(
        dictOrganization['Stadt'],
        datetime.date.today().strftime('%d.%m.%Y')
    )

    et.find('name').text = '{0}\n{1} {2}\n{3} {4}'.format(
        dictDonor['Name'], 
        dictDonor['Strasse'],
        dictDonor['Hausnummer'],
        dictDonor['PLZ'],
        dictDonor['Stadt']
    )
    et.find('wert').text = dictDonor['Betrag']
    et.find('wert2').text = num2str(dictDonor['Betrag'])
    et.find('datum').text = dictDonor['ZuwendungsBeginn']
    
    if dictDonor['VerzichtErstattung']:
        et.find('k1').text = 'true'
        et.find('k2').text = 'false'
    else:
        et.find('k1').text = 'false'
        et.find('k2').text = 'true'
    return et

def createMultiDonationString(dictOrganization: dict, dictDonor: dict):
    et = ET.parse(xmltemplates.templateXMLmulti)
    et.find('aussteller').text = '{0}\n{1} {2}\n{3} {4}'.format(
        dictOrganization['Name'], 
        dictOrganization['Strasse'],
        dictOrganization['Hausnummer'],
        dictOrganization['PLZ'],
        dictOrganization['Stadt']
    )
    et.find('k3').text = dictOrganization['checkboxWegenFoerderung']
    et.find('k4').text = dictOrganization['checkBoxEinhaltung']
    et.find('zwecke').text = '\n'.join(dictOrganization['Zwecke'])
    et.find('zwecke2b2').text = '\n'.join(dictOrganization['Zwecke'])
    et.find('stnr2').text = dictOrganization['SteuerbescheidNummer']
    et.find('finamt2').text = dictOrganization['Finanzamt']
    et.find('datum3').text = dictOrganization['SteuerbescheidDatum']
    et.find('k5').text = dictOrganization['checkboxEstg']
    et.find('ort_datum').text = '{0}, {1}'.format(
        dictOrganization['Stadt'],
        datetime.date.today().strftime('%d.%m.%Y')
    )

    et.find('name').text = '{0}\n{1} {2}\n{3} {4}'.format(
        dictDonor['Name'], 
        dictDonor['Strasse'],
        dictDonor['Hausnummer'],
        dictDonor['PLZ'],
        dictDonor['Stadt']
    )
    et.find('datum').text = dictDonor['ZuwendungsBeginn']
    et.find('datum4').text = dictDonor['ZuwendungsEnde']

    totalAmount = 0
    numBetraege = 0 
    for betrag in dictDonor['Betraege']:
        totalAmount = totalAmount + float(betrag['Betrag'])
        numBetraege = numBetraege + 1
        datarow = ET.SubElement(et.find('Betraege'),'datarow')
        ET.SubElement(datarow, 'element', attrib={'id':'ID_LINE'}).text = numBetraege
        ET.SubElement(datarow, 'element', attrib={'id':'dat1'}).text = betrag['Datum']
        ET.SubElement(datarow, 'element', attrib={'id':'art'}).text = betrag['Art']
        ET.SubElement(datarow, 'element', attrib={'id':'ja_nein'}).text = betrag['VerzichtErstattung']
        ET.SubElement(datarow, 'element', attrib={'id':'betrag1'}).text = betrag['Betrag']

    et.find('wert').text = '{0:.2f}'.format(totalAmount)
    et.find('wert2').text = '{0} Euro und {1} Cent'.format(
        num2str(int(totalAmount)),
        num2str(100*(totalAmount - int(totalAmount)))
    )
    
    return et

if isSingleDonation(dictDonor):
    xmlTree = createSingleDonationString(dictVerein, dictDonor)
else:
    xmlTree = createMultiDonationString(dictVerein, dictDonor)

print(savePath)

xmlTree.write(open(savePath, 'w'))