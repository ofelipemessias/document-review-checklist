import argparse
import sys

from checker.document import load_text
from checker.engine import review
from checker.report import render_json, render_text
from checker.rules import load_rules


def main():
    parser = argparse.ArgumentParser(
        description="Revisa um documento contra um checklist de regras configurável."
    )
    parser.add_argument("document", help="Caminho do documento (.txt, .md ou .docx)")
    parser.add_argument("--rules", default=None, help="Caminho do JSON de regras (padrão: rules/default.json)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    text = load_text(args.document)
    rules = load_rules(args.rules)
    report = review(text, rules)
    print(render_json(report) if args.format == "json" else render_text(report))
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
