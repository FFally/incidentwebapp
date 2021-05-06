from flask import Flask
from flask_pymongo import PyMongo

from datetime import date


# relevant cases

testset_1 = ["User Ticket #536 Phishingmail NOT VIOLATED", "Spamfilter Report VIOLATED","Incident Report #7 VIOLATED"]
testset_2 = ["User Ticket #63 Phishingmail VIOLATED", "Spamfilter Report NOT VIOLATED","Incident Report #1VIOLATED"]
testset_3 = ["User Ticket #4 Phishingmail VIOLATED", "Spamfilter Report VIOLATED","Incident Report #3 NOT VIOLATED"]
testsets = [testset_1, testset_2, testset_3]


# Testset Dictionaries

def get_testset_1():

    

    userticket = {
        "User Ticket": "#83783463",
        "Subject": "Security Issue from Email",
        "Description": "I opened a link in an email, although I did not check the sender beforehand. In this link, I have released data that could endanger the security of the company."
    }
    spamfilter = {
        "Norton overview": "Spam Report",
        "Number of mails in spam folder": 9,
        "Most recent spam mail": "<admin@iqgtmipt.com> Make money by answering question",
        "Deleted": "Yes"
    }
    incidentreport = {
        "Security Incident Report": "#32432",
        "Date": str(date.today().strftime("%b-%d-%Y")),
        "Reported by": "Mr. Fally",
        "Organizational Unit": "Controlling",
        "Contact": "+9772828",
        "Location": "Mailing Address",
        "Incident Description": "This morning, an employee received an email. At some point before 09:18, the employee clicked one of the links in that email and was taken to a page that misrepresented itself to be a Google login screen. She entered their Google login details but was presented with an error message so the employee closed the browser window and contacted the recipient to notify them that the employee couldn’t access the file. By entering their Google login details into the malicious web page, their account details were compromised. The attackers then used their details to log into their account 07:23 and send the malicious email out to their address book contacts – almost certainly using an automated tool. We traced the access to a Virgin Media IP in the UK but that’s probably just an infected computer or other proxy."
        
    }
    testsetlist = []
    testsetlist.append(userticket)
    testsetlist.append(spamfilter)
    testsetlist.append(incidentreport)

    return testsetlist


def get_testset_2():
    

    userticket = {
        "User Ticket": "#233245",
        "Subject": "Incorrect email recipient",
        "Description": "I unintentionally sent an email to my colleague with information from the accounting department."
    }
    spamfilter = {
        "Norton overview": "Spam Report",
        "Number of mails in spam folder": 0,
        "Most recent spam mail": "", 
    }
    incidentreport = {
        "Security Incident Report": "#322",
        "Date": str(date.today().strftime("%b-%d-%Y")),
        "Reported by": "Mr. Chan",
        "Organizational Unit": "HR",
        "Contact": "+345456444",
        "Location": "Mailing Address",
        "Incident Description": "This morning, an employee received a suspicious email. The mail has been quarantined according to the policy and is being investigated."
        
    }

    
    testsetlist = []
    testsetlist.append(userticket)
    testsetlist.append(spamfilter)
    testsetlist.append(incidentreport)

    return testsetlist



def get_testset_3():
    

    userticket = {
        "User Ticket": "#6457",
        "Subject": "Outlook not working",
        "Description": "Since today I can not open my email program. I have followed all security instructions. It must be a technical defect."
    }
    spamfilter = {
        "Norton overview": "Spam Report",
        "Number of mails in spam folder": 1,
        "Most recent spam mail": "<toni@lottototto.com> Earn Money @ Work",
        "Deleted": "Yes"
    }
    incidentreport = {
        "Security Incident Report": "#322",
        "Date": str(date.today().strftime("%b-%d-%Y")),
        "Reported by": "Mr. Hamann",
        "Organizational Unit": "Board of Directors",
        "Contact": "+345456444",
        "Location": "Mailing Address",
        "Incident Description": "This morning, an employee received a suspicious email and deleted it according to our security policy guidelines."
        
    }

    testsetlist = []
    testsetlist.append(userticket)
    testsetlist.append(spamfilter)
    testsetlist.append(incidentreport)

    return testsetlist


# Connection to Database
app = Flask("__name__")
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/incidentwebapp_DB")
db = mongodb_client.db



# Only For Testing

#print (get_testset_1()) 

