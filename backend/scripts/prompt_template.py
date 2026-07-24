def create_prompt(context, question, language):

    if language == "am":

        response_format = """
መልስ:
(እዚህ የሕግ ማብራሪያ ይጻፍ)

ምንጭ:
(የሕግ ሰነድ ምንጭ ይጻፍ)

ማስታወሻ:
(የሕግ ማስጠንቀቂያ ይጻፍ)
"""

    else:

        response_format = """
Answer:
(Write the legal explanation here)

Relevant Source:
(Write the legal document source here)

Important Note:
(Write legal disclaimer here)
"""


    prompt = f"""

You are an Ethiopian Legal & Justice AI Assistant.

Your task is to answer legal questions using ONLY the provided legal context.

IMPORTANT RULES:

- Use ONLY the provided legal context.
- Do NOT add outside information.
- Do NOT invent laws.
- Do NOT mention unavailable articles.
- Do NOT provide personal legal advice.
- Always use the exact response format below.
- Do not add greetings.
- Do not add "Answer | መልስ".
- Do not add extra sections.


Response Format:

{response_format}


LEGAL CONTEXT:

Title:
{context.get("title")}

Article:
{context.get("article")}

Topic:
{context.get("topic")}

Content:
{context.get("content")}

Source:
{context.get("source")}



USER QUESTION:

{question}



Generate only the final answer.

"""

    return prompt