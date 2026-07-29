import { useState, useEffect } from "react";

function App() {
  const [question, setQuestion] = useState("");
  // Load chats from Local Storage immediately when the app starts
  const [chats, setChats] = useState(() => {
    const savedChats = localStorage.getItem("legalAiChats");
    return savedChats ? JSON.parse(savedChats) : [];
  });
  const [currentChatId, setCurrentChatId] = useState(null);
  const [loading, setLoading] = useState(false);

  // Save chats to Local Storage whenever chats change
  useEffect(() => {
    localStorage.setItem("legalAiChats", JSON.stringify(chats));
  }, [chats]);

  const currentChat = chats.find((c) => c.id === currentChatId);
  const messages = currentChat ? currentChat.messages : [];

  const startNewChat = () => {
    setCurrentChatId(null);
    setQuestion("");
  };

  const selectChat = (id) => {
    setCurrentChatId(id);
  };

  // NEW: Delete a specific chat
  const deleteChat = (e, chatId) => {
    e.stopPropagation(); // Prevent selecting the chat when clicking delete
    setChats((prev) => prev.filter((c) => c.id !== chatId));
    if (currentChatId === chatId) {
      setCurrentChatId(null); // Go back to new chat screen if we deleted the active one
    }
  };

  const sendMessage = async (customQuestion = null) => {
    const currentQuestion = customQuestion || question;
    if (!currentQuestion.trim() || loading) return;

    let chatId = currentChatId;

    // If no active chat, create a new one
    if (!chatId) {
      chatId = Date.now();
      setChats((prev) => [
        { id: chatId, title: currentQuestion.substring(0, 30) + "...", messages: [] },
        ...prev,
      ]);
      setCurrentChatId(chatId);
    }

    // 1. Add User Message to the specific chat
    setChats((prev) =>
      prev.map((c) =>
        c.id === chatId
          ? { ...c, messages: [...c.messages, { role: "user", content: currentQuestion }] }
          : c
      )
    );

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: currentQuestion }),
      });

      const data = await response.json();
      const answerText = data?.result?.answer || "Error: Could not get response from server.";

      // 2. Add Assistant Message to the specific chat
      setChats((prev) =>
        prev.map((c) =>
          c.id === chatId
            ? { ...c, messages: [...c.messages, { role: "assistant", content: answerText }] }
            : c
        )
      );
    } catch (error) {
      setChats((prev) =>
        prev.map((c) =>
          c.id === chatId
            ? { ...c, messages: [...c.messages, { role: "assistant", content: "Connection error." }] }
            : c
        )
      );
    }

    setLoading(false);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      alert(`Selected file: ${file.name}\n(File upload backend integration is not implemented yet.)`);
    }
  };

  return (
    <div className="flex h-screen bg-slate-100 font-sans">
      
      {/* Left Sidebar (Chat History) - Deep Slate/Blue Theme */}
      <div className="hidden md:flex md:w-72 lg:w-80 flex-col bg-slate-900 text-white">
        
        <div className="p-3 border-b border-slate-700/50">
          <button 
            onClick={startNewChat}
            className="w-full flex items-center justify-center gap-2 p-3 border border-slate-600 rounded-lg hover:bg-slate-800 transition font-medium"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            New Chat
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
          {chats.length === 0 && (
            <p className="text-slate-500 text-sm text-center mt-10">No chat history</p>
          )}
          {chats.map((chat) => (
            <div
              key={chat.id}
              onClick={() => selectChat(chat.id)}
              className={`group w-full flex items-center justify-between p-3 rounded-lg transition cursor-pointer ${
                chat.id === currentChatId ? "bg-blue-600/90 shadow-lg" : "hover:bg-slate-800"
              }`}
            >
              <div className="flex items-center gap-3 overflow-hidden">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4 text-slate-300 flex-shrink-0">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <span className="truncate text-sm">{chat.title}</span>
              </div>

              {/* Delete Button (Visible on hover) */}
              <button 
                onClick={(e) => deleteChat(e, chat.id)}
                className="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-400 transition p-1 rounded"
                title="Delete chat"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3" />
                </svg>
              </button>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-slate-700/50">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-700 flex items-center justify-center text-white text-sm shadow">⚖️</div>
            <span className="font-bold text-sm">Ethiopian Legal AI</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Provides general legal info based on FDRE Constitution.
          </p>
        </div>
      </div>

      {/* Right Chat Interface */}
      <div className="flex-1 flex flex-col bg-white">
        
        {/* Mobile Header */}
        <div className="md:hidden flex items-center justify-between gap-2 p-4 border-b border-slate-200 bg-white">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white text-xl">⚖️</div>
            <h1 className="font-bold text-slate-800">Legal Assistant</h1>
          </div>
          <button onClick={startNewChat} className="text-sm text-blue-600 font-medium">New</button>
        </div>

        {/* Chat Area */}
        <main className="flex-1 overflow-y-auto bg-gradient-to-b from-slate-50 to-slate-100">
          <div className="max-w-3xl mx-auto px-4 py-6">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-[70vh] text-center">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-800 flex items-center justify-center text-white text-4xl shadow-xl mb-6">
                  ⚖️
                </div>
                <h2 className="text-3xl font-bold text-slate-800 mb-3">How can I help you today?</h2>
                <p className="text-slate-500 mb-8 max-w-md">
                  Ask any question regarding the FDRE Constitution, human rights, and legal procedures.
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-lg">
                  <button
                    onClick={() => sendMessage("What does Article 25 say?")}
                    className="text-left p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-400 hover:shadow-md transition shadow-sm"
                  >
                    <p className="font-semibold text-slate-700">⚖️ Article 25</p>
                    <p className="text-xs text-slate-400 mt-1">Equality before the law</p>
                  </button>
                  <button
                    onClick={() => sendMessage("የግል ሕይወት መብት ምንድነው?")}
                    className="text-left p-4 bg-white rounded-xl border border-slate-200 hover:border-blue-400 hover:shadow-md transition shadow-sm"
                  >
                    <p className="font-semibold text-slate-700">🇪🇹 የግል ሕይወት መብት</p>
                    <p className="text-xs text-slate-400 mt-1">Right to privacy</p>
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-8">
                {messages.map((message, index) => (
                  <div key={index} className={`flex flex-col ${message.role === "user" ? "items-end" : "items-start"}`}>
                    
                    <div className={`flex items-center gap-2 mb-1.5 ${message.role === "user" ? "flex-row-reverse" : ""}`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm shadow-sm ${message.role === "user" ? "bg-slate-400" : "bg-blue-600"}`}>
                        {message.role === "user" ? "🧑" : "⚖️"}
                      </div>
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                        {message.role === "user" ? "You" : "Legal Assistant"}
                      </span>
                    </div>

                    <div className={`max-w-[90%] md:max-w-[80%] rounded-2xl px-5 py-4 text-sm md:text-base leading-relaxed whitespace-pre-wrap ${
                        message.role === "user" 
                        ? "bg-blue-600 text-white rounded-tr-sm shadow-md" 
                        : "bg-white border border-slate-100 text-slate-800 shadow-sm rounded-tl-sm"
                      }`}>
                      {message.content}
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex flex-col items-start">
                    <div className="flex items-center gap-2 mb-1.5">
                      <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm">⚖️</div>
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Legal Assistant</span>
                    </div>
                    <div className="bg-white border border-slate-100 rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm">
                      <div className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce"></span>
                        <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce delay-100"></span>
                        <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce delay-200"></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </main>

        {/* Input Area (Bottom) */}
        <footer className="bg-transparent pb-4 pt-2 px-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex items-end gap-2 bg-white border border-slate-300 rounded-2xl p-2 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition shadow-md">
              
              <label className="p-2 text-slate-400 hover:text-blue-600 cursor-pointer rounded-lg hover:bg-slate-100 transition" title="Upload Document">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
                <input type="file" className="hidden" onChange={handleFileUpload} />
              </label>

              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                placeholder="Ask a legal question... | የሕግ ጥያቄ ይጠይቁ..."
                rows="1"
                className="flex-1 bg-transparent px-2 py-2 outline-none text-slate-700 resize-none max-h-40"
              />
              <button
                onClick={() => sendMessage()}
                disabled={loading || !question.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white p-3 rounded-xl transition shadow-sm"
                aria-label="Send"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                  <path d="M3.4 20.4l17.45-7.48a1 1 0 000-1.84L3.4 3.6a.993.993 0 00-1.39.91L2 9.12c0 .5.37.93.87.99L17 12 2.87 13.88c-.5.07-.87.5-.87 1l.01 4.61c0 .71.73 1.2 1.39.91z" />
                </svg>
              </button>
            </div>
            <p className="text-[10px] text-center text-slate-400 mt-2">
              Press Enter to send. AI may produce inaccurate information.
            </p>
          </div>
        </footer>
        
      </div>
    </div>
  );
}

export default App;