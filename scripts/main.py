from chatbot import chat


print("Ethiopian Legal Assistant Chatbot")
print("Type exit to quit")


while True:

    question = input("\nAsk legal question: ")

    if question.lower() == "exit":
        break

    answer = chat(question)

    print("\n")
    print(answer)