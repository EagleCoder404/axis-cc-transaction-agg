import email
import re
import os
from imapclient import IMAPClient
from models import Transaction

def get_axis_transactions(from_date:str="2025/08/15", to_date:str="2025/09/15"):
    gmail_passcode = os.environ.get("DEV_GMAIL_PASSCODE")
    print(gmail_passcode)
    server = IMAPClient('imap.gmail.com', use_uid=True)
    server.login('harsha.jediknight@gmail.com', gmail_passcode)
    server.select_folder('INBOX')
    messages = server.gmail_search(f"from:alerts@axisbank.com and subject:\"transaction alert\" and after:{from_date} and before:{to_date}")

    transactions: list[Transaction] = []

    for uid, message_data in server.fetch(messages, "RFC822").items():      
        email_message = email.message_from_bytes(message_data[b"RFC822"])
        email_body = email_message.as_string()
        matches = re.findall(r"INR ([\d.]+) at (.*) on (\d{2}-\d{2}-\d{4})", email_body)
        keywords = []

        if re.search("decline", email_body, re.IGNORECASE):
            keywords.append("decline")
        if re.search("reverse", email_body, re.IGNORECASE):
            keywords.append("reverse")

        if(len(matches) > 0):
            pmatch = matches[0]
            transactions.append(Transaction(pmatch[0], pmatch[1], pmatch[2], keywords))

    return transactions

