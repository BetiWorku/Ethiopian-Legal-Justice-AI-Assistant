from scripts.chatbot import chat

print("Ethiopian Legal Assistant Chatbot")
print("የኢትዮጵያ የሕግ ረዳት ቻትቦት")

print("Type 'exit' to quit")
print("ለመውጣት 'exit' ይጻፉ")


while True:

    question = input(
        "\nAsk a legal question | የሕግ ጥያቄ ይጠይቁ: "
    )

    if question.lower() == "exit":
        print("Goodbye! | ደህና ሁኑ!")
        break

    answer = chat(question)

    print("\nAnswer | መልስ:")
    print(answer)