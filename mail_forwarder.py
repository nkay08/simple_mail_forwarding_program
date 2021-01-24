import smtplib, imaplib, email
import logging

from enums import FetchProtocol, MailStatus
from forwarding_rules import ForwardingRule
from mail_message import Email
from periodic_job import schedule_function


logger = logging.getLogger()

# -----------------------------------


def save_mail_id_fetched(mail_id: str, rule: ForwardingRule):
    pass


def save_mail_id_forwarded(mail_id: str, rule: ForwardingRule):
    pass


def schedule_rules(rules: {ForwardingRule}):
    for name, rule in rules.items():
        schedule_function(rule.schedule, fetch_and_forward, [rule])


def fetch_mail(mail_id, server_conn: imaplib.IMAP4):
    if type(mail_id) == str or type(mail_id) == str:
        return server_conn.fetch(str(mail_id), '(RFC822)')
    elif type(mail_id) == Email:
        return server_conn.fetch(mail_id.id, '(RFC822)')


def fetch_emails(rule: ForwardingRule, save_ids: bool = True) -> [Email]:
    # raise NotImplementedError

    if rule.protocol == FetchProtocol.IMAP:
        server_conn = imaplib.IMAP4_SSL(rule.credentials.host)
    elif rule.protocol == FetchProtocol.POP3:
        raise NotImplementedError
    else:
        server_conn: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(rule.credentials.host)

    server_conn.login(rule.credentials.username, rule.credentials.password)
    server_conn.select()
    # By default inbox
    # server_conn.select(rule.folder)

    # can also be ALL
    return_code, data = server_conn.search(None, 'UnSeen')

    mail_ids: str = data[0].decode()
    id_list: [str] = mail_ids.split()

    fetched_mails: [Email] = []

    if len(id_list) > 0:
        logger.info("List of new mail ids: {ids}".format(ids=id_list))
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        emails = []

        for mail_id in id_list:
            typ, data = fetch_mail(mail_id, server_conn)
            current_mail: Email = Email.from_bytes(data[0][1], mail_id)

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

            # TODO remove line
            # mark_unseen(current_mail, server_conn)

            fetched_mails.append(current_mail)
    else:
        logger.warning("No new messages")
    server_conn.close()
    return fetched_mails


def forward_mail(mail: Email, rule: ForwardingRule, server_conn: smtplib.SMTP, save_ids: bool = True):
    mail.add_original_sender()
    # print(current_mail.body_text)

    mail.set_reply_to(mail.from_address)
    mail.from_address = rule.from_address
    mail.to_address = rule.to_address

    if save_ids and rule.save_ids:
        # save_mail_id_forwarded(mail._)
        pass

    raise NotImplementedError

    server_conn.send_message(mail.email)


def forward_mails(mails: [Email], rule: ForwardingRule, save_ids: bool = True):
    error_mails = []
    if len(mails) > 0:
        logger.info("Try forwarding mails for rule: {rule}".format(rule=rule.name))
        with smtplib.SMTP_SSL(rule.credentials_outgoing.host) as server:
            server.login(rule.credentials_outgoing.username, rule.credentials_outgoing.password)
            for mail in mails:
                logger.info("Forwarding mail with uid: {uid}".format(uid=mail.id))
                try:
                    forward_mail(mail, rule, server, save_ids)
                except Exception as e:
                    logger.error(e)
                    error_mails.append(mail)
    else:
        logger.info("No mails to forward for rule: {rule}".format(rule=rule.name))
    reset_mail_status(error_mails, rule)


def fetch_and_forward(rule: ForwardingRule, save_ids: bool = True):
    mails: [Email] = fetch_emails(rule, save_ids)
    forward_mails(mails, rule, save_ids)


def reset_mail_status(mails: [Email], rule: ForwardingRule):
    if len(mails) > 0:
        logger.info("Resetting mail status for rule {rule} and mails: [{mails}]".format(rule=rule.name, mails=mails))
        with imaplib.IMAP4_SSL(rule.credentials.host) as server_conn:
            server_conn.login(rule.credentials.username, rule.credentials.password)
            server_conn.select()
            for mail in mails:
                mark_unseen(mail, server_conn)


def mark_seen(mail: Email, server_conn: imaplib.IMAP4):
    server_conn.store(mail.id, '-FLAGS', '\Seen')


def mark_unseen(mail: Email, server_conn: imaplib.IMAP4):
    server_conn.store(mail.id, '-FLAGS', '\Seen')
