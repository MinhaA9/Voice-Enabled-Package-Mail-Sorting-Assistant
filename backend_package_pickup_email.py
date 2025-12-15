import threading
import smtplib
from email.message import EmailMessage

def send_email(sender, password, recipient, subject, body):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

def send_email_thread(recipient, subject,body):
    try:
        send_email(
            sender="first.last@company.com",
            password="app password",
            recipient=recipient,
            subject=subject,
            body=body
        )
        print("Email has been sent")
        successfull = True

    except Exception as e:
        print("Email not send")
        successfull = False
    return successfull
def on_send_click():
    threading.Thread(target=send_email_thread, daemon=True).start()
