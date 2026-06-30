import re
from typing import Optional
from pydantic.fields import FieldInfo
from pydantic import AfterValidator, Field


_HTML_TAG = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")
_SCRIPT_PROTOCOL = re.compile(r"javascript\s*:", re.IGNORECASE)
_EVENT_HANDLER = re.compile(r"\bon[a-zA-Z]+\s*=", re.IGNORECASE)
_SQLI_LIKE = re.compile(
    r"(--|;|\bunion\s+select\b|\bor\s+1\s*=\s*1\b)", re.IGNORECASE)
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

_DANGEROUS_PATTERNS = (
    _HTML_TAG,
    _SCRIPT_PROTOCOL,
    _EVENT_HANDLER,
    _SQLI_LIKE,
    _CONTROL_CHARS,
)


def _validate(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    for pattern in _DANGEROUS_PATTERNS:
        if pattern.search(value):
            raise ValueError(
                "La cadena contiene caracteres o patrones no permitidos"
            )

    return value.strip()


def safe_str(*, max_length: int = 100) -> FieldInfo:
    field = Field(..., max_length=max_length)
    field.metadata.append(AfterValidator(_validate))
    return field


def safe_optional_str(*, max_length: int = 100) -> FieldInfo:
    field = Field(default=None, max_length=max_length)
    field.metadata.append(AfterValidator(_validate))
    return field
