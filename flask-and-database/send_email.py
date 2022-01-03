import email
import smtplib


def send_email(email, height, average_height, counts):
    from_email = "ENTER YOUR EMAIL HERE"
    from_password = "ENTER THE EMAIL'S PASSWORD"
    to_email = email

    subject = "Height data"
    message = f"Hello there, your height is <strong>{height}</strong>. The average height is <strong>{average_height}</strong> with total samples of <strong>{counts}</strong>"
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
