import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def send_email_alert(receiver_email, subject, message_body, image_path=None):
    sender_email = "Mahaalosaimi2@gmail.com"  # ✏️ إيميلك
    sender_password = "ijsj seex sxif mltw"




  # ✏️ كلمة مرور التطبيق (مو العادي)

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
        print(f"❌ Failed to send email: {e}")
