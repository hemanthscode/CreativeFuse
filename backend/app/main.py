from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ai_logic import generate_idea

app = FastAPI(title="CreativeFuse Backend API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    # Add your frontend production URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IdeaRequest(BaseModel):
    domain: str
    keywords: str = ""
    style: str = "creative"

class IdeaResponse(BaseModel):
    idea: str

@app.post("/generate", response_model=IdeaResponse)
async def generate_idea_endpoint(request: IdeaRequest):
    try:
        idea_text = generate_idea(request.domain, request.keywords, request.style)
        return IdeaResponse(idea=idea_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to CreativeFuse Backend API"}
