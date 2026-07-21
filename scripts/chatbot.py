from legal_knowledge import search_legal_content
from prompt_template import create_prompt
from llm_service import generate_response


def chat(question):

    context = search_legal_content(question)

    if context is None:
        return """
Answer:
The answer is not available in the current knowledge base.

Relevant Source:
No matching legal document found.

Important Note:
Please consult official legal sources for further information.
"""

    prompt = create_prompt(
        context,
        question
    )

    response = generate_response(prompt)

    return response