from pydantic import BaseModel, Field
from typing import List

class CriteriaResponse(BaseModel):
    status_code: int = Field(...,title="status code associated with the response")
    criteria: List[str] = Field(..., alias="criteria",title="requirements",description="Job description highlighting the key requirements of the job")