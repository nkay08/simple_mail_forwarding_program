import smtplib, imaplib, email
import logging

from enums import FetchProtocol, MailStatus
from forwarding_rules import ForwardingRule
from mail_message import Email
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
from periodic_job import schedule_function


logger = logging.getLogger()

# -----------------------------------



def save_mail_id_fetched(mail_id: str, rule: ForwardingRule):
    """
    This function shall save the ids of fetched emails in a local db.
    :param mail_id:
    :param rule:
    :return:
    """
    # TODO
    pass


def save_mail_id_forwarded(mail_id: str, rule: ForwardingRule):
    """
    This function shall save the ids of forwarded emails in a local db.
    :param mail_id:
    :param rule:
    :return:
    """
    # TODO
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
        # first_email_id = int(id_list[0])
        # latest_email_id = int(id_list[-1])


        for mail_id in id_list:
            typ, data = fetch_mail(mail_id, server_conn)
            current_mail: Email = Email.from_bytes(data[0][1], mail_id)

            if rule.save_ids:
                save_mail_id_fetched(str(mail_id), rule)

            fetched_mails.append(current_mail)
    else:
        logger.warning("No new messages")
    server_conn.close()
    return fetched_mails


def forward_mail(mail: Email, rule: ForwardingRule, server_conn: smtplib.SMTP, save_ids: bool = True):
    logger.info("Sending mail {mail}".format(mail=mail))

    part1 = MIMEText("")
    part2 = MIMEMessage(mail.email)

    new_email = MIMEMultipart()
    new_email['Subject'] = mail.subject
    new_email['From'] = rule.from_address
    new_email['To'] = rule.to_address
    if rule.set_reply_to:
        new_email['Reply-To'] = mail.from_address
    new_email.attach(part1)
    new_email.attach(part2)
    server_conn.send_message(new_email)
    logger.info("Successfully sent mail {mail}".format(mail=mail))


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
        logger.info("Done RESET mail status for rule {rule} and mails: [{mails}]".format(rule=rule.name, mails=mails))


def mark_seen(mail: Email, server_conn: imaplib.IMAP4):
    server_conn.store(mail.id, '+FLAGS', '\Seen')


def mark_unseen(mail: Email, server_conn: imaplib.IMAP4):
    server_conn.store(mail.id, '-FLAGS', '\Seen')
