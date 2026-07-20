from chatbot import chatbot


def main():

    print("Ethiopian Legal AI Assistant")
    print("----------------------------")


    while True:

        question = input(
            "\nAsk your legal question: "
        )


        if question.lower() == "exit":
            break


        response = chatbot(question)


        print("\n")
        print(response)



if __name__ == "__main__":
    main()