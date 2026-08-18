# Alphabetic Code Generator – Developer's Guide

## Architecture Overview

This project separates concerns into distinct layers:

- **Mapping Layer** (`mapping/`): Single source of truth for all character-to-code mappings.
- **Core Engine** (`core/`): Conversion logic independent of UI.
- **GUI Layer** (`gui/`): PySide6-based desktop application.
- **Utilities** (`utils/`): Clipboard, validation, and helper functions.
- **Tests** (`tests/`): Pytest-based test suite.

## Mapping Data Structure

The mapping is stored as a Python dictionary in [mapping/code_mapping.py](mapping/code_mapping.py):

```python
CODE_MAP = {
    "A": ".-",
    "B": "-...",
    # ... all characters
}
```

To update the mapping:

1. Edit `mapping/code_mapping.py`.
2. Run tests to verify consistency: `pytest tests/test_converter.py -v`.
3. The GUI reference table will automatically reflect the new mapping.

## Conversion Engine

The core engine is in [core/converter.py](core/converter.py) and supports three modes:

1. **Character mode**: Converts each character individually.
2. **Word mode**: Returns a list of [word, [codes]].
3. **Sentence mode**: Splits by sentence boundaries and converts each.

Example:

```python
from core.converter import convert_text

result = convert_text("HELLO", mode="character")
# Result: ".... . .-.. .-.. ---"
```

## Adding New Features

### New Conversion Mode

1. Add logic to `core/converter.py`.
2. Add corresponding test in `tests/test_converter.py`.
3. Update `gui/main_window.py` to expose the mode in the UI.

### New Punctuation or Character

1. Add the character and its code to `CODE_MAP` in `mapping/code_mapping.py`.
2. Run tests to verify.
3. The mapping reference table updates automatically.

### GUI Improvements

The main window is in [gui/main_window.py](gui/main_window.py). PySide6 components:

- `mapping_view.py`: Displays the complete mapping table with filtering.
- `notes_view.py`: Help and explanatory text.
- `main_window.py`: Main application window.

## Testing

All tests use pytest:

```bash
pytest tests/test_converter.py -v
```

Tests cover:

- Character, word, and sentence conversion modes.
- Uppercase/lowercase normalization.
- Space and punctuation handling.
- Unsupported character warnings.
- Empty input handling.
- Mapping completeness.

## Multi-Language Implementation

The conversion engine is designed to be language-agnostic. To implement in another language:

1. Load the mapping from [shared/code_mapping.json](shared/code_mapping.json) or rewrite it inline.
2. Implement the three conversion functions (character, word, sentence).
3. Match the exact output format.
4. Add equivalent tests.

Example structure for JavaScript:

```
alphabetic-code-generator/
├── python/
│   └── ...
├── javascript/
│   ├── src/
│   │   ├── mapping.js
│   │   ├── converter.js
│   │   └── gui.js
│   └── tests/
│       └── converter.test.js
└── shared/
    └── code_mapping.json
```

## Deployment

### Local Development

```bash
pip install -r requirements.txt
python app.py
```

### GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/python-tests.yml`) that:

1. Checks out the code.
2. Sets up Python 3.11+.
3. Installs dependencies.
4. Runs pytest.

Trigger: Push to main or pull requests.

## Troubleshooting

### Import errors

Ensure all required packages are installed:

```bash
pip install -r requirements.txt
```

### PySide6 installation fails

PySide6 is large (~170MB). If installation stalls:

1. Check your network connection.
2. Try installing with a longer timeout: `pip install --default-timeout=1000 PySide6`.
3. Consider using a pre-built Python distribution (Anaconda, for example).

### Tests fail

1. Check that `pytest` is installed: `pip install pytest`.
2. Verify the current directory: `cd` to the project root.
3. Run with verbose output: `pytest -v`.

## Contributing

1. Create a new branch: `git checkout -b feature/my-feature`.
2. Make changes and add tests.
3. Run `pytest` to verify.
4. Commit: `git commit -m "Add my feature"`.
5. Push: `git push origin feature/my-feature`.
6. Open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
