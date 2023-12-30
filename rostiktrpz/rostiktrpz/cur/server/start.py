import socket
import threading

from cur.server.builder import EmailClientBuilder, EmailInterpreter
from cur.server.provider import EmailProvider


class EmailServer:
    def __init__(self, host, port, provider_name, user_email, user_password):
        self.host = host
        self.port = port
        self.provider_name = provider_name
        self.user_email = user_email
        self.user_password = user_password
        self.email_interpreter = self._create_email_interpreter()

    def _create_email_interpreter(self):
        config = self.get_provider_config(self.provider_name)
        if config:
            client_builder = EmailClientBuilder()
            organizer = (client_builder.set_provider(config)
                                       .set_user_email(self.user_email)
                                       .set_user_password(self.user_password))
            return EmailInterpreter(organizer.build_organizer())
        else:
            raise ValueError(f"Провайдер '{self.provider_name}' не найден.")

    @staticmethod
    def get_provider_config(provider_name):
        providers = {
            'gmail': EmailProvider('smtp.gmail.com', 587, 'imap.gmail.com', 'pop.gmail.com'),
            'ukr.net': EmailProvider('smtp.ukr.net', 465, 'imap.ukr.net', 'pop3.ukr.net'),
            'i.ua': EmailProvider('smtp.i.ua', 465, 'imap.i.ua', 'pop3.i.ua')
        }
        return providers.get(provider_name.lower())

    def process_command(self, command):
        if command.startswith("CONFIG"):
            try:
                _, provider_name, user_email, user_password = command.split(" ", 3)
                config = self.get_provider_config(provider_name)
                if config:
                    client_builder = EmailClientBuilder()
                    organizer = (client_builder.set_provider(config)
                                           .set_user_email(user_email)
                                           .set_user_password(user_password))
                    self.email_interpreter = EmailInterpreter(organizer.build_organizer())
                    return "Configuration successful."
                else:
                    return f"Provider '{provider_name}' not found."
            except Exception as e:
                return f"Error in configuration: {e}"

        elif command.startswith("send email"):
            _, recipient, subject, body = command.split(" ", 3)
            self.email_interpreter.email_organizer.prepare_and_send_message(recipient, subject, body)
            return "Email sent successfully."

        elif command.startswith("classify emails"):
            self.email_interpreter.email_organizer.classify_and_move_emails()
            return "Emails classified."

        elif command.startswith("read emails"):
            self.email_interpreter.email_organizer.read_emails()
            return "Emails read."

        elif command.startswith("save draft"):
            params = command.split(" ", 3)[1:]
            if len(params) >= 3:
                recipient, subject, body = params
                self.email_interpreter.email_organizer.save_draft(recipient, subject, body)
                return "Draft saved."
            else:
                return "Insufficient parameters for 'save draft'."

        else:
            return "Invalid command."

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024)
            if not request:
                break
            response = self.process_command(request.decode('utf-8'))
            client_socket.send(response.encode('utf-8'))
        client_socket.close()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client, address = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12347
    PROVIDER_NAME = 'gmail'
    USER_EMAIL = 'your-email@example.com'
    USER_PASSWORD = 'your_password'

    email_server = EmailServer(HOST, PORT, PROVIDER_NAME, USER_EMAIL, USER_PASSWORD)
    email_server.start_server()