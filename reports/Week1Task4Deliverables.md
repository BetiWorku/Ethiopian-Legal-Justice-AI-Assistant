# Task 4: Testing, Method Review, and Limitation Analysis

## 1. Chatbot Testing Results

The chatbot was tested using five legal information questions to evaluate retrieval accuracy, response quality, source citation, and safe handling of unsupported questions.

| No | Legal Question | Response Quality Comment |
|---|---|---|
| 1 | What does Article 25 say about equality? | The chatbot correctly retrieved Article 25 from the legal knowledge base and generated an accurate response with source citation and legal disclaimer. |
| 2 | What are accused persons' rights? | The chatbot correctly identified Article 20 and provided relevant information about accused persons' rights with the correct legal source. |
| 3 | What is Article 19 about? | The chatbot successfully retrieved Article 19 and generated a clear explanation about rights during arrest with source citation. |
| 4 | What are the requirements of a contract? | The chatbot correctly matched Ethiopian Civil Code Article 1725 and provided the required contract information with the relevant source. |
| 5 | What is Article 100 about? | The chatbot safely handled an unsupported question by returning that the information was not available in the current knowledge base. |


## Testing Summary

The chatbot successfully answered supported legal questions by retrieving relevant information from the JSON legal knowledge base and generating responses using the Gemini API.

The testing showed that the system can:

- Retrieve relevant legal information from predefined documents.
- Generate controlled responses using Gemini API.
- Provide legal source citations.
- Include legal disclaimers.
- Handle unsupported questions safely without generating unsupported information.
---
## 2. LLM Method Review

### Selected LLM Method: API-Based Inference (Gemini API)

The chatbot uses an API-based LLM inference approach with Google Gemini 3.1 Flash Lite for generating legal information responses.

Instead of directly asking the LLM legal questions, the system first retrieves relevant legal information from the predefined JSON knowledge base. The retrieved legal content is then passed to Gemini through a prompt template. Gemini generates a controlled response using the provided legal context.

### LLM Workflow

User Question
      |
      v
Legal Knowledge Retrieval
(JSON Knowledge Base)
      |
      v
Prompt Template
(Context + Question + Instructions)
      |
      v
Gemini 3.1 Flash Lite API
      |
      v
Final Legal Response

### Advantages of the Selected Method

- Easy integration through API.
- Does not require local hardware resources.
- Provides high-quality natural language responses.
- Supports prompt-based control to restrict answers to legal context.
- Suitable for a Week 1 prototype implementation.
---
## 3. Limitation Analysis

Although the chatbot successfully demonstrates legal information retrieval and LLM integration, the Week 1 prototype has some limitations:

### 1. Limited Legal Knowledge Base

The chatbot only uses a small predefined JSON file containing sample legal documents. It cannot answer questions about legal information that is not included in the knowledge base.

### 2. Keyword-Based Retrieval

The current retrieval system uses keyword matching. It may fail when users ask questions using different words or sentence structures.

Example:

Stored keyword:
accused

User question:
What rights does a person charged with a crime have?
The system may not identify the correct document.

### 3. No Semantic Search

The prototype does not use embeddings or vector databases. Therefore, it cannot understand the deeper meaning of questions or find similar legal documents based on context.

### 4. Limited Document Coverage

Only sample Ethiopian legal documents are included. A production system would require a larger collection of Ethiopian laws, regulations, court decisions, and legal documents.

### 5. Dependence on External API

The chatbot uses Gemini API as a cloud-based LLM service. Therefore, it requires an internet connection and depends on API availability for response generation.

### 6. No Conversation Memory

The current prototype handles each question independently and does not maintain previous conversation history.