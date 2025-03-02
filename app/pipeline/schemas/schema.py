from pydantic import BaseModel
import os
import sys


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "pipeline")))

class TableSchema(BaseModel):

    class Config:
        from_attributes = True
