from retrieval import search_legal_documents
from prompt_template import create_prompt
from llm_service import generate_response
from language_detector import detect_language
from context_builder import build_context
from logger import save_log



def chat(question):

    language = detect_language(question)


    # Validate empty input

    if not question.strip():

        return "Please enter a legal question."


    # Retrieve

    documents = search_legal_documents(
        question,
        top_k=5,
        threshold=0.75
    )


    # Safe fallback

    if not documents:

        return fallback_response(language)



    # Build legal context

    context = build_context(
        documents
    )


    # Create RAG prompt

    prompt = create_prompt(
        context,
        question,
        language
    )


    # Gemini generation

    answer = generate_response(
        prompt
    )


    # Logging

    save_log(
        question,
        documents,
        answer
    )


    return answer.strip()