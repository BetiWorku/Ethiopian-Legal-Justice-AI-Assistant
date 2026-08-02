function StatCard({ title, value, icon, color }) {
  return (
    <div
      className="
        bg-white
        rounded-2xl
        shadow-md
        p-6
        hover:shadow-xl
        transition
        duration-300
      "
    >
      <div className="flex items-center justify-between">

        {/* Left Side */}
        <div>
          <p className="text-gray-500 text-sm font-medium">
            {title}
          </p>

          <h2 className="text-4xl font-bold text-slate-900 mt-3">
            {value}
          </h2>
        </div>

        {/* Right Side Icon */}
        <div
          className={`
            w-14
            h-14
            rounded-full
            flex
            items-center
            justify-center
            text-2xl
            ${color}
          `}
        >
          {icon}
        </div>

      </div>
    </div>
  );
}

export default StatCard;