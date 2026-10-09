from mapping.code_mapping import CODE_MAP, REVERSE_CODE_MAP

WARNING_PREFIX = "\u26a0 Unsupported character: "


def is_supported(char: str) -> bool:
    return char.isspace() or char.upper() in CODE_MAP


def find_unsupported(text: str) -> list[str]:
    seen: list[str] = []
    for char in text:
        if not is_supported(char) and char not in seen:
            seen.append(char)
    return seen


def find_unknown_codes(codes: list[str]) -> list[str]:
    seen: list[str] = []
    for code in codes:
        if code not in REVERSE_CODE_MAP and code not in seen:
            seen.append(code)
    return seen


def format_warning(char: str) -> str:
    return f"{WARNING_PREFIX}{char}"
