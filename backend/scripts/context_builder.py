def build_context(documents):
    """
    Convert retrieved legal documents into
    structured RAG context.
    """


    context = ""


    for index, doc in enumerate(documents, start=1):

        context += f"""

================================
Retrieved Legal Context {index}
================================


Document:
{doc.get("document", "FDRE Constitution")}


Chapter:
{doc.get("chapter", "Unknown")}


Article:
{doc.get("article", "Unknown")}


Article Title:
{doc.get("title", "Unknown")}


Pages:
{doc.get("pages", "Unknown")}


Source:
{doc.get("source", "FDRE Constitution")}


Similarity Score:
{doc.get("score", "Unknown")}


Legal Text:

{doc.get("text", "")}


"""


    return context