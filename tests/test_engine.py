import json
import subprocess
import sys
from pathlib import Path

import pytest

from checker.engine import check_rule, review
from checker.rules import load_rules

ROOT = Path(__file__).resolve().parent.parent


def test_required_phrase_found_and_missing():
    rule = {"id": "x", "type": "required_phrase", "value": "Assinatura", "description": "d", "severity": "error"}
    passed, detail = check_rule(rule, "linha um\nAssinatura do cliente\nlinha três")
    assert passed and "line 2" in detail
    passed, _ = check_rule(rule, "nada aqui")
    assert not passed


def test_forbidden_phrase():
    rule = {"id": "x", "type": "forbidden_phrase", "value": "[NOME]", "description": "d", "severity": "error"}
    passed, detail = check_rule(rule, "contrato de [NOME] empresa")
    assert not passed and "line 1" in detail
    passed, _ = check_rule(rule, "contrato de Fulano")
    assert passed


def test_required_regex():
    rule = {"id": "x", "type": "required_regex", "value": r"\b\d{2}/\d{2}/\d{4}\b", "description": "d", "severity": "error"}
    passed, _ = check_rule(rule, "São Paulo, 01/11/2026")
    assert passed
    passed, _ = check_rule(rule, "sem data nenhuma")
    assert not passed


def test_min_max_words():
    min_rule = {"id": "x", "type": "min_words", "value": "3", "description": "d", "severity": "warning"}
    max_rule = {"id": "y", "type": "max_words", "value": "5", "description": "d", "severity": "warning"}
    assert check_rule(min_rule, "uma duas três quatro")[0]
    assert not check_rule(min_rule, "uma duas")[0]
    assert check_rule(max_rule, "uma duas três")[0]
    assert not check_rule(max_rule, "uma duas três quatro cinco seis")[0]


def test_review_aggregates_errors_and_warnings():
    rules = [
        {"id": "e", "type": "required_phrase", "value": "ausente", "description": "d", "severity": "error"},
        {"id": "w", "type": "required_phrase", "value": "ausente", "description": "d", "severity": "warning"},
        {"id": "ok", "type": "required_phrase", "value": "presente", "description": "d", "severity": "error"},
    ]
    report = review("texto presente aqui", rules)
    assert report["passed"] is False
    assert report["total"] == 3
    assert report["failed_errors"] == 1
    assert report["failed_warnings"] == 1


def test_review_all_pass():
    rules = [{"id": "ok", "type": "required_phrase", "value": "presente", "description": "d", "severity": "error"}]
    report = review("texto presente", rules)
    assert report["passed"] is True


def test_load_rules_rejects_unknown_type(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps([{"id": "x", "type": "inventado", "value": "", "description": "d"}]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_rules(bad)


def test_cli_sample_document_is_rejected_with_placeholders():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), str(ROOT / "samples" / "contrato-exemplo.txt")],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1
    assert "REJECTED" in proc.stdout
    assert "sem_placeholder" in proc.stdout


def test_cli_clean_document_passes(tmp_path):
    doc = tmp_path / "ok.txt"
    doc.write_text(
        "Nome: Fulano de Tal\nContrato de serviços com várias palavras para passar "
        "no mínimo de trinta palavras exigido pelo checklist padrão do projeto de "
        "demonstração com mais e mais conteúdo suficiente aqui.\n"
        "São Paulo, 01/11/2026\nAssinatura do contratante\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), str(doc)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout
    assert "APPROVED" in proc.stdout
