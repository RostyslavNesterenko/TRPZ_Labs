from abc import ABC, abstractmethod


class EmailTemplate(ABC):
    def __init__(self, provider, user_email, user_password):
        self.provider = provider
        self.user_email = user_email
        self.user_password = user_password

    def perform_email_operation(self):
        self.connect_to_server()
        self.prepare_message()
        self.send_message()
        self.disconnect_from_server()

    @abstractmethod
    def connect_to_server(self):
        pass

    @abstractmethod
    def prepare_message(self):
        pass

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def disconnect_from_server(self):
        pass