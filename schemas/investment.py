from pydantic import BaseModel


class InvestmentRequest(BaseModel):
    idea_id: int
    amount: float


class InvestmentResponse(BaseModel):
    id: int
    idea_id: int
    investor_id: int
    amount: float
    status: str
