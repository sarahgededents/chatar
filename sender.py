from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
import prono
import smtplib

######create your id.txt file with email, password and name in it separated by comma#######

with open('id.txt', 'r', encoding='utf-8') as ids:
    idt = ids.read()
    MY_ADDRESS = idt.split(',')[0]
    PASSWORD = idt.split(',')[1]
    NAME = idt.split(',')[2]

######create your emails.txt file with emails separated by comma#######
emails = []
with open('emails.txt', 'r', encoding='utf-8') as ema:
    em = ema.read()
    for email in em.split(','):
        emails.append(email)

def main():
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)  # Change with your host
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    for email in emails:
        msg = MIMEMultipart()
        msg['From'] = NAME
        msg['To'] = email
        msg['Subject'] = f'Pronostic quinté du {str(datetime.datetime.today().date())}'

        msg.attach(MIMEText(f"Bonjour,\n\nVoici le pronostic du jour: {str(prono.prono).strip('[]')}.\n\nBonne journée,\n{NAME}", 'plain'))
        s.send_message(msg)
        del msg
    s.quit()


if __name__ == '__main__':
    main()
