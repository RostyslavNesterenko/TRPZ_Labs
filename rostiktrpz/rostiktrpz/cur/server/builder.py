from cur.server.emailclient import EmailClient
from cur.server.organizer import EmailOrganizer


class EmailClientBuilder:
    def __init__(self):
        self._provider = None
        self._user_email = None
        self._user_password = None

    def set_provider(self, provider):
        self._provider = provider
        return self

    def set_user_email(self, user_email):
        self._user_email = user_email
        return self

    def set_user_password(self, user_password):
        self._user_password = user_password
        return self

    def build(self):
        if not all([self._provider, self._user_email, self._user_password]):
            raise ValueError("Відсутні обов'язкові поля")
        return EmailClient(self._provider, self._user_email, self._user_password)

    def build_organizer(self):
        if not all([self._provider, self._user_email, self._user_password]):
            raise ValueError("Відсутні обов'язкові поля")
        return EmailOrganizer(self._provider, self._user_email, self._user_password)


class EmailInterpreter:
    def __init__(self, email_organizer):
        self.email_organizer = email_organizer

    def interpret(self, command):
        if "send email" in command:
            self.email_organizer.perform_email_operation()
        elif "classify emails" in command:
            self.email_organizer.classify_and_move_emails()
        elif "save draft" in command:
            self.email_organizer.save_draft("recipient@example.com", "Draft Subject", "Draft Body")
        elif "list folders" in command:
            print("Список папок...")
        elif "read emails" in command:
            self.email_organizer.read_emails()
        else:
            print("Недопустимая команда")
