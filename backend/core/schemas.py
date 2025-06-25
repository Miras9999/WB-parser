from pydantic import BaseModel


class WbProductRawSchema(BaseModel):
    id: int
    name: str
    priceU: int
    salePriceU: int
    rating: float
    feedbacks: int
