# Alphabetic Code Generator

A polished Python desktop application that converts normal text into a custom alphabetic code based on a supplied mapping table. The project keeps the mapping data separate from the conversion logic so it can be updated later without rewriting the engine.

## Features

- Character, word, and sentence conversion modes
- Separate original text and generated code panels
- Copy-to-clipboard support
- Clear input and output controls
- Full mapping reference table with filter/search
- Help and notes section
- Unsupported-character warnings instead of silent deletion
- Dark, modern desktop UI with PySide6
- Automated test coverage for conversion behavior

## Supported conversion modes

1. Character mode: converts each character individually.
2. Word mode: converts each word independently.
3. Sentence mode: splits by sentence boundaries and converts each sentence.

## Mapping rules

This project uses the supplied alphabetic code mapping as the single source of truth. Uppercase and lowercase letters resolve to the same code. Spaces are preserved as structural separators and are not encoded as a character. Unsupported characters trigger a warning in the format `⚠ Unsupported character: X`.

The mapping is stored in [mapping/code_mapping.py](mapping/code_mapping.py).

## Installation

```bash
cd alphabetic-code-generator
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
cd alphabetic-code-generator
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

## Run tests

```bash
pytest -q
```

## Example

Input:

```text
HELLO WORLD
```

Character mode output:

```text
.... . .-.. .-.. ---  .-- --- .-. .-.. -..
```

The exact mapping must be checked against the project’s canonical values in the source mapping file.

## Project structure

```text
alphabetic-code-generator/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── mapping/
│   ├── __init__.py
│   └── code_mapping.py
├── core/
│   ├── __init__.py
│   ├── converter.py
│   └── validator.py
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── mapping_view.py
│   └── notes_view.py
├── utils/
│   ├── __init__.py
│   └── clipboard.py
├── tests/
│   └── test_converter.py
└── .github/
    └── workflows/
        └── python-tests.yml
```

## Unsupported characters

Unsupported characters are not dropped silently. They are surfaced as warnings to keep the conversion transparent and predictable.

## Multi-language compatibility

The conversion logic is intentionally separated from the UI so the same mapping and conversion rules can be reused in other languages later. The mapping file is designed to be portable and easy to adapt to JSON, JavaScript, TypeScript, Java, C#, Go, or C++ implementations.

## GitHub setup

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Future updates:

```bash
git add .
git commit -m "Describe your changes"
git push
```

## License

This project uses the MIT license. It is included in the repository as [LICENSE](LICENSE).

## Contributing

Contributions are welcome. Please open an issue first to discuss the change and then submit a pull request with a clear description of the proposed update.

## Future improvements

- real-time conversion toggle while typing
- export to plain text or file
- richer JSON import/export for mapping definitions
- web version built on the same conversion engine
