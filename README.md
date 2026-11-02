# ✅ Document Review Checklist

🌐 [Español](#español) | [English](#english) | [Português](#português)

---

## 🇪🇸 Español

Motor de reglas en **Python** que revisa un documento contra un checklist configurable y devuelve un informe **pass/fail por regla, con la línea exacta del problema**. Ideal como puerta de calidad: el proceso termina con código de salida 1 si alguna regla de severidad `error` falla, listo para integrar en CI.

Proyecto de demostración basado en un revisor de documentos real que desarrollé para un despacho jurídico (que validaba cada pieza contra un checklist obligatorio), reconstruido de forma genérica: **sin datos personales reales, sin claves y sin información del despacho**.

### Tipos de regla

| Tipo | Qué verifica |
|------|--------------|
| `required_phrase` | Frase obligatoria presente |
| `forbidden_phrase` | Frase prohibida ausente (ej.: placeholders sin rellenar) |
| `required_regex` | Patrón obligatorio (ej.: fecha en `dd/mm/aaaa`) |
| `min_words` / `max_words` | Límites de tamaño |

Cada regla tiene severidad `error` (bloquea) o `warning` (solo informa). Las reglas se definen en un JSON propio o en el `rules/default.json` incluido.

### Ejecutar

```bash
pip install -r requirements.txt

# demo: documento de ejemplo con errores sembrados a propósito
python main.py samples/contrato-exemplo.txt
```

Salida (fragmento):

```
[PASS] (error) identificacao: Documento deve ter seção de identificação - matched at line 3
[FAIL] (error) sem_placeholder: Documento não pode conter placeholders - found at line 7
RESULT: REJECTED   (exit code 1)
```

Con Docker:

```bash
docker build -t document-review-checklist .
docker run --rm -v "$PWD:/data" document-review-checklist /data/mi-documento.txt
```

### Pruebas

```bash
pip install -r requirements-dev.txt
pytest -v
```

Resultado: **12 pruebas, todas en verde** ✅ (CI con GitHub Actions en cada push/PR)

### Estructura

```
├── checker/
│   ├── document.py    # Lectura de .txt/.md/.docx
│   ├── rules.py       # Carga y validación del checklist (JSON)
│   ├── engine.py      # Motor: aplica reglas, localiza evidencias
│   └── report.py      # Informe en texto o JSON
├── rules/default.json # Checklist de ejemplo (7 reglas)
├── samples/           # Documento ficticio con errores sembrados
└── tests/             # 12 pruebas
```

---

## 🇬🇧 English

**Python** rule engine that reviews a document against a configurable checklist and returns a **per-rule pass/fail report with the exact line of each problem**. Built as a quality gate: the process exits with code 1 when any `error`-severity rule fails, ready to plug into CI.

Demo project based on a real document reviewer I built for a law office (which validated every filing against a mandatory checklist), rebuilt as a generic version: **no real personal data, no keys, no office information**.

### Rule types

| Type | What it checks |
|------|----------------|
| `required_phrase` | Mandatory phrase is present |
| `forbidden_phrase` | Forbidden phrase is absent (e.g.: unfilled placeholders) |
| `required_regex` | Mandatory pattern (e.g.: date as `dd/mm/yyyy`) |
| `min_words` / `max_words` | Length limits |

Each rule has severity `error` (blocking) or `warning` (informational). Rules live in your own JSON or the bundled `rules/default.json`.

### Run

```bash
pip install -r requirements.txt

# demo: sample document with deliberately planted errors
python main.py samples/contrato-exemplo.txt
```

Output (excerpt):

```
[PASS] (error) identificacao: Documento deve ter seção de identificação - matched at line 3
[FAIL] (error) sem_placeholder: Documento não pode conter placeholders - found at line 7
RESULT: REJECTED   (exit code 1)
```

With Docker:

```bash
docker build -t document-review-checklist .
docker run --rm -v "$PWD:/data" document-review-checklist /data/my-document.txt
```

### Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

Result: **12 tests, all passing** ✅ (CI with GitHub Actions on every push/PR)

### Project layout

```
├── checker/
│   ├── document.py    # .txt/.md/.docx loading
│   ├── rules.py       # Checklist loading and validation (JSON)
│   ├── engine.py      # Engine: applies rules, locates evidence
│   └── report.py      # Text or JSON report
├── rules/default.json # Sample checklist (7 rules)
├── samples/           # Fictional document with planted errors
└── tests/             # 12 tests
```

---

## 🇧🇷 Português

Motor de regras em **Python** que revisa um documento contra um checklist configurável e devolve um relatório **pass/fail por regra, com a linha exata do problema**. Feito como portão de qualidade: o processo sai com código 1 quando alguma regra de severidade `error` falha, pronto pra plugar em CI.

Projeto de demonstração baseado em um revisor de documentos real que desenvolvi para um escritório de advocacia (que validava cada peça contra um checklist obrigatório), reconstruído de forma genérica: **sem dados pessoais reais, sem chaves e sem informações do escritório**.

### Tipos de regra

| Tipo | O que verifica |
|------|----------------|
| `required_phrase` | Frase obrigatória presente |
| `forbidden_phrase` | Frase proibida ausente (ex.: placeholders não preenchidos) |
| `required_regex` | Padrão obrigatório (ex.: data em `dd/mm/aaaa`) |
| `min_words` / `max_words` | Limites de tamanho |

Cada regra tem severidade `error` (bloqueia) ou `warning` (só informa). As regras ficam num JSON próprio ou no `rules/default.json` incluído.

### Rodar

```bash
pip install -r requirements.txt

# demo: documento de exemplo com erros plantados de propósito
python main.py samples/contrato-exemplo.txt
```

Saída (trecho):

```
[PASS] (error) identificacao: Documento deve ter seção de identificação - matched at line 3
[FAIL] (error) sem_placeholder: Documento não pode conter placeholders - found at line 7
RESULT: REJECTED   (exit code 1)
```

Com Docker:

```bash
docker build -t document-review-checklist .
docker run --rm -v "$PWD:/data" document-review-checklist /data/meu-documento.txt
```

### Testes

```bash
pip install -r requirements-dev.txt
pytest -v
```

Resultado: **12 testes, todos passando** ✅ (CI com GitHub Actions a cada push/PR)

### Estrutura

```
├── checker/
│   ├── document.py    # Leitura de .txt/.md/.docx
│   ├── rules.py       # Carga e validação do checklist (JSON)
│   ├── engine.py      # Motor: aplica regras, localiza evidências
│   └── report.py      # Relatório em texto ou JSON
├── rules/default.json # Checklist de exemplo (7 regras)
├── samples/           # Documento fictício com erros plantados
└── tests/             # 12 testes
```
