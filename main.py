# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def test(rule: object):
    print(rule.__dict__)

# Press the green button in the gutter to run the script.
import json

if __name__ == '__main__':
    import forwarding_rules
    import loader
    import periodic_job
    import mail_forwarder

    rules = loader.load_all_rules()

    for k, v in rules.items():
        print(v.__dict__)
        print(v.credentials.__dict__)
        print(v.credentials_outgoing.__dict__)

    # for k, v in rules.items():
    #     periodic_job.schedule_function(v.schedule, test, [v])

    # mail_forwarder.schedule_rules(rules)

    # rule = forwarding_rules.ForwardingRule.from_json_file("rules/linkrotator.json")
    # print(rule.__dict__)

    # mails = mail_forwarder.fetch_emails(rule)
    # mail_forwarder.forward_mails(mails, rule)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
