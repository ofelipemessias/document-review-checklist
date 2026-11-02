from docx import Document

from checker.document import load_text


def test_load_txt(tmp_path):
    f = tmp_path / "doc.txt"
    f.write_text("linha 1\nlinha 2", encoding="utf-8")
    assert load_text(f) == "linha 1\nlinha 2"


def test_load_docx(tmp_path):
    doc = Document()
    doc.add_paragraph("Primeiro parágrafo")
    doc.add_paragraph("Segundo parágrafo")
    f = tmp_path / "doc.docx"
    doc.save(f)
    text = load_text(f)
    assert "Primeiro parágrafo" in text
    assert "Segundo parágrafo" in text


def test_load_unsupported_format(tmp_path):
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF fake")
    try:
        load_text(f)
        assert False, "should have raised"
    except ValueError as e:
        assert "unsupported format" in str(e)
