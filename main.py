# !/bin/python3

import json
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    import forwarding_rules
    import loader
    import periodic_job
    import mail_forwarder

    rules = loader.load_all_rules()

    # for rulename, rule in rules.items():
    #     print("Executing rule ", rulename)
    #     mails = mail_forwarder.fetch_emails(rule)
    #     mail_forwarder.forward_mails(mails, rule)

    mail_forwarder.schedule_rules(rules)


