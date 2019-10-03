import logging
import socket


class AddHostName(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = self.hostname
        return True


class NotIncludeHealthcheck(logging.Filter):
    def filter(self, record):
        return '/healthcheck' not in record.getMessage()
