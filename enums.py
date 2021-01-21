from enum import Enum


class FetchProtocol(Enum):
    IMAP = 1
    POP3 = 2


class MailStatus(Enum):
    ALL = 1
    UNREAD = 2
    READ = 3