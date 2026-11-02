from pathlib import Path


def load_text(path):
    """Load a document as plain text. Supports .txt/.md and .docx."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8")
    if suffix == ".docx":
        from docx import Document

        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"unsupported format: {suffix} (use .txt, .md or .docx)")
