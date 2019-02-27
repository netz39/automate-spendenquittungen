#! /usr/bin/env python3

import argparse
import json
import os

import pandas
import pymysql.cursors
import datetime

parser = argparse.ArgumentParser(
    description='Create Spqndenquittung json files from jameica bookkeeping system')
parser.add_argument('jameicaJson', type=str, nargs=1,
                    help='JSON file containing bookkeeping config')
parser.add_argument('jsonListDonors', type=str, nargs=1,
                    help='JSON file containing data on the donors (names, adresses, year)')

args = parser.parse_args()

try:
    listDonors = json.load(open(os.path.abspath(args.jsonListDonors[0])))
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
by = pandas.read_sql('select * from geschaeftsjahr', con)
by_id = int(by[by.beginn.astype('str').contains(listDonors['year'])].id)
for donor in listDonors['donors']:
    # file to save info to
    # acc_id
    donor_id = getAccIdByName(donor['name'], acc)
    # transactions coming from 'Spenden*' or 'Mitgliedsbeiträge'
    sourceIDs = list(acc[acc.name.str.contains('Spenden') | acc.name.str.contains('Mitgliedsbeiträge')].id) 
    transactions = trans[trans.habenkonto_id.isin(sourceIDs) & trans.sollkonto == donor_id]

def getAccIdByName(name: str, acc: pandas.DataFrame):
    try:
        return int(acc[acc.name.astype('str') == 'Kreditor - ' + name].id)
    except Exception:
        return 0