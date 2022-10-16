import smtplib
from email.mime.text import MIMEText
from src.config import MAIL, MAIL_PASSWORD


def send_email(title, content, adress):
    session = smtplib.SMTP(host='smtp.gmail.com', port=587)

    session.starttls()

    session.login(user=MAIL, password=MAIL_PASSWORD)

    mail = MIMEText(title)
    mail['Subject'] = content

    session.sendmail(from_addr=MAIL, to_addrs=adress, msg=mail.as_string())

    session.quit()