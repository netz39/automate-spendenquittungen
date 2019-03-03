#! /usr/bin/env python3

import argparse
import json
import os

import pandas
import pymysql.cursors
import datetime

parser = argparse.ArgumentParser(
    description='Create Spqndenquittung json files from jameica bookkeeping system')
parser.add_argument('jameicaJSON', type=str, nargs=1,
                    help='JSON file containing bookkeeping config')
parser.add_argument('listDonorsJSON', type=str, nargs=1,
                    help='JSON file containing data on the donors (names, adresses, year)')

args = parser.parse_args()

try:
    listDonors = json.load(open(os.path.abspath(args.listDonorsJSON[0])))
except Exception as e:
    print(e)
    exit(1)
try:
    jameica = json.load(open(os.path.abspath(args.jameicaJSON[0])))
except Exception as e:
    print(e)
    exit(1)


con = pymysql.connect(host=jameica['dbHost'],
                      user=jameica['dbUser'],
                      password=jameica['dbPass'],
                      db=jameica['dbName'],
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)

acc = pandas.read_sql('select * from konto', con)
trans = pandas.read_sql('select * from buchung', con)
by_id = int(pandas.read_sql(
    'select id from geschaeftsjahr where beginn like "{}-%"'.format(listDonors["year"]), con).id)

for donor in listDonors['donors']:
    # file to save info to
    fname = '{year}.{name}.json'.format(
        year=listDonors['year'], name=donor['Name'])

    try:
        donor_id = int(acc[acc.name.astype('str') ==
                           'Kreditor - ' + donor['Name']].id)
    except Exception:
        print('Donor {name} not found, continuing.'.format(name=donor['Name']))
        continue
    # transactions coming from 'Spenden*' or 'Mitgliedsbeiträge'
    donationAccIDs = list(acc[acc.name.str.contains('Spenden')].id)
    membershipAccIDs = list(acc[acc.name.str.contains('Mitgliedsbeiträge')].id)
    tx_idx_source = trans.habenkonto_id.isin(donationAccIDs + membershipAccIDs)
    tx_idx_donor = trans.sollkonto_id == donor_id
    tx_idx_year = trans.geschaeftsjahr_id == by_id
    tx_idx_valid = tx_idx_source & tx_idx_donor & tx_idx_year
    validTxs = trans[tx_idx_valid]

    transactionList = []
    for idx, tx in validTxs.iterrows():
        txDict = dict()
        txDict['Datum'] = tx.datum.isoformat()
        if tx.habenkonto_id in membershipAccIDs:
            txDict['Art'] = "Mitgliedsbeitrag"
        else:
            txDict['Art'] = "Geldzuwendung"
        txDict['VerzichtErstattung'] = "nein"
        txDict['Betrag'] = tx.betrag
        transactionList.append(txDict)
    donor['Betraege'] = sorted(transactionList, key=lambda tx: tx['Datum'])
    with open(fname, 'w') as fp:
        json.dump(donor, fp, indent=4, ensure_ascii=False)
