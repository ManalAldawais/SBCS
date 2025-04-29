import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import os

sender_email = os.getenv('SENDER_EMAIL', "Mahaalosaimi2@gmail.com")
sender_password = os.getenv('SENDER_PASSWORD', "ijsj seex sxif mltw")

def send_email_alert(receiver_email, subject, message_body, image_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_body, 'plain'))

    if image_path:
        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={Path(image_path).name}",
            )
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📨 Email sent successfully!")
    except Exception as e:
        raise Exception(f"❌ Failed to send email: {e}")
