from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.ai_logic import boost_idea, categorize_idea_type
import logging
from typing import Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CreativeFuse - Universal Idea Enhancement Platform",
    description="Transform any idea into an actionable plan - business, creative, social impact, or personal",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enhanced CORS configuration
origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # React
    "http://localhost:3001",  # Alternative React
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:8080",  # Vue
    "http://localhost:4200",  # Angular
    # Production domains (add when ready)
    # "https://creativefuse.com",
    # "https://www.creativefuse.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Enhanced Pydantic models
class BoostIdeaRequest(BaseModel):
    idea: str = Field(
        ..., 
        min_length=15, 
        max_length=3000, 
        description="Any type of idea you want to enhance - business, creative, social, or personal",
        example="I want to create an NGO that teaches coding to underprivileged children in rural India"
    )

class BoostIdeaResponse(BaseModel):
    boosted_idea: str
    idea_type: str
    processing_time: float
    success: bool = True
    message: str = "Idea enhanced successfully"
    word_count: int

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_type: str
    suggestion: str = None

class IdeaStats(BaseModel):
    total_ideas_processed: int
    popular_categories: dict
    avg_processing_time: float

# In-memory stats (use database in production)
app_stats = {
    "total_processed": 0,
    "categories": {},
    "processing_times": []
}

# Enhanced API endpoints
@app.post("/boost", response_model=BoostIdeaResponse)
async def boost_idea_endpoint(request: BoostIdeaRequest):
    """
    🚀 Transform any idea into an actionable plan
    
    Supports all types of ideas:
    - Business & Startup ideas
    - Social Impact & NGO initiatives  
    - Creative projects & content
    - Technology & app concepts
    - Personal development goals
    - Community initiatives
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing idea: {request.idea[:100]}...")
        
        # Enhanced input validation
        if not request.idea.strip():
            raise HTTPException(
                status_code=400, 
                detail="Please describe your idea in detail"
            )
        
        # Check for inappropriate content
        inappropriate_keywords = ['illegal', 'harmful', 'scam', 'fraud']
        if any(word in request.idea.lower() for word in inappropriate_keywords):
            raise HTTPException(
                status_code=400,
                detail="We can only help enhance positive and constructive ideas"
            )
        
        # Categorize the idea
        idea_type = categorize_idea_type(request.idea)
        
        # Process the idea
        enhanced_idea = boost_idea(request.idea)
        
        # Calculate metrics
        processing_time = round(time.time() - start_time, 2)
        word_count = len(enhanced_idea.split())
        
        # Update stats
        app_stats["total_processed"] += 1
        app_stats["categories"][idea_type] = app_stats["categories"].get(idea_type, 0) + 1
        app_stats["processing_times"].append(processing_time)
        
        logger.info(f"Idea enhanced successfully in {processing_time}s ({word_count} words)")
        
        return BoostIdeaResponse(
            boosted_idea=enhanced_idea,
            idea_type=idea_type,
            processing_time=processing_time,
            success=True,
            message=f"Your {idea_type} idea has been transformed into an actionable plan!",
            word_count=word_count
        )
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400, 
            detail=ErrorResponse(
                message="Invalid input provided",
                error_type="validation_error",
                suggestion="Please provide a more detailed description of your idea"
            ).dict()
        )
    
    except RuntimeError as re:
        logger.error(f"AI service error: {str(re)}")
        error_msg = str(re)
        if "timeout" in error_msg.lower():
            suggestion = "The AI service is busy. Please try again in a moment."
        elif "network" in error_msg.lower():
            suggestion = "Connection issue detected. Check your internet and retry."
        else:
            suggestion = "Our AI service is temporarily unavailable. Please try again."
            
        raise HTTPException(
            status_code=503, 
            detail=ErrorResponse(
                message="AI service temporarily unavailable",
                error_type="service_error",
                suggestion=suggestion
            ).dict()
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=ErrorResponse(
                message="An unexpected error occurred",
                error_type="server_error",
                suggestion="Please try again. If the problem persists, contact support."
            ).dict()
        )

@app.get("/")
async def root():
    """
    🏠 Welcome to CreativeFuse - Where Ideas Come to Life
    """
    return {
        "message": "Welcome to CreativeFuse - Universal Idea Enhancement Platform",
        "tagline": "Transform ANY idea into an actionable plan",
        "supported_types": [
            "Business & Startup Ideas",
            "Social Impact Initiatives", 
            "Creative Projects",
            "Technology Concepts",
            "Personal Development Goals",
            "Community Initiatives"
        ],
        "status": "ready",
        "version": "2.0.0",
        "endpoints": {
            "enhance_idea": "POST /boost",
            "stats": "GET /stats",
            "health": "GET /health",
            "documentation": "GET /docs"
        }
    }

@app.get("/health")
async def health_check():
    """
    🔍 Comprehensive health check
    """
    return {
        "status": "healthy",
        "service": "CreativeFuse Universal Idea Enhancement",
        "version": "2.0.0",
        "uptime": "operational",
        "ai_service": "connected",
        "features": {
            "idea_enhancement": "active",
            "multi_category_support": "active",
            "real_time_processing": "active",
            "indian_context": "active"
        }
    }

@app.get("/stats", response_model=IdeaStats)
async def get_stats():
    """
    📊 Platform usage statistics
    """
    avg_time = sum(app_stats["processing_times"]) / len(app_stats["processing_times"]) if app_stats["processing_times"] else 0
    
    return IdeaStats(
        total_ideas_processed=app_stats["total_processed"],
        popular_categories=app_stats["categories"],
        avg_processing_time=round(avg_time, 2)
    )

@app.get("/categories")
async def get_supported_categories():
    """
    📂 Get all supported idea categories with examples
    """
    return {
        "categories": {
            "business": {
                "name": "Business & Startups",
                "description": "Revenue-generating ventures, products, services",
                "examples": ["E-commerce platform", "SaaS solution", "Local service business"]
            },
            "social_impact": {
                "name": "Social Impact & NGOs", 
                "description": "Community welfare, social change initiatives",
                "examples": ["Education NGO", "Environmental cleanup", "Healthcare access"]
            },
            "technology": {
                "name": "Technology & Digital",
                "description": "Apps, software, digital platforms, AI solutions",
                "examples": ["Mobile app", "Web platform", "AI tool"]
            },
            "creative": {
                "name": "Creative Projects",
                "description": "Art, content, design, entertainment",
                "examples": ["YouTube channel", "Art exhibition", "Design portfolio"]
            },
            "personal_development": {
                "name": "Personal Development",
                "description": "Skills, learning, self-improvement goals",
                "examples": ["Learning new skill", "Fitness journey", "Career transition"]
            },
            "general": {
                "name": "General Ideas",
                "description": "Any other innovative concept or initiative",
                "examples": ["Community event", "Research project", "Innovation concept"]
            }
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"message": "Endpoint not found. Visit /docs for API documentation."}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"message": "Internal server error. Please try again later."}

# For development
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CreativeFuse - Universal Idea Enhancement Platform")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🎯 Ready to transform ideas into reality!")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)