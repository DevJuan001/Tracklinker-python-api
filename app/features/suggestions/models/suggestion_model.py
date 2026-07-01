from pydantic import BaseModel

from app.utils.safe_types import safe_str


class SuggestionModel(BaseModel):
    suggestion: str = safe_str(min_length=3, max_length=1000)
