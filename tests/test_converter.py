import pytest

from core.converter import (
    MODE_CHARACTER,
    MODE_MORSE_TO_ROT13_TO_TEXT,
    MODE_MORSE_TO_TEXT,
    MODE_ROT13_TO_TEXT,
    MODE_SENTENCE,
    MODE_TEXT_TO_MORSE,
    MODE_TEXT_TO_ROT13,
    MODE_TEXT_TO_ROT13_TO_MORSE,
    MODE_WORD,
    ConversionHistory,
    convert,
    convert_sentences,
    convert_text,
    convert_words,
    rot13,
)
from mapping.code_mapping import CODE_MAP, REVERSE_CODE_MAP


def test_character_mode_matches_readme_example():
    assert convert_text("HELLO WORLD") == ".... . .-.. .-.. ---  .-- --- .-. .-.. -.."


def test_case_insensitive():
    assert convert_text("hello", MODE_CHARACTER) == convert_text("HELLO", MODE_CHARACTER)


def test_multiple_spaces_collapse_to_single_word_gap():
    assert convert_text("A   B") == ".-  -..."


def test_word_mode():
    assert convert_words("Hi there") == [["Hi", ["....", ".."]], ["there", ["-", "....", ".", ".-.", "."]]]
    assert convert_text("Hi", MODE_WORD) == "Hi \u2192 .... .."


def test_sentence_mode():
    assert convert_sentences("Hi. Go!") == [["Hi.", ".... .. .-.-.-"], ["Go!", "--. --- -.-.--"]]
    assert convert_text("Hi. Go!", MODE_SENTENCE) == "Hi.\n.... .. .-.-.-\n\nGo!\n--. --- -.-.--"


def test_unsupported_characters_warn():
    result = convert("A#B#~", MODE_CHARACTER)
    assert result.output == ".- -..."
    assert result.warnings == ["\u26a0 Unsupported character: #", "\u26a0 Unsupported character: ~"]


def test_empty_input():
    assert convert("   ", MODE_CHARACTER).output == ""
    assert convert("", MODE_MORSE_TO_TEXT).output == ""


def test_numbers_and_punctuation_roundtrip():
    text = "SOS 123, OK?"
    encoded = convert_text(text, MODE_TEXT_TO_MORSE)
    assert convert_text(encoded, MODE_MORSE_TO_TEXT) == text


@pytest.mark.parametrize("separator", ["  ", " / ", "/", "\n"])
def test_morse_decoding_word_separators(separator):
    code = f".... ..{separator}- .... . .-. ."
    expected = "HI\nTHERE" if separator == "\n" else "HI THERE"
    assert convert_text(code, MODE_MORSE_TO_TEXT) == expected


def test_unknown_morse_code_warns():
    result = convert(".- ...---... -...", MODE_MORSE_TO_TEXT)
    assert result.output == "AB"
    assert result.warnings == ["\u26a0 Unknown code: ...---..."]


def test_rot13_preserves_non_letters():
    assert rot13("Hello, World! 123") == "Uryyb, Jbeyq! 123"
    assert convert_text("Uryyb, Jbeyq! 123", MODE_ROT13_TO_TEXT) == "Hello, World! 123"
    assert convert_text("Hello", MODE_TEXT_TO_ROT13) == "Uryyb"


def test_rot13_morse_pipeline():
    encoded = convert_text("HELLO", MODE_TEXT_TO_ROT13_TO_MORSE)
    assert encoded == convert_text("URYYB", MODE_TEXT_TO_MORSE)
    assert convert_text(encoded, MODE_MORSE_TO_ROT13_TO_TEXT) == "HELLO"


def test_history_backtracking_restores_case():
    history = ConversionHistory()
    encoded = history.convert("Hello World", MODE_TEXT_TO_ROT13_TO_MORSE).output
    assert history.convert(encoded, MODE_MORSE_TO_ROT13_TO_TEXT).output == "Hello World"
    history.clear()
    assert history.convert(encoded, MODE_MORSE_TO_ROT13_TO_TEXT).output == "HELLO WORLD"


def test_unknown_mode_raises():
    with pytest.raises(ValueError):
        convert("abc", "nope")


def test_mapping_completeness():
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        assert char in CODE_MAP
    assert len(REVERSE_CODE_MAP) == len(CODE_MAP)
