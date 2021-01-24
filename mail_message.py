from email.message import EmailMessage, Message
from email import message_from_string, message_from_bytes
from email.policy import default as email_default_policy # use this policy to get EmailMessage instead of Message object
import logging

from utils import soup_insert_in_html_body, soup_insert_link_in_html_body


ORIGINAL_FROM = "ORIGINAL FROM: "

logger = logging.getLogger()

# -----------------------------------


class Email:

    _email: EmailMessage = None

    def __init__(self, mail: EmailMessage, uid):
        self._email: EmailMessage = mail
        self._id = uid

    def __str__(self):
        return self._id

    def __repr__(self):
        return self.__class__.__name__ + "::" + self._id

    @staticmethod
    def from_bytes(email_bytes, uid) -> 'Email':
        return Email(message_from_bytes(email_bytes, policy=email_default_policy), uid)

    @staticmethod
    def from_string(email_string, uid) -> 'Email':
        return Email(message_from_string(email_string, policy=email_default_policy), uid)

    @property
    def subject(self) -> str:
        return self._email['subject']

    @property
    def body(self) -> Message:
        return self._email.get_body()

    @property
    def body_html(self) -> Message:
        return self._email.get_body(('html', ))

    @property
    def body_text(self) -> Message:
        return self._email.get_body(('plain', ))

    def body_add_line(self, line: str):
        self.body_add_line_text(line)
        self.body_add_line_html(line)

    def body_add_line_text(self, line: str):
        text = self.body_text
        if text:
            new_line = "* " + str(line)
            split = text.as_string().split("\n")[3:]
            split.insert(0, new_line)
            new_text = "\n".join(split)
            text.set_payload(new_text)

    def body_add_line_html(self, line: str):
        html = self.body_html
        if html:
            html.set_payload(soup_insert_link_in_html_body(html, line))

    def add_original_sender(self):
        self.add_original_sender_to_text()
        self.add_original_sender_to_html()

    def add_original_sender_to_text(self):
        self.body_add_line_text(ORIGINAL_FROM + self.from_address)

    def add_original_sender_to_html(self):
        html = self.body_html
        if html:
            html.set_payload(soup_insert_link_in_html_body(str(html), "mailto:" + str(self.from_address), ORIGINAL_FROM + str(self.from_address)))

    @property
    def date(self):
        return self._email['date']

    @property
    def from_address(self) -> str:
        return self._email['from']

    @from_address.setter
    def from_address(self, address: str):
        self._email.replace_header('from', address)
        # self._email['from'] = address

    @property
    def to_address(self) -> str:
        return self._email['to']

    @to_address.setter
    def to_address(self, address: str):
        self._email.replace_header('to', address)
        # self._email['to'] = address

    @property
    def email(self) -> EmailMessage:
        return self._email

    def set_header(self, header: str, value: str):
        try:
            self._email.replace_header(header, value)
        except KeyError as e:
            self._email.add_header(header, value)

    def set_reply_to(self, value: str):
        self.set_header('reply-to', value)

    @property
    def id(self):
        return self._id
