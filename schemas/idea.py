from pydantic import BaseModel


class IdeaResponse(BaseModel):
    id: int
    title: str
    summary: str
    category: str
    funding_needed: float
    equity_offered: float
    funded_amount: float
    funding_progress: float
    product_image: str | None = None
