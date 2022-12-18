from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status = "in_progress"
    message = ""