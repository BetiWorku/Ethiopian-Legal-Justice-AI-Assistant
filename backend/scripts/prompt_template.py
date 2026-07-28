def create_prompt(context, question, language):

    legal_context = ""

    for index, doc in enumerate(context, start=1):
        if isinstance(doc, dict):
            legal_context += f"""
==============================
Retrieved Legal Context {index}
==============================
Document: {doc.get("document", "FDRE Constitution")}
Article: {doc.get("article", "Unknown")}
Article Title: {doc.get("title", "Unknown")}
Pages: {doc.get("pages", "Unknown")}
Legal Text: {doc.get("text", "")}
"""

    if language == "am":
        language_instruction = "Answer ONLY in Amharic language. Use Amharic script. Translate legal explanations naturally while keeping article numbers unchanged."
        response_format = "መልስ:\n(በቀረበው የሕግ ማስረጃ ላይ ተመስርቶ የተሰጠ ማብራሪያ)"
    else:
        language_instruction = "Answer ONLY in English language. If the retrieved legal text is written in Amharic, translate the explanation into English. Keep article numbers unchanged."
        response_format = "Answer:\n(Legal explanation based only on retrieved evidence)"

    prompt = f"""
You are an Ethiopian Legal Information Assistant.

Your task is to answer legal questions using ONLY the retrieved legal context provided below.

LANGUAGE REQUIREMENT:
{language_instruction}

STRICT LEGAL RAG RULES:
1. Use ONLY information from the retrieved legal context.
2. Do NOT use external knowledge.
3. Do NOT invent laws, articles, sections, penalties, dates, or legal procedures.
4. Do NOT write "Relevant Sources" or "Important Note". The system will add them automatically.
5. If the retrieved context does not contain enough information to answer the question, respond exactly:
"The answer is not available in the retrieved legal documents."
6. Provide only general legal information.

RESPONSE FORMAT:
{response_format}

RETRIEVED LEGAL CONTEXT:
{legal_context}

USER QUESTION:
{question}

Generate only the final answer explanation.
"""
    return prompt