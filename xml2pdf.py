#! /usr/bin/env python3

from time import sleep
import os.path
from sys import exit
import argparse
from selenium import webdriver
import requests
import shutil

parser = argparse.ArgumentParser(description='Convert xml Spendenquittungen to pdf Spendenquittungen')
parser.add_argument('infile', type=str, nargs=1, help='XML file to convert.')
args = parser.parse_args()

name, extension = os.path.splitext(args.infile[0])
if not os.path.isfile(name + extension):
    print('Error: File {} does not exists. Aborting.'.format(name + extension))
    exit(1)
pathToXML = os.path.abspath(name + extension)
savePath = os.path.abspath(name + '.pdf')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=options)

# open website
url='https://www.formulare-bfinv.de/ffw/action/invoke.do?id=Welcome'
driver.get(url)
# dismiss warning
driver.find_element_by_class_name('button').click()

# navigate to xmlupload
# link needs to be visible to be clicked
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
driver.find_element_by_link_text('XML Daten hochladen').click()

# click continue
driver.find_element_by_name('$action:next').click()

# add file
driver.find_element_by_name('dataFile').send_keys(pathToXML)

driver.find_element_by_name('$action:next').click()
driver.find_element_by_name('$action:finish').click()

# now we should be in the document view
# generate the pdf
driver.find_element_by_id('lip_toolbar_form:2fprint').click()
# it takes a second to generate the pdf, so we wait
sleep(1)

# selenium does not support downloading filestherefore we are
# using requests package with cookie injection to download the actual pdf
downloadlink = driver.find_element_by_link_text('PDF-Datei anzeigen').get_attribute('href')
selenium_cookies = driver.get_cookies()
session = requests.Session()
f = requests.utils.cookiejar_from_dict
for ck in selenium_cookies:
    for k in ck:
        ck[k] = str(ck[k])
    session.cookies.set(ck['name'],ck['value'])

response = session.get(downloadlink, stream=True)
with open(savePath, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

driver.close()