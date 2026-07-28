from rag_pipeline import generate_legal_answer


print("Ethiopian Legal RAG Assistant")
print("የኢትዮጵያ የሕግ RAG ረዳት")


print("Type 'exit' to quit")
print("ለመውጣት 'exit' ይጻፉ")



while True:


    question = input(
        "\nAsk a legal question | የሕግ ጥያቄ ይጠይቁ: "
    )


    if question.lower() == "exit":

        print(
            "Goodbye! | ደህና ሁኑ!"
        )

        break



    response = generate_legal_answer(
        question
    )



    print(
        "\n=============================="
    )


    print(
        "Answer | መልስ:"
    )


    print(
        response["answer"]
    )



    print(
        "\nRelevant Sources | ተዛማጅ ምንጮች:"
    )


    for source in response["sources"]:

        print(
            source
        )



    print(
        "\nImportant Note | ማስታወሻ:"
    )


    print(
        response["important_note"]
    )


    print(
        "\n=============================="
    )