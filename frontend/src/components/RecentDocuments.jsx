function RecentDocuments() {
  const documents = [
    {
      id: 1,
      name: "FDRE Constitution.pdf",
      date: "2026-08-02",
      status: "Processed",
    },
    {
      id: 2,
      name: "Civil Code.pdf",
      date: "2026-08-01",
      status: "Pending",
    },
    {
      id: 3,
      name: "Criminal Code.pdf",
      date: "2026-07-30",
      status: "Processed",
    },
  ];

  return (
    <div className="bg-white rounded-2xl shadow-md p-6">

      <div className="flex justify-between items-center mb-6">

        <h2 className="text-2xl font-bold text-slate-800">
          Recent Documents
        </h2>

        <button className="text-green-700 font-semibold hover:underline">
          View All
        </button>

      </div>

      <div className="overflow-x-auto">

        <table className="w-full">

          <thead>

            <tr className="border-b text-left">

              <th className="py-3">Document</th>

              <th className="py-3">Upload Date</th>

              <th className="py-3">Status</th>

              <th className="py-3">Action</th>

            </tr>

          </thead>

          <tbody>

            {documents.map((doc) => (

              <tr
                key={doc.id}
                className="border-b hover:bg-gray-50"
              >

                <td className="py-4">
                  📄 {doc.name}
                </td>

                <td>{doc.date}</td>

                <td>

                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      doc.status === "Processed"
                        ? "bg-green-100 text-green-700"
                        : "bg-yellow-100 text-yellow-700"
                    }`}
                  >
                    {doc.status}
                  </span>

                </td>

                <td>

                  <button className="text-blue-600 hover:underline mr-4">
                    View
                  </button>

                  <button className="text-red-600 hover:underline">
                    Delete
                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default RecentDocuments;