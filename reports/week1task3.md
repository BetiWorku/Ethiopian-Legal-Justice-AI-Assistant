# Ethiopian Legal Assistant Chatbot

## Project Description

The Ethiopian Legal Assistant Chatbot is a prototype legal information system that retrieves predefined Ethiopian legal content from a JSON knowledge base and generates controlled responses using the Gemini API.

The system accepts legal questions, matches relevant legal information, uses an LLM prompt template to generate answers, and provides the answer with source citation and legal disclaimer.

## Setup and Installation

### 1. Create Virtual Environment

python -m venv venv

Activate:

venv\Scripts\activate
2. Install Requirements
pip install -r requirements.txt

Required packages:

google-genai
python-dotenv
3. Gemini API Setup

Create a Gemini API key and add it to a .env file:

GEMINI_API_KEY=your_api_key_here

The chatbot uses Gemini API for generating legal responses.

Run the Application
python scripts/main.py
   ### Deliverables
1. Working Chatbot Prototype
The chatbot workflow is:

         User Question  
              ↓  
       main.py (User Interface)  
              ↓  
     chatbot.py (Chatbot Controller)  
              ↓  
     legal_knowledge.py (Legal Content Retrieval from JSON)  
              ↓  
     prompt_template.py (Prompt Creation with Legal Context)  
              ↓  
     llm_service.py (Gemini API Integration)  
              ↓  
     Gemini 3.1 Flash Lite (Response Generation)  
              ↓  
     Final Legal Answer with Source Citation and Legal Disclaimer

The prototype can:
- Accept user legal questions.
- Retrieve relevant legal information from the JSON knowledge base.
- Generate controlled responses using Gemini API.
- Display legal source and disclaimer.
- Handle unsupported questions safely.
2. Source Code
scripts/
├── main.py
├── chatbot.py
├── legal_knowledge.py
├── prompt_template.py
└── llm_service.py
3. JSON Legal Knowledge File
data/
└── sample_legal_content.json

Contains predefined Ethiopian legal information including:
Article
Topic
Keywords
Legal content
Source citation