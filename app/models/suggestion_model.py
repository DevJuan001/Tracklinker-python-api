from pydantic import BaseModel

class SuggestionModel(BaseModel):
    suggestion: str