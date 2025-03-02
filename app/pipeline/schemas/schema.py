from pydantic import BaseModel


class TableSchema(BaseModel):

    class Config:
        from_attributes = True
