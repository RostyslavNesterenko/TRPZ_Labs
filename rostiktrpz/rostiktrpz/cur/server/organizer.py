import email
import imaplib

from cur.server.decorator import measure_execution_time
from cur.server.emailclient import EmailClient


class EmailOrganizer(EmailClient):
    @measure_execution_time
    def connect_to_server(self):
        try:
            print("Підключення до IMAP серверу...")

            with imaplib.IMAP4_SSL(self.provider.imap_server) as server:
                server.login(self.user_email, self.user_password)
                server.select('inbox')
        except Exception as e:
            print(f"Помилка підключення до IMAP серверу: {e}")

    def read_emails(self):
        print("Підключення до IMAP серверу...")

        try:

            with imaplib.IMAP4_SSL(self.provider.imap_server) as server:
                server.login(self.user_email, self.user_password)
                server.select('inbox')

                typ, messages = server.search(None, 'ALL')
                if typ != 'OK':
                    print("Не удалось найти сообщения.")
                    return

                for num in messages[0].split()[:5]:  # Пример чтения последних 5 сообщений
                    typ, data = server.fetch(num, '(RFC822)')
                    if typ != 'OK':
                        continue

                    msg = email.message_from_bytes(data[0][1])
                    print(f"Письмо от: {msg['from']}")
                    print(f"Тема: {msg['subject']}")
                    print("Содержание:")
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                print(part.get_payload(decode=True).decode())
                    else:
                        print(msg.get_payload(decode=True).decode())

        except Exception as e:
            print(f"Ошибка при чтении писем: {e}")


    def classify_and_move_emails(self):
        print("Класифікація та переміщення листів...")
        try:
            with imaplib.IMAP4_SSL(self.provider.imap_server) as server:
                server.login(self.user_email, self.user_password)
                server.select('inbox')
                typ, messages = server.search(None, 'ALL')

                if typ != 'OK':
                    print("No messages to classify.")
                    return

                for num in messages[0].split():
                    typ, data = server.fetch(num, '(RFC822)')
                    if typ != 'OK':
                        continue

                    msg = email.message_from_bytes(data[0][1])
                    subject = msg['subject'].lower()

                    # Logic for email classification
                    if 'important' in subject:
                        self.create_folder_if_not_exists(server, 'Important')
                        server.copy(num.decode('utf-8'), 'Important')
                        server.store(num, '+FLAGS', '\\Deleted')
                    elif 'work' in subject:
                        self.create_folder_if_not_exists(server, 'Work')
                        server.copy(num.decode('utf-8'), 'Work')
                        server.store(num, '+FLAGS', '\\Deleted')

                server.expunge()
        except Exception as e:
            print(f"Ошибка при классификации и перемещении писем: {e}")

    def create_folder_if_not_exists(self, server, folder_name):
        print(f"Створення папки '{folder_name}', якщо вона не існує...")