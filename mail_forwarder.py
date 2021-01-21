import smtplib, imaplib, email
import logging

from enums import FetchProtocol, MailStatus
from forwarding_rules import ForwardingRule
from mail_message import Email


logger = logging.getLogger()

# -----------------------------------


def save_mail_id_fetched(mail_id: str, rule: ForwardingRule):
    pass


def save_mail_id_forwarded(mail_id: str, rule: ForwardingRule):
    pass


def fetch_emails(rule: ForwardingRule, save_ids: bool = True) -> [Email]:
    # raise NotImplementedError

    if rule.protocol == FetchProtocol.IMAP:
        client = imaplib.IMAP4_SSL(rule.credentials.host)
    elif rule.protocol == FetchProtocol.POP3:
        raise NotImplementedError
    else:
        client: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(rule.credentials.host)

    client.login(rule.credentials.username, rule.credentials.password)
    client.select()
    # By default inbox
    # client.select(rule.folder)

    # can also be ALL
    return_code, data = client.search(None, 'UnSeen')

    mail_ids: str = data[0].decode()
    id_list: [str] = mail_ids.split()

    fetched_mails: [Email] = []

    if len(id_list) > 0:
        logger.info("List of new mail ids: {ids}".format(ids=id_list))
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        emails = []

        for mail_id in id_list:
            typ, data = client.fetch(str(mail_id), '(RFC822)')
            current_mail: Email = Email.from_bytes(data[0][1])

            # print(current_mail.subject, current_mail.from_address, current_mail.to_address)
            # print(current_mail.body)
            # current_mail.body_add_line_text("ORIGINAL_FROM: " + current_mail.from_address)
            #
            # print(current_mail.body_text)
            current_mail.add_original_sender()
            # print(current_mail.body_text)

            current_mail.set_reply_to(current_mail.from_address)
            current_mail.from_address = rule.from_address
            current_mail.to_address = rule.to_address

            if rule.save_ids:
                save_mail_id_fetched(str(mail_id), rule)

    else:
        logger.warning("No new messages")

    return fetched_mails


def forward_mail(mail: Email, rule: ForwardingRule, save_ids: bool = True):
    mail.add_original_sender()
    # print(current_mail.body_text)

    mail.set_reply_to(mail.from_address)
    mail.from_address = rule.from_address
    mail.to_address = rule.to_address

    if save_ids and rule.save_ids:
        # save_mail_id_forwarded(mail._)
        pass
    raise NotImplementedError


def forward_mails(mails: [Email], rule: ForwardingRule, save_ids: bool = True):
    for mail in mails:
        forward_mail(mail, rule, save_ids)
