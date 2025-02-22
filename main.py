from api import routes
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

logging.basicConfig(filename='app.log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="Resume Ranking System",
    description="""API for extracting job requirements and ranking resumes.
    
    ## Features
    - Extract key requirements from job descriptions
    - Rank resumes against job requirements
    - Support for PDF and DOCX files
    - Integration with Gemini AI for text processing
    
    ## Error Codes
    - 400: Bad Request (invalid input)
    - 422: Unsupported file type (invalid file format)
    - 500: Internal Server Error (processing failure)
    """,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router, prefix="/api")

@app.get("/")
def root():
    logging.info("Root endpoint accessed")
    return {"message": "Resume Ranking System API"}

if __name__ == "__main__":
    logging.info("Starting the FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000)
