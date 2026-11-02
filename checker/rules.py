import json
import re
from pathlib import Path


def load_rules(path):
    with open(path or Path(__file__).resolve().parent.parent / "rules" / "default.json",
              encoding="utf-8") as f:
        rules = json.load(f)
    valid_types = {
        "required_phrase", "forbidden_phrase", "required_regex",
        "min_words", "max_words",
    }
    for rule in rules:
        if rule.get("type") not in valid_types:
            raise ValueError(f"unknown rule type: {rule.get('type')}")
        rule.setdefault("severity", "error")
    return rules
