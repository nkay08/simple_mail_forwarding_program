# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
import json

if __name__ == '__main__':
    # print_hi('PyCharm')
    import mail_forwarder
    import credentials
    import forwarding_rules

    creds = credentials.Credentials("linkrotator@yahoo.com", "fwtlhvjwcyrwayiu", "imap.mail.yahoo.com")
    rule = forwarding_rules.ForwardingRule(
        from_address="linkrotator@yahoo.com",
        to_address="n.klipp@nkay.info",
        credentials=creds
    )

    with open("rules/linkrotator.json") as file:
        rule = forwarding_rules.ForwardingRule.from_json(json.load(file))
        print(rule.__dict__)

    # mails = mail_forwarder.fetch_emails(rule)
    # mail_forwarder.forward_mails(mails, rule)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
