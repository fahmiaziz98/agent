from pydantic import BaseModel, Field

class Grade(BaseModel):
    score: bool = Field(description="Boolean that indicates whether the response is accurate relative to the reference answer")
