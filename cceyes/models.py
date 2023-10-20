from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class StatusEnum(str, Enum):
    Concept = "Concept"
    InDevelopment = "In Development"
    PostProduction = "Post-Production"
    Completed = "Completed"
    Released = "Released"
    OnHiatus = "On Hiatus"
    Cancelled = "Cancelled"
    Archived = "Archived"


class ProductionReviews(BaseModel):
    rating: float = Field(
        ..., title="Average rating from 0 to 10 from audiences or critics", ge=0, le=10
    )
    count: int = Field(0, title="Number of reviews", ge=0)
    popularity: float = Field(
        ...,
        title="Rating from 0 (smallest audience size) to 10 (largest audience size)",
        ge=0,
        le=10,
    )

    class Config:
        json_schema_extra = {"example": {"rating": 7.5, "count": 10, "popularity": 8.5}}


class ProductionStatus(BaseModel):
    current_status: StatusEnum
    last_updated: str
    notes: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "current_status": "In Development",
                "last_updated": "2023-08-14",
                "notes": "The script is in its final stages, expected to move to post-production by September.",
            }
        }


class ProductionExtra(BaseModel):
    model_config = {"extra": "allow"}


class ProductionBaseMeta(BaseModel):
    id: str


class ProductionMeta(ProductionBaseMeta):
    title: str
    image: str | None = None
    status: ProductionStatus | None = None
    ratings: ProductionReviews | None = None
    extra: ProductionExtra | None = None

    def model_dump(self, **kwargs):
        return super().model_dump(**kwargs)


class ProductionDataset(BaseModel):
    type: str
    provider: str


class BaseProduction(BaseModel):
    title: str = Field(..., title="Production title", max_length=255)
    content: str = Field(..., title="Production content", max_length=1000)
    dataset: ProductionDataset = Field(..., title="Production dataset")
    meta: ProductionMeta = Field(..., title="Production meta")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Lost in Time",
                "content": "Dr. Clara Maxwell, a brilliant but eccentric physicist, stumbles upon a groundbreaking discovery - a watch-like device that can transport the wearer through time. When her teenage son, Jack, accidentally activates the device, he is flung into different eras every time he falls asleep. In every episode, Clara, her faithful assistant Reuben, and Jack’s best friend Lily must decipher clues left by Jack about his location in time. As they race against the clock, they must navigate the perils of history, while trying to bring back Jack, one era at a time.",
                "dataset": {"type": "TV Series", "provider": "BetaSeries"},
                "meta": {
                    "id": 1,
                    "title": "Lost in Time",
                    "image": "https://placehold.co/300x400",
                },
            }
        }


class Production(BaseProduction):
    id: int = Field(None, title="Production ID", examples=[1])
    score: Optional[float] = Field(None, title="Relevance score", examples=[0.5])
