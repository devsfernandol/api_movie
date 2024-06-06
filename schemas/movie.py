
from pydantic import BaseModel, Field ,  conint, confloat
from typing import Optional, List




class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5 ,max_length=30)
    overview: str = Field(min_length=5 ,max_length=100)
    year: int = Field(le=2024)
    rating: float = Field ()
    category: str =Field (min_length=2 , max_length=30)


    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo",
                "overview": "descripcion",
                "year": 2022,
                "rating": 1.5,
                "category": "Accion"
            }
        }
        