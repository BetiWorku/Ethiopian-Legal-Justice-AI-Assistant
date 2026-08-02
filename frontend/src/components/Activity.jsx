function Activity() {
  const activities = [
    {
      id: 1,
      icon: "📄",
      title: "FDRE Constitution.pdf uploaded",
      time: "2 minutes ago",
    },
    {
      id: 2,
      icon: "🧠",
      title: "Embeddings generated successfully",
      time: "10 minutes ago",
    },
    {
      id: 3,
      icon: "🗄️",
      title: "Qdrant collection updated",
      time: "25 minutes ago",
    },
    {
      id: 4,
      icon: "💬",
      title: "New chatbot query processed",
      time: "40 minutes ago",
    },
    {
      id: 5,
      icon: "✅",
      title: "Document processing completed",
      time: "1 hour ago",
    },
  ];

  return (
    <div className="bg-white rounded-2xl shadow-md p-6">

      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-slate-800">
          Recent Activity
        </h2>

        <button className="text-green-700 hover:underline">
          View All
        </button>
      </div>

      <div className="space-y-4">

        {activities.map((activity) => (

          <div
            key={activity.id}
            className="flex items-start gap-4 border-b pb-4 last:border-none"
          >

            <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-xl">
              {activity.icon}
            </div>

            <div className="flex-1">
              <p className="font-medium text-slate-800">
                {activity.title}
              </p>

              <p className="text-sm text-gray-500">
                {activity.time}
              </p>
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Activity;