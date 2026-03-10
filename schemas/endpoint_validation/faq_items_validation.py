from pydantic import BaseModel

class FaqItem(BaseModel):
    title: str
    question: str
    answer: str
    category: str
