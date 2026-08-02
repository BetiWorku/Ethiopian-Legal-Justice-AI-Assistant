function TopNavbar() {
  return (
    <header className="bg-white shadow-sm px-8 py-4 flex items-center justify-between">

      {/* Search Box */}
      <div className="w-1/2">
        <input
          type="text"
          placeholder="Search documents, chunks, cases..."
          className="
            w-full
            border
            border-gray-300
            rounded-xl
            px-5
            py-3
            outline-none
            focus:ring-2
            focus:ring-green-600
          "
        />
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-5">

        {/* Notification */}
        <button className="text-2xl hover:scale-110 transition">
          🔔
        </button>

        {/* Status */}
        <div className="bg-green-100 text-green-700 px-4 py-2 rounded-full font-medium">
          🟢 Qdrant Online
        </div>

      </div>

    </header>
  );
}

export default TopNavbar;