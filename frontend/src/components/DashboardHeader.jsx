function DashboardHeader({ onRefresh, onUpload }) {
  return (
    <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">

      {/* Left Side */}
      <div>
        <h1 className="text-4xl font-bold text-slate-900">
          Admin Dashboard
        </h1>

        <p className="text-gray-500 mt-2">
          Manage the Ethiopian Legal AI Retrieval-Augmented Generation System.
        </p>
      </div>

      {/* Right Side */}
      <div className="flex gap-4 mt-6 md:mt-0">

        <button
          onClick={onRefresh}
          className="
            px-5
            py-3
            bg-white
            border
            border-gray-300
            rounded-xl
            shadow-sm
            hover:bg-gray-100
            transition
          "
        >
          🔄 Refresh
        </button>

        <button
          onClick={onUpload}
          className="
            px-5
            py-3
            bg-green-700
            text-white
            rounded-xl
            hover:bg-green-800
            transition
          "
        >
          ⬆ Upload PDF
        </button>

      </div>

    </div>
  );
}

export default DashboardHeader;