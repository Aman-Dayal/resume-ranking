import logging
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from data.Schemas import CriteriaResponse
import asyncio
from typing import List
from api.helpers import *

logging.basicConfig(filename='app.log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.post("/extract-criteria", 
          response_model=CriteriaResponse, 
          tags=["Extraction"],
          summary="Extract job requirements from a pdf or docx and return in a list",
          description="""Extracts key requirements from uploaded job description documents.
          
          ## Supported Formats
          - PDF
          - DOCX
          
          ## Example Request
          ```json
          {
              "file": "job_description.pdf"
          }
          ```
          
          ## Example Response
          ```json
          {   
              "status_code":200,
              "criteria": [
                  "Bachelor's degree in Computer Science",
                  "5+ years of Python experience",
                  "Experience with FastAPI"
              ]
          }
          ```
          """,
          responses={
              200: {"description": "Job description processed and requirements generated sucessfully"},
              400: {"description": "Invalid file type or size"},
              422: {"description": "Unprocessable file content"},
              500: {"description": "Internal processing error"}
          })
async def extract_criteria(file: UploadFile = File(...)):
    logging.info("Extract criteria endpoint called with file: %s", file.filename)

    """Function to implement the extraction of job requirements from uploaded documents"""
    dpd = dp(file)
    text = await dpd.process()
    if "error" in text:
        logging.error("Error during text extraction: %s", text["error"])

        raise HTTPException(status_code=text["status_code"], detail=text["error"])
    result = AI().extract_criteria(text)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    logging.info("Criteria extracted successfully: %s", result.get('requirements'))
    return CriteriaResponse(status_code= 200, criteria= result.get('requirements'))


@router.post("/rank-resumes",
          tags=["Ranking"],
          summary="Rank resumes against job requirements",
          description="""Ranks multiple resumes against provided job requirements.
          
          ## Input
          - requirements: List of job requirements
          - resumes: List of resume files (PDF/DOCX)
          
          ## Output
          - Excel file with scores for each candidate along with scores for each requirement 
          
          ## Example Request
          ```json
          {
              "requirements": "[\"Python experience\", \"Degree in CS\"]",
              "resumes": ["resume1.pdf", "resume2.docx"]
          }
          ```
          """,
          responses={
              200: {"description": "Resumes processed, ranked and corresponding excel sheet is generated"},
              400: {"description": "Invalid input format (Bad Request)"},
              422: {"description": "Unsupported File Type (file type cannot be processed)"},
              500: {"description": "Internal processing error (An unknown error occured internally)"}
          })
async def rank_resumes(
    requirements: str = Form(...),
    resumes: List[UploadFile] = File(...)):
    logging.info("Rank resumes endpoint called with requirements: %s and resumes: %s", requirements, resumes)

    """process and rank resumes on basis of extracted criteria"""
    tasks = [process_resume(resume,requirements) for resume in resumes]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    final_results = []
    errors = []
    for res in results:
        if isinstance(res, HTTPException):
            logging.error("Error processing resume: %s", res.detail)
            errors.append({"error": res.detail})
        else:
            final_results.append(res)
    excel = generate_excel(final_results)
    logging.info(f"Resumes ranked successfully, returning results {final_results}.")

    return StreamingResponse(excel,status_code=200, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=resume_scores.xlsx"})
