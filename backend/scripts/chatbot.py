from scripts.legal_knowledge import search_legal_content
from scripts.prompt_template import create_prompt
from scripts.llm_service import generate_response
from scripts.language_detector import detect_language


def chat(question):

    # Detect user language
    language = detect_language(question)


    # Retrieve legal context
    context = search_legal_content(
        question,
        language
    )


    # If no matching legal information
    if context is None:

        if language == "am":

            return """
መልስ:

በአሁኑ የሕግ መረጃ ውሂብ ውስጥ ተዛማጅ መልስ አልተገኘም።

ምንጭ:

ምንም ተዛማጅ የሕግ ሰነድ አልተገኘም።

ማስታወሻ:

እባክዎ ይፋዊ የሕግ ምንጮችን ያረጋግጡ።
"""

        else:

            return """
Answer:

The answer is not available in the current legal knowledge base.

Relevant Source:

No matching legal document found.

Important Note:

Please consult official legal sources.
"""


    # Create Gemini prompt
    # Send dictionary directly
    prompt = create_prompt(
        context,
        question,
        language
    )


    # Generate response from Gemini
    response = generate_response(prompt)


    return response



if __name__ == "__main__":

    while True:

        question = input(
            "\nጥያቄዎን ያስገቡ (exit to stop): "
        )


        if question.lower() == "exit":
            print("Chatbot stopped.")
            break


        answer = chat(question)


        print("\n====================")
        print(answer)
        print("====================")