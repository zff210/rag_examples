from pydantic import BaseModel

class GenerateQuestionsRequest(BaseModel):
    question_count: int = 10
    with_example_answer: bool = False
    append: bool = False