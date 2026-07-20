from legal_knowledge import load_legal_content, search_legal_content
from prompt_template import create_prompt
from llm_service import generate_response


def chatbot(question):

    if not question.strip():
        return "Please enter a legal question."


    legal_data = load_legal_content()


    context = search_legal_content(
        question,
        legal_data
    )


    if context is None:

        return """
Answer:
The answer is not available in the current knowledge base.

Relevant Source:
No relevant source available.

Important Note:
This response provides general legal information only and is not legal advice.
"""


    prompt = create_prompt(
        context,
        question
    )


    answer = generate_response(prompt)


    return answer