#! /usr/bin/env python3

import argparse
import json
import os
import sys

import pandas
import pymysql.cursors

parser = argparse.ArgumentParser(
    description='Create Spendenquittung json files from jameica bookkeeping system')
parser.add_argument('jameicaJSON', type=str, nargs=1,
                    help='JSON file containing bookkeeping config')
parser.add_argument('outPath', type=str, nargs=1,
                    help='path to store the output files')
args = parser.parse_args()

try:
    listDonors = json.load(sys.stdin)
except Exception as e:
    print(e, file=sys.stderr)
    exit(1)
try:
    jameica = json.load(open(os.path.abspath(args.jameicaJSON[0])))
except Exception as e:
    print(e, file=sys.stderr)
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
    f"select id from geschaeftsjahr where beginn like '{listDonors['year']}-%'", con).id)

for donor in listDonors['donors']:
    # file to save info to
    fname = f"{args.outPath[0]}{listDonors['year']}.{donor['name'].strip()}.json"

    try:
        donor_id = int(acc[acc.name.astype('str') ==
                           'Kreditor - ' + donor['name'].strip()].id)
    except Exception:
        print(f"Donor {donor['name'].strip()} not found, continuing.", file=sys.stderr)
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
