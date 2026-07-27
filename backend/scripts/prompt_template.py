def create_prompt(context, question, language):


    # ==========================
    # Convert retrieved documents into text
    # ==========================

    legal_context = ""

    for doc in context:

        legal_context += f"""

Article:
{doc.get("article","Unknown")}

Title:
{doc.get("title","Unknown")}

Source:
{doc.get("source","Unknown")}

Content:
{doc.get("text","")}

----------------------

"""


    # ==========================
    # Language Control
    # ==========================

    if language == "am":

        language_instruction = """
Answer ONLY in Amharic language.
Use Amharic script.
Do not answer in English.
"""

        response_format = """
መልስ:

(የሕግ ማብራሪያ)

ምንጭ:

(የሕግ ሰነድ ምንጭ)

ማስታወሻ:

(የሕግ ማስጠንቀቂያ)
"""


    else:

        language_instruction = """
Answer ONLY in English language.
Do not use Amharic.
Even if the legal document is written in Amharic, translate the answer into English.
"""

        response_format = """
Answer:

(Legal explanation)

Relevant Source:

(Legal document source)

Important Note:

(Legal disclaimer)
"""



    # ==========================
    # Create Prompt
    # ==========================

    prompt = f"""

You are an Ethiopian Legal & Justice AI Assistant.

LANGUAGE REQUIREMENT:

{language_instruction}


IMPORTANT RULES:

- Use ONLY the provided legal context.
- Do NOT use outside knowledge.
- Do NOT invent laws.
- Do NOT create missing articles.
- Always mention the correct article number.
- Follow the response format exactly.
- Always include:
  Answer/መልስ
  Relevant Source/ምንጭ
  Important Note/ማስታወሻ
- Never remove section titles.



RESPONSE FORMAT:

{response_format}



LEGAL CONTEXT:

{legal_context}



USER QUESTION:

{question}



Generate only the final answer.

"""


    return prompt