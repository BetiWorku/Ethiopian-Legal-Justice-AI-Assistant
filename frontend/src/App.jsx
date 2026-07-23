import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (customQuestion = null) => {
    const currentQuestion = customQuestion || question;

    if (!currentQuestion.trim() || loading) return;

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
        }),
      });

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Unable to connect to the legal assistant backend.",
        },
      ]);
    }

    setLoading(false);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="min-h-screen bg-slate-100">

      {/* Header */}
      <header className="border-b bg-white shadow-sm">

        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">

          <div className="flex items-center gap-3">

            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-2xl text-white">
              ⚖️
            </div>

            <div>
              <h1 className="text-xl font-bold text-slate-900">
                Ethiopian Legal Assistant
              </h1>

              <p className="text-sm text-slate-500">
                የኢትዮጵያ የሕግ ረዳት
              </p>
            </div>

          </div>

          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="rounded-lg border px-4 py-2 text-sm text-slate-600 hover:bg-slate-100"
            >
              🧹 Clear Chat
            </button>
          )}

        </div>

      </header>


      {/* Main */}
      <main className="mx-auto max-w-5xl px-6 pb-32">

        {messages.length === 0 ? (

          <div className="py-24 text-center">

            <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-blue-600 text-4xl text-white shadow-lg">
              ⚖️
            </div>

            <h2 className="text-4xl font-bold text-slate-900">
              How can I help you?
            </h2>

            <p className="mt-3 text-lg text-slate-600">
              Ask questions about Ethiopian law
            </p>

            <p className="text-lg text-slate-600">
              ስለ ኢትዮጵያ ሕግ ጥያቄዎን ይጠይቁ
            </p>


            {/* Suggestions */}
            <div className="mx-auto mt-10 grid max-w-3xl gap-4 md:grid-cols-2">

              <button
                onClick={() =>
                  sendMessage("What is Article 25?")
                }
                className="rounded-xl border bg-white p-5 text-left shadow-sm transition hover:border-blue-500 hover:shadow-md"
              >
                <p className="font-semibold text-slate-900">
                  ⚖️ What is Article 25?
                </p>

                <p className="mt-2 text-sm text-slate-500">
                  Learn about the right to equality
                </p>
              </button>


              <button
                onClick={() =>
                  sendMessage("የእኩልነት መብት ምንድነው?")
                }
                className="rounded-xl border bg-white p-5 text-left shadow-sm transition hover:border-blue-500 hover:shadow-md"
              >
                <p className="font-semibold text-slate-900">
                  🇪🇹 የእኩልነት መብት ምንድነው?
                </p>

                <p className="mt-2 text-sm text-slate-500">
                  ስለ እኩልነት መብት ይወቁ
                </p>
              </button>

            </div>

          </div>

        ) : (

          <div className="space-y-6 py-8">

            {messages.map((message, index) => (

              <div
                key={index}
                className={`flex ${
                  message.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >

                <div
                  className={`max-w-3xl rounded-2xl px-6 py-5 ${
                    message.role === "user"
                      ? "bg-blue-600 text-white"
                      : "border bg-white text-slate-800 shadow-sm"
                  }`}
                >

                  {message.role === "assistant" && (
                    <div className="mb-3 flex items-center gap-2 font-semibold text-blue-600">
                      ⚖️ Legal Assistant
                    </div>
                  )}

                  <div className="whitespace-pre-wrap leading-7">
                    {message.content}
                  </div>

                </div>

              </div>

            ))}


            {loading && (

              <div className="flex justify-start">

                <div className="rounded-2xl border bg-white px-6 py-4 text-slate-500 shadow-sm">

                  <span className="animate-pulse">
                    ⚖️ Thinking...
                  </span>

                </div>

              </div>

            )}

          </div>

        )}

      </main>


      {/* Input */}
      <div className="fixed bottom-0 left-0 right-0 border-t bg-white/95 p-4 backdrop-blur">

        <div className="mx-auto flex max-w-5xl gap-3">

          <input
            type="text"
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask a legal question... | የሕግ ጥያቄ ይጠይቁ..."
            className="flex-1 rounded-xl border border-slate-300 px-5 py-3 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          />

          <button
            onClick={() => sendMessage()}
            disabled={loading || !question.trim()}
            className="rounded-xl bg-blue-600 px-7 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "..." : "Send"}
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;