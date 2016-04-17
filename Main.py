__author__ = 'agentnola'
import praw
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json


# I am so sorry JB, but Total War means TOTAL WAR

docKey = 'KillTheHouseOfLords.json'
json_key = json.load(open(docKey))
docName = "English Bill Data Base"
sheetName = "Sheet1"
scope = ['https://spreadsheets.google.com/feeds']
r = praw.Reddit('Lord Killer v1')
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
sh = gc.open(docName)
wks = sh.worksheet(sheetName)


def is_done(wks,row):
    value = wks.cell(row,2)
    if "Posted" in str(value):
        return True
    else:
        return False


def pull_bill_names(amount):
    bills = []
    counter = 0
    row = 1
    while counter <= amount-1:

        cell_value = wks.cell(row,1)
        print(is_done(wks,row))
        if is_done(wks,row) is False:
            formatted_value = str(cell_value).split("'")
            bill_name = (formatted_value[1].rpartition("c. "))[0]
            wks.update_cell(row, 2, "Posted")
            print(bill_name)
            if bill_name not in bills:
                bills.append(bill_name)
                counter += 1
        row += 1

    print(bills)
    return bills


def createDocument(amount):
    billNames = pull_bill_names(amount)
    bills = []
    for x in range(len(billNames)):
        billname = billNames[x]
        doc = "     **"+billname+"""Repeal Bill 2016.**

    An act to repeal the """+billname+ """


    *BE IT ENACTED by The Queen's most Excellent Majesty, by and with the advice and consent of the Commons in this present Parliament assembled, in accordance with the provisions of the Parliament Acts 1911 and 1949, and by the authority of the same, as follows:-*

    (1) Repeal

    (a) """+billname+ """ shall be repealed.

    (2) Commencement, Short Title & Extent

    (a) This Act may be cited as the"""+billname+ """  Repeal Act 2016

    (b) This bill shall come into effect immediately upon receiving Royal Assent.

    (c) This bill will apply to the United Kingdom of Great Britain and Northern Ireland.

    ---

    Submitted by [The 1st Baron of New Galloway MBE](/u/agentnola)
"""

        bills.append(doc)
    return bills


def reddit():
    r.login("","")
    bills = createDocument(10)
    for x in range(len(bills)):
        title = bills[x].split("\n")[0]
        print(title)
        r.send_message("/r/mhollegislation",title,bills[x])

