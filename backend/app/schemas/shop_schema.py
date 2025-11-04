from pydantic import BaseModel

class OfferBuyRequest(BaseModel):
    offer_id: str