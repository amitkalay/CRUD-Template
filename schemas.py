from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

# Column Names: ['id', 'Region', 'Year', 'Percentage_using', 'Source']
class InternetUsageDataSchema(BaseModel):
    id: int
    Region: str
    Year: int
    Percentage_using: float
    Source: str

class InternetUsageDataCreate(BaseModel):
    Region: str
    Year: int
    Percentage_using: float
    Source: str