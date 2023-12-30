class EmailProvider:
    _instances = {}

    def __new__(cls, smtp_server, smtp_port, imap_server, pop3_server):
        key = (smtp_server, smtp_port, imap_server, pop3_server)
        if key not in cls._instances:
            instance = super(EmailProvider, cls).__new__(cls)
            cls._instances[key] = instance
            return instance
        return cls._instances[key]

    def __init__(self, smtp_server, smtp_port, imap_server, pop3_server):
        if not hasattr(self, '_initialized'):
            self.smtp_server = smtp_server
            self.smtp_port = smtp_port
            self.imap_server = imap_server
            self.pop3_server = pop3_server
            self._initialized = True