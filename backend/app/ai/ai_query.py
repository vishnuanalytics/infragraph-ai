from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ai.rag_engine import answer_question

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

# Sample questions you show during the interview demo
SAMPLE_QUESTIONS = [
    "Which compressors have had critical incidents?",
    "What is the current status of all assets with open incidents?",
    "Which assets are at highest risk right now?",
    "What maintenance work was done on Compressor C-101?",
    "Which failure modes have caused the most incidents?",
    "What is the total maintenance cost across all assets?",
    "Are there any assets that share the same failure mode?",
    "Which plant has the most incidents?"
]

@router.post("/ask")
def ask_question(request: QuestionRequest):
    if not request.question or len(request.question.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Question too short. Please ask a complete question."
        )
    result = answer_question(request.question)
    return result

@router.get("/sample-questions")
def get_sample_questions():
    return {
        "description": "Sample questions you can ask the AI about the knowledge graph",
        "questions": SAMPLE_QUESTIONS
    }