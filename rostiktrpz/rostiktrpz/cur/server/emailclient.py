import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from cur.server.decorator import measure_execution_time
from cur.server.template import EmailTemplate


class EmailClient(EmailTemplate):
    @measure_execution_time
    def connect_to_server(self):
        try:
            print("Підключення до SMTP серверу...")

            with smtplib.SMTP(self.provider.smtp_server, self.provider.smtp_port) as server:
                server.starttls()
                server.login(self.user_email, self.user_password)

        except Exception as e:
            print(f"Помилка підключення до SMTP серверу: {e}")



    def prepare_and_send_message(self, recipient, subject, body, attachments=None):
        print("Підготовка та відправка повідомлення...")

        self.prepare_message(recipient, subject, body, attachments)
        self.send_message()

    def prepare_message(self, recipient, subject, body, attachments=None):
        print("Підготовка повідомлення...")

        self.message = MIMEMultipart()
        self.message['From'] = self.user_email
        self.message['To'] = recipient
        self.message['Subject'] = subject
        self.message.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                self.message.attach(part)

    def send_message(self):
        print("Відправлення повідомлення...")

        try:
            with smtplib.SMTP(self.provider.smtp_server, self.provider.smtp_port) as server:
                server.starttls()
                server.login(self.user_email, self.user_password)
                server.sendmail(self.user_email, [self.message['To']], self.message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")


    def disconnect_from_server(self):
        print("Відключення від SMTP сервера...")

    def save_draft(self, recipient, subject, body, attachments=None):
        print("Збереження чернетки...")

        msg = MIMEMultipart()
        msg['From'] = self.user_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)

        with open(f"{subject}_draft.eml", "w") as draft_file:
            draft_file.write(msg.as_string())
        print("Draft saved successfully.")


    def send_email_with_attachments(self, recipient, subject, body, attachments=None):
        print("Відправлення листа з додатками...")

        msg = MIMEMultipart()
        msg['From'] = self.user_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for file_path in attachments:
                part = MIMEBase('application', "octet-stream")
                with open(file_path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)

        try:
            with smtplib.SMTP(self.provider.smtp_server, self.provider.smtp_port) as server:
                server.starttls()
                server.login(self.user_email, self.user_password)
                server.sendmail(self.user_email, [recipient], msg.as_string())
            print("Email with attachments sent successfully!")
        except Exception as e:
            print(f"Error sending email with attachments: {e}")