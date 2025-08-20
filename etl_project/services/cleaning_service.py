import unicodedata

def clean_text(value: str) -> str:
    if not isinstance(value, str):
        return value
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    return value.strip()
