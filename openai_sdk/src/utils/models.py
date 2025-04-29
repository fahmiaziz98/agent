from pydantic import BaseModel, Field

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

class ChrunDetectionOutput(BaseModel):
    is_churn_risk: bool = Field(description="Whether the user message indicates a potential risk.")
    reasoning: str = Field(description="Reasoning behind the churn risk detection.")
