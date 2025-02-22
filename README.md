# Resume Ranking System

## Description
The Resume Ranking System is an API designed to extract key requirements from job descriptions and rank resumes against those requirements. It supports PDF and DOCX file formats and integrates with Gemini AI for text processing.

## Features
- Extract key requirements from job descriptions.
- Rank resumes against job requirements.
- Support for PDF and DOCX files.
- Integration with Gemini AI for text processing.

## Technologies Used
- FastAPI
- Uvicorn
- Google Gemini AI
- Pandas
- PyPDF2
- python-docx
- dotenv

## Installation
1. Clone the repository:
   ```bash
   git clone https://www.github.com/aman-dayal/resume-ranking
   
   cd resume_ranking
   ```
2. Create a virtual environment:
   ```bash
   python -m venv nvnv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     nvnv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source nvnv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Start the FastAPI application:
   ```bash
   python main.py
   ```
2. Access the API at `http://localhost:8000/docs`.

### API Endpoints
- **POST /api/rank-resumes**: Rank resumes against job requirements.
- **POST /api/extract-criteria**: Extract key requirements from job descriptions.

## Logging
The application logs important events and errors to `app.log.txt`. This file can be used for monitoring and debugging purposes.


