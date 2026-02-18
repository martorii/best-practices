from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user query to process.")


class ToolInfo(BaseModel):
    name: str
    description: str
