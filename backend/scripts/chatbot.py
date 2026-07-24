from scripts.legal_knowledge import search_legal_content
from scripts.prompt_template import create_prompt
from scripts.llm_service import generate_response
from scripts.language_detector import detect_language



def chat(question):

    # Detect language
    language = detect_language(question)


    # Search legal knowledge base
    context = search_legal_content(
        question,
        language
    )


    # If no legal information found
    if context is None:

        if language == "am":

            return """
መልስ:

በአሁኑ የሕግ መረጃ ውሂብ ውስጥ ተዛማጅ መረጃ አልተገኘም።

ምንጭ:

ምንም ተዛማጅ የሕግ ሰነድ አልተገኘም።

ማስታወሻ:

እባክዎ የተረጋገጡ የሕግ ምንጮችን ይጠቀሙ።
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


    # Create prompt
    prompt = create_prompt(
        context,
        question,
        language
    )


    # Generate Gemini response
    try:

        response = generate_response(prompt)

        return response.strip()


    except Exception:

        if language == "am":

            return """
መልስ:

Gemini API በአሁኑ ጊዜ አይገኝም።

ምንጭ:

ምንም መልስ አልተፈጠረም።

ማስታወሻ:

እባክዎ ቆይተው ይሞክሩ።
"""

        else:

            return """
Answer:

Gemini API is currently unavailable.

Relevant Source:

No response generated.

Important Note:

Please try again later.
"""



if __name__ == "__main__":


    print("Ethiopian Legal Assistant Chatbot")


    while True:

        question = input(
            "\nAsk a legal question | የሕግ ጥያቄ ይጠይቁ: "
        )


        if question.lower() == "exit":

            print("Chatbot stopped.")
            break


        answer = chat(question)


        print("\n")
        print(answer)
        print("\n")