import re


def _line_of(text, needle):
    """1-based line number of the first line containing needle, or None."""
    for i, line in enumerate(text.splitlines(), start=1):
        if needle.lower() in line.lower():
            return i
    return None


def check_rule(rule, text):
    """Return (passed, detail). detail locates the evidence when relevant."""
    rtype = rule["type"]
    value = rule.get("value", "")

    if rtype == "required_phrase":
        line = _line_of(text, value)
        if line is not None:
            return True, f"found at line {line}"
        return False, "phrase not found"

    if rtype == "forbidden_phrase":
        line = _line_of(text, value)
        if line is None:
            return True, "not present"
        return False, f"found at line {line}"

    if rtype == "required_regex":
        match = re.search(value, text, re.IGNORECASE | re.MULTILINE)
        if match:
            line = text[: match.start()].count("\n") + 1
            return True, f"matched at line {line}"
        return False, "pattern not found"

    words = len(text.split())
    if rtype == "min_words":
        if words >= int(value):
            return True, f"{words} words"
        return False, f"{words} words (minimum {value})"

    if rtype == "max_words":
        if words <= int(value):
            return True, f"{words} words"
        return False, f"{words} words (maximum {value})"

    raise ValueError(f"unknown rule type: {rtype}")


def review(text, rules):
    """Run all rules over the text. Returns a report dict."""
    results = []
    for rule in rules:
        passed, detail = check_rule(rule, text)
        results.append(
            {
                "id": rule["id"],
                "description": rule["description"],
                "severity": rule["severity"],
                "passed": passed,
                "detail": detail,
            }
        )
    errors = sum(1 for r in results if not r["passed"] and r["severity"] == "error")
    warnings = sum(1 for r in results if not r["passed"] and r["severity"] == "warning")
    return {
        "passed": errors == 0,
        "total": len(results),
        "failed_errors": errors,
        "failed_warnings": warnings,
        "results": results,
    }
