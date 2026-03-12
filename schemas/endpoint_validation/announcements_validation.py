from pydantic import BaseModel

class CreateAnnouncementSchema(BaseModel):
    title: str
    content: str
    target_role: str

class DeleteAnnouncementSchema(BaseModel):
    details: str