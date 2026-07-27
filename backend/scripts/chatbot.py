from retriever import search_legal_documents
from prompt_template import create_prompt
from llm_service import generate_response
from language_detector import detect_language



def chat(question):

    # ==========================
    # Detect Language
    # ==========================

    language = detect_language(question)



    # ==========================
    # Retrieve Legal Documents
    # ==========================

    documents = search_legal_documents(
        question,
        top_k=5
    )



    # ==========================
    # No Relevant Context
    # ==========================

    if not documents:

        if language == "am":

            return """
መልስ:

በሕግ መረጃ ውሂብ ውስጥ ተዛማጅ መረጃ አልተገኘም።


ምንጭ:

ምንም ተዛማጅ የሕግ ሰነድ አልተገኘም።


ማስታወሻ:

እባክዎ የተረጋገጡ የሕግ ምንጮችን ይጠቀሙ።
"""

        else:

            return """
Answer:

No relevant legal information was found.


Relevant Source:

No matching legal document found.


Important Note:

Please use official legal sources.
"""



    # ==========================
    # Create Prompt Context
    # Send documents directly
    # ==========================

    context = documents



    # ==========================
    # Create Prompt
    # ==========================

    prompt = create_prompt(
        context,
        question,
        language
    )



    # ==========================
    # Generate Gemini Response
    # ==========================

    try:

        response = generate_response(
            prompt
        )

        return response.strip()



    except Exception as e:

        print(
            "Gemini Error:",
            e
        )


        if language == "am":

            return """
መልስ:

Gemini API ላይ ችግር ተፈጥሯል።


ማስታወሻ:

እባክዎ ቆይተው እንደገና ይሞክሩ።
"""

        else:

            return """
Answer:

Gemini API error occurred.


Important Note:

Please try again later.
"""




# ==========================
# CLI Testing
# ==========================

if __name__ == "__main__":


    print(
        "Ethiopian Legal Assistant Chatbot"
    )

    print(
        "የኢትዮጵያ የሕግ ረዳት ቻትቦት"
    )


    print(
        "Type 'exit' to quit"
    )


    while True:


        question = input(
            "\nAsk a legal question | የሕግ ጥያቄ: "
        )


        if question.lower() == "exit":

            print(
                "Chatbot stopped."
            )

            break



        answer = chat(
            question
        )


        print("\n")
        print(answer)
        print("\n")