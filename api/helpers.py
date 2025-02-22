import logging
from core.file_processor import DocProcessor as dp
from core.aimodels import models as AI
from fastapi import HTTPException
import pandas as pd
from io import BytesIO
import json

# Configure logging
logging.basicConfig(filename='app.log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_resume(resume, requirements):
    logging.info("Processing resume: %s with requirements: %s", resume.filename, requirements)
    dpd = dp(resume)
    text = await dpd.process()
    if "error" in text:
        logging.error("Error processing resume: %s", text["error"])
        raise HTTPException(status_code=text["status_code"], detail=text["error"])
    
    result = AI().rank_resumes(requirements, text)
    if "error" in result:
        logging.error("Error ranking resumes: %s", result["error"])
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    
    logging.info("Successfully processed resume: %s", resume.filename)
    return json.loads(result['response'])

def generate_excel(results):
    logging.info("Generating Excel file from results with %d entries", len(results))
    df = pd.DataFrame(results)
    output = BytesIO()
    colmap = AI().shorten_requirements(list(df.columns))
    df.rename(columns=colmap,inplace=True)
    df['Total Score'] = df.drop('Candidate Name', axis=1).sum(axis=1)

    df.to_excel(output)
    output.seek(0)
    logging.info("Excel file generated successfully")
    return output
