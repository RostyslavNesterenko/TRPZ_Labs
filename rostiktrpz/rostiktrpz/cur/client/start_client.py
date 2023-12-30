import socket

class EmailClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def send_command(self, command):
        self.client.send(command.encode('utf-8'))
        response = self.client.recv(4096).decode('utf-8')
        return response

    def configure(self):
        provider_name = input("Enter your email provider (e.g., 'gmail'): ")
        user_email = input("Enter your email address: ")
        user_password = input("Enter your password: ")
        response = self.send_command(f"CONFIG {provider_name} {user_email} {user_password}")
        print(response)

    def run(self):
        self.connect()
        self.configure()

        while True:
            command = input("Enter command (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break
            elif command.lower() == 'help':
                self.print_help()
                continue
            response = self.send_command(command)
            print(f"Response: {response}")

        self.client.close()

    @staticmethod
    def print_help():
        print("Available commands:")
        print("CONFIG <provider> <email> <password> - Configure email client.")
        print("send email <recipient> <subject> <body> - Send an email.")
        print("classify emails - Classify and move emails.")
        print("save draft <recipient> <subject> <body> - Save a draft email.")
        print("read emails - Read emails from inbox.")


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12347
    email_client = EmailClient(HOST, PORT)
    email_client.run()
