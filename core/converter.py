"""Conversion engine, independent of the GUI."""

import codecs
import re
from dataclasses import dataclass, field

from core.validator import find_unknown_codes, find_unsupported, format_warning
from mapping.code_mapping import (
    CHARACTER_SEPARATOR,
    CODE_MAP,
    REVERSE_CODE_MAP,
    WORD_SEPARATOR,
)

MODE_CHARACTER = "character"
MODE_WORD = "word"
MODE_SENTENCE = "sentence"
MODE_TEXT_TO_MORSE = "text_to_morse"
MODE_MORSE_TO_TEXT = "morse_to_text"
MODE_TEXT_TO_ROT13 = "text_to_rot13"
MODE_ROT13_TO_TEXT = "rot13_to_text"
MODE_TEXT_TO_ROT13_TO_MORSE = "text_to_rot13_to_morse"
MODE_MORSE_TO_ROT13_TO_TEXT = "morse_to_rot13_to_text"

MODE_LABELS: dict[str, str] = {
    MODE_CHARACTER: "Character",
    MODE_WORD: "Word",
    MODE_SENTENCE: "Sentence",
    MODE_TEXT_TO_MORSE: "Text \u2192 Morse",
    MODE_MORSE_TO_TEXT: "Morse \u2192 Text",
    MODE_TEXT_TO_ROT13: "Text \u2192 ROT13",
    MODE_ROT13_TO_TEXT: "ROT13 \u2192 Text",
    MODE_TEXT_TO_ROT13_TO_MORSE: "Text \u2192 ROT13 \u2192 Morse",
    MODE_MORSE_TO_ROT13_TO_TEXT: "Morse \u2192 ROT13 \u2192 Text",
}

REVERSE_MODES: dict[str, str] = {
    MODE_TEXT_TO_MORSE: MODE_MORSE_TO_TEXT,
    MODE_TEXT_TO_ROT13: MODE_ROT13_TO_TEXT,
    MODE_TEXT_TO_ROT13_TO_MORSE: MODE_MORSE_TO_ROT13_TO_TEXT,
}

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_MORSE_WORD_SPLIT = re.compile(r"\s*/\s*|\s{2,}|\n+")


@dataclass
class ConversionResult:
    output: str
    warnings: list[str] = field(default_factory=list)


def _encode_word(word: str) -> str:
    return CHARACTER_SEPARATOR.join(
        CODE_MAP[char.upper()] for char in word if char.upper() in CODE_MAP
    )


def _encode_line(line: str) -> str:
    encoded = (_encode_word(word) for word in line.split())
    return WORD_SEPARATOR.join(code for code in encoded if code)


def _text_warnings(text: str) -> list[str]:
    return [format_warning(char) for char in find_unsupported(text)]


def convert_character(text: str) -> str:
    return "\n".join(_encode_line(line) for line in text.splitlines())


def convert_words(text: str) -> list[list]:
    return [
        [word, [CODE_MAP[c.upper()] for c in word if c.upper() in CODE_MAP]]
        for word in text.split()
    ]


def convert_sentences(text: str) -> list[list[str]]:
    sentences = [s for s in _SENTENCE_SPLIT.split(text.strip()) if s]
    return [[sentence, _encode_line(sentence)] for sentence in sentences]


def text_to_morse(text: str) -> ConversionResult:
    return ConversionResult(convert_character(text), _text_warnings(text))


def morse_to_text(code: str) -> ConversionResult:
    lines: list[str] = []
    all_codes: list[str] = []
    for line in code.strip().splitlines():
        words: list[str] = []
        for chunk in _MORSE_WORD_SPLIT.split(line.strip()):
            symbols = chunk.split()
            if not symbols:
                continue
            all_codes.extend(symbols)
            words.append("".join(REVERSE_CODE_MAP.get(s, "") for s in symbols))
        lines.append(" ".join(w for w in words if w))
    warnings = [f"\u26a0 Unknown code: {c}" for c in find_unknown_codes(all_codes)]
    return ConversionResult("\n".join(lines), warnings)


def rot13(text: str) -> str:
    return codecs.encode(text, "rot13")


def convert(text: str, mode: str = MODE_CHARACTER) -> ConversionResult:
    if not text.strip():
        return ConversionResult("")

    if mode in (MODE_CHARACTER, MODE_TEXT_TO_MORSE):
        return text_to_morse(text)
    if mode == MODE_WORD:
        lines = [f"{word} \u2192 {' '.join(codes)}" for word, codes in convert_words(text)]
        return ConversionResult("\n".join(lines), _text_warnings(text))
    if mode == MODE_SENTENCE:
        lines = [f"{sentence}\n{code}" for sentence, code in convert_sentences(text)]
        return ConversionResult("\n\n".join(lines), _text_warnings(text))
    if mode == MODE_MORSE_TO_TEXT:
        return morse_to_text(text)
    if mode in (MODE_TEXT_TO_ROT13, MODE_ROT13_TO_TEXT):
        return ConversionResult(rot13(text))
    if mode == MODE_TEXT_TO_ROT13_TO_MORSE:
        return text_to_morse(rot13(text))
    if mode == MODE_MORSE_TO_ROT13_TO_TEXT:
        decoded = morse_to_text(text)
        return ConversionResult(rot13(decoded.output), decoded.warnings)
    raise ValueError(f"Unknown conversion mode: {mode}")


def convert_text(text: str, mode: str = MODE_CHARACTER) -> str:
    return convert(text, mode).output


class ConversionHistory:
    """Remembers forward conversions so reversing an output restores the exact
    original text (Morse is case-insensitive, so plain decoding loses case)."""

    def __init__(self) -> None:
        self._originals: dict[tuple[str, str], str] = {}

    def convert(self, text: str, mode: str) -> ConversionResult:
        key = (mode, text.strip())
        if key in self._originals:
            return ConversionResult(self._originals[key])
        result = convert(text, mode)
        reverse_mode = REVERSE_MODES.get(mode)
        if reverse_mode and result.output:
            self._originals[(reverse_mode, result.output.strip())] = text
        return result

    def clear(self) -> None:
        self._originals.clear()
