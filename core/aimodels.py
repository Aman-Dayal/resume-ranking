from google import genai
from dotenv import load_dotenv
import os
import logging
import json

load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class models:
    def __init__(self):        
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = 'models/gemini-1.5-flash-001'

    def extract_criteria(self, job_description):
        logging.info("Extracting criteria from job description")
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"""
                        Analyse and validate if the provided text is a job description, if not, return "INVALID_INPUT",
                        Extract all key requirements from this job description such as skills, certifications, experience, and qualifications:
                        {job_description}
                        Format:
                            - Each requirement should be a clear, self-contained statement.
                            - No bullet points, hyphens or numbers.
                            - requirement must be a quantifiable metric
                            - requirement must be a must have , no nice to haves
                        Return only the extracted requirements as a plain list.
                """
            )
            if response.text.strip() == "INVALID_INPUT":
                logging.error("Invalid job description provided")
                return {"error": "Not a valid Job Description", "status_code": 400}

            logging.info("Criteria extracted successfully")
            return {"requirements": response.text.strip().split('\n'), "code": 200}

        except Exception as e:
            logging.error("Extraction failed: %s", str(e))
            return {"error": f"Extraction failed: {str(e)}", "status_code": 500}   
    
    def rank_resumes(self, req_ls, resume):
        logging.info("Ranking resumes with requirements: %s", req_ls)
        candidate_score = self.client.models.generate_content(
            model=self.model,
            contents=(f"""You are a resume ranking and analysis expert, rank the resume you are provided as per the requirements.
                    For each requirement, provide Score (0-5), 0 being the least matched and 5 being most:

                    Requirements:
                    {req_ls}

                    Resume:
                    {resume}
                    
                    Return a string response only as "NOT_VALID" and nothing else, if:
                        - The Resume is not valid resume from a candidate
                        - job requirements are not valid requirements
                    if not NOT_VALID, Return a valid dictionary, where:
                        - The first key is 'Candidate Name' with the candidate's name.
                        - Each job requirement is a key and its score (integer) is the value.
                    """
            )
        )
        if "NOT_VALID" in candidate_score.text.strip():
            logging.error("Not a valid Resume or Job Requirements")
            return {"error": "Not a valid Resume or Job Requirements", "status_code": 400}
        
        logging.info("Resumes ranked successfully")
        return {"response": candidate_score.text.lstrip("```json").rstrip("```"), "status_code": 200}
    
    def shorten_requirements(self, req_ls):
        logging.info("Shortening requirements: %s", req_ls)
        req_dic = self.client.models.generate_content(
            model=self.model,
            contents=(f"""Convert these requirements into labels and generate a dictionary with these requirements as keys and corresponding labels as the values
                    {req_ls}
                  return only the generate labels dictionary as a json
                """
            )
        )
        logging.info("Requirements shortened successfully")
        return json.loads(req_dic.text.lstrip("```json").rstrip("```"))
