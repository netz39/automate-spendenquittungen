#! /usr/bin/env python3

import argparse
import json
import os
import pymysql.cursors

parser = argparse.ArgumentParser(
    description='Create Spqndenquittung json files from jameica bookkeeping system')
parser.add_argument('jameicaJson', type=str, nargs=1,
                    help='JSON file containing data on the bookkeeping system')
parser.add_argument('jsonListDonors', type=str, nargs=1,
                    help='JSON file containing data on the donors (names, adresses, year)')

args = parser.parse_args()
