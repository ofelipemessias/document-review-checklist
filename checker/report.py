import json


def render_text(report):
    icon = {True: "PASS", False: "FAIL"}
    lines = []
    for r in report["results"]:
        lines.append(
            f"[{icon[r['passed']]}] ({r['severity']}) {r['id']}: "
            f"{r['description']} - {r['detail']}"
        )
    lines.append("")
    lines.append(
        f"{report['total'] - report['failed_errors'] - report['failed_warnings']}"
        f"/{report['total']} passed, "
        f"{report['failed_errors']} error(s), {report['failed_warnings']} warning(s)"
    )
    lines.append("RESULT: " + ("APPROVED" if report["passed"] else "REJECTED"))
    return "\n".join(lines)


def render_json(report):
    return json.dumps(report, indent=2, ensure_ascii=False)
