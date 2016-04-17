__author__ = 'agentnola'

import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json


# I am so sorry JB, but Total War means TOTAL WAR

docKey = 'VoteCounter2-af942bc69325.json'
json_key = json.load(open(docKey))
docName = "English Bill Data Base"
sheetName = "Sheet1"
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
sh = gc.open(docName)
wks = sh.worksheet(sheetName)


def pull_bill_names(amount):
    bills = []
    for x in range(amount):
        cell = x + 1
        cellValue = wks.cell(cell,1)

        formattedValue = str(cellValue).split("'")
        billName = (formattedValue[1].rpartition("c. "))[0]
        print(billName)
        if billName not in bills:
            bills.append(billName)
    print(bills)
    return bills


def createDocument():
    billNames = pull_bill_names(1)
    bills = []
    for x in range(len(billNames)):
        billname = billNames[x]
        doc = billname+"""Repeal Bill 2016'

An act to repeal the"""+billname+ """
BE IT ENACTED by The Queen's most Excellent Majesty, by and with the advice and consent of the Commons in this present Parliament assembled, in accordance with the provisions of the Parliament Acts 1911 and 1949, and by the authority of the same, as follows:-

(1) Repeal

(a) """+billname+ """ shall be repealed.

(2) Commencement, Short Title & Extent

(a) This Act may be cited as the"""+billname+ """  Repeal Act 2016

(b) This bill shall come into effect immediately upon receiving Royal Assent.

(c) This bill will apply to the United Kingdom of Great Britain and Northern Ireland.

---

Submitted by (The 1st Baron of New Galloway MBE)[/u/agentnola]
"""
        text_file = open(billname +" Repeal Bill.txt","w")
        text_file.write(doc)
        text_file.close()



createDocument()