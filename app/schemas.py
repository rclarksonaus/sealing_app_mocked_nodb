from pydantic import BaseModel
from typing import List

class InputData(BaseModel):
    temp_c: float
    pressure_bar: float
    media_type: str
    movement_type: str
    space_constraint: str

class GradeResult(BaseModel):
    grade_id: int
    score: float
    reason: str

class RecommendResponse(BaseModel):
    results: List[GradeResult]
