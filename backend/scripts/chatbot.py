from scripts.legal_knowledge import search_legal_content
from scripts.prompt_template import create_prompt
from scripts.llm_service import generate_response
from scripts.language_detector import detect_language


def chat(question):

    # Detect user language
    language = detect_language(question)

    print(f"\n[DEBUG] Language: {language}")

    # Retrieve legal context
    context = search_legal_content(
        question,
        language
    )

    print(f"[DEBUG] Context Found: {context is not None}")

    if context:
        print(f"[DEBUG] Article: {context.get('article')}")
        print(f"[DEBUG] Topic: {context.get('topic')}")
        print(f"[DEBUG] Source: {context.get('source')}")
        print(f"[DEBUG] Content Length: {len(context.get('content', ''))}")

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
    prompt = create_prompt(
        context,
        question,
        language
    )

    print("\n========== DEBUG ==========")
    print(f"Prompt Length: {len(prompt)} characters")
    print("---------------------------")
    print(prompt[:800])   # First 800 characters only
    print("---------------------------")

    # Generate response from Gemini
    try:

        response = generate_response(prompt)

        print("[DEBUG] Gemini Response Received Successfully")

        return response

    except Exception as e:

        print("\n========== ERROR ==========")
        print(e)
        print("===========================")

        if language == "am":
            return (
                "Gemini API በአሁኑ ጊዜ አይገኝም ወይም "
                "quota አልቋል። "
                "እባክዎ ቆይተው ይሞክሩ።"
            )

        return (
            "Gemini API is unavailable or "
            "quota has been exceeded. "
            "Please try again later."
        )


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