function SystemHealth() {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6">

      <h2 className="text-2xl font-bold text-slate-800 mb-6">
        System Health
      </h2>

      {/* Indexing Pipeline */}
      <div className="mb-6">
        <div className="flex justify-between mb-2">
          <span className="text-gray-600">Indexing Pipeline</span>
          <span className="font-semibold">92%</span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-green-600 h-3 rounded-full"
            style={{ width: "92%" }}
          ></div>
        </div>
      </div>

      {/* Vector Storage */}
      <div className="mb-6">
        <div className="flex justify-between mb-2">
          <span className="text-gray-600">Vector Storage</span>
          <span className="font-semibold">64%</span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-blue-600 h-3 rounded-full"
            style={{ width: "64%" }}
          ></div>
        </div>
      </div>

      {/* API Quota */}
      <div className="mb-6">
        <div className="flex justify-between mb-2">
          <span className="text-gray-600">API Quota</span>
          <span className="font-semibold">38%</span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-yellow-500 h-3 rounded-full"
            style={{ width: "38%" }}
          ></div>
        </div>
      </div>

      {/* Status */}
      <div className="mt-8 p-4 bg-green-50 rounded-xl border border-green-200">
        <p className="text-green-700 font-semibold">
          🟢 All Systems Operational
        </p>
      </div>

    </div>
  );
}

export default SystemHealth;