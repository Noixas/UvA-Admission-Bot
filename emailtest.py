import smtplib,ssl
import json

def send_email(subject, body, file_emails='email.json'):
    with open(file_emails, 'r') as fp:
        email_data = json.load(fp)
        
    receiver = email_data['receiver']
    sender= email_data['sender']
    smtp_server = email_data['smtp_server']

    file5 = open('Credentials', 'r') #read passwords
    Lines = file5.readlines() 
    gmail_password = Lines[2]
   
    message = "Subject: "+subject+'\n \n'+body

    port = 587
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            
            print (sender,'- Login step next!')
            server.login(sender, gmail_password)
            
            print (sender,'- Login Succesful!')
            server.sendmail(sender, receiver, message)
        print ('Email sent!')
        print('Message:',message)
    except:
        print ('Something went wrong...')

subject = 'Function message'
body = 'Python. 3'
send_email(subject,body)