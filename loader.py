import glob
import os
import logging
import threading

from forwarding_rules import ForwardingRule

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

RULES_DIR = os.environ.get('SMFP_RULES_DIR') or os.path.join(BASE_DIR, "rules")
RULES_FILE_EXTENSION = "*.json"

logger = logging.getLogger()


def load_all_rules(rules_dir: str = RULES_DIR) -> {ForwardingRule}:
    rules_files = os.path.join(rules_dir, RULES_FILE_EXTENSION)

    rules = {}

    files = glob.glob(rules_files)

    print(files)

    if files:
        for file in files:
            current_rule: ForwardingRule = ForwardingRule.from_json_file(file)
            rules[current_rule.name] = current_rule
    else:
        logger.warning("No rules found in: {dir}".format(dir=rules_dir))
    return rules
