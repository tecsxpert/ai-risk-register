const COLOR_MAP = {
  blue: {
    bg: "bg-[#1B4F8A]",
    light: "bg-blue-50 border border-blue-100",
    text: "text-[#1B4F8A]",
    subtitleBg: "bg-blue-100 text-blue-800",
  },
  red: {
    bg: "bg-red-500",
    light: "bg-red-50 border border-red-100",
    text: "text-red-600",
    subtitleBg: "bg-red-100 text-red-700",
  },
  yellow: {
    bg: "bg-yellow-500",
    light: "bg-yellow-50 border border-yellow-100",
    text: "text-yellow-600",
    subtitleBg: "bg-yellow-100 text-yellow-700",
  },
  green: {
    bg: "bg-green-500",
    light: "bg-green-50 border border-green-100",
    text: "text-green-600",
    subtitleBg: "bg-green-100 text-green-700",
  },
  purple: {
    bg: "bg-purple-600",
    light: "bg-purple-50 border border-purple-100",
    text: "text-purple-600",
    subtitleBg: "bg-purple-100 text-purple-700",
  },
};

const KpiCard = ({ title, value, subtitle, icon, color = "blue", trend }) => {
  const c = COLOR_MAP[color] || COLOR_MAP.blue;

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5 flex items-center gap-4 hover:shadow-md transition-shadow duration-200 animate-fadeIn">

      {/* Icon Box */}
      <div className={`w-14 h-14 rounded-xl flex items-center justify-center text-2xl flex-shrink-0 ${c.bg}`}>
        <span>{icon}</span>
      </div>

      {/* Content */}
      <div className="flex flex-col min-w-0">
        <span className={`text-3xl font-extrabold ${c.text} leading-tight`}>
          {value}
        </span>
        <span className="text-sm font-semibold text-gray-600 truncate">
          {title}
        </span>
        {subtitle && (
          <span className={`text-xs mt-1 px-2 py-0.5 rounded-full font-medium w-fit ${c.subtitleBg}`}>
            {subtitle}
          </span>
        )}
        {trend && (
          <span className={`text-xs mt-1 font-medium ${trend > 0 ? "text-red-500" : "text-green-500"}`}>
            {trend > 0 ? "↑" : "↓"} {Math.abs(trend)}% this month
          </span>
        )}
      </div>
    </div>
  );
};

export default KpiCard;