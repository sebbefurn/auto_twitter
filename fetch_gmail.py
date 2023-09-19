import imaplib
import credentials
import email

imap_url = 'imap.gmail.com'
 
# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
 
# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    data = data[0].split()
    data = data[-10:]
    print(data)
    return data
 
# Function to get the list of emails under this label
def get_emails(result_bytes, con):
    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes:
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
 
    return msgs
 
def extract_subject_from_email(raw_email):
    email_message = email.message_from_bytes(raw_email)
    return email_message["Subject"]

def get_codes(user, password):
    # this is done to make SSL connection with GMAIL
    con = imaplib.IMAP4_SSL(imap_url)
    
    # logging the user in
    con.login(user, password)
    
    # calling function to check for email under this label
    con.select('Inbox')
    
    # fetching emails from this user "tu**h*****1@gmail.com"
    #msgs = get_emails(search('FROM', 'info@x.com', con))
    msgs = get_emails(search('FROM', 'info@x.com', con), con)
    codes = []
    
    for email_data in reversed(msgs):
        raw_email = email_data[0][1]
        subject = extract_subject_from_email(raw_email)
        codes.append(subject[:6].strip())

    return codes
