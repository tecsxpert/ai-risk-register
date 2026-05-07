const ScoreMeter = ({ score }) => {
  const getConfig = () => {
    if (score >= 70) return {
      barColor: "bg-red-500",
      textColor: "text-red-600",
      bgColor: "bg-red-50 border-red-100",
      label: "High Risk",
      emoji: "🔴",
    };
    if (score >= 50) return {
      barColor: "bg-yellow-500",
      textColor: "text-yellow-600",
      bgColor: "bg-yellow-50 border-yellow-100",
      label: "Medium Risk",
      emoji: "🟡",
    };
    return {
      barColor: "bg-green-500",
      textColor: "text-green-600",
      bgColor: "bg-green-50 border-green-100",
      label: "Low Risk",
      emoji: "🟢",
    };
  };

  const config = getConfig();

  return (
    <div className="flex flex-col gap-3">

      {/* Score number and label */}
      <div className="flex items-center justify-between">
        <div className="flex items-baseline gap-2">
          <span className={`text-4xl font-extrabold ${config.textColor}`}>
            {score}
          </span>
          <span className="text-gray-400 text-sm font-medium">/ 100</span>
        </div>
        <span className={`text-sm font-semibold px-3 py-1.5 rounded-full border ${config.bgColor} ${config.textColor}`}>
          {config.emoji} {config.label}
        </span>
      </div>

      {/* Progress bar track */}
      <div className="relative w-full bg-gray-100 rounded-full h-4 overflow-hidden">
        {/* Score zones */}
        <div className="absolute inset-0 flex">
          <div className="flex-1 bg-green-100 opacity-40" style={{ width: "50%" }} />
          <div className="flex-1 bg-yellow-100 opacity-40" style={{ width: "20%" }} />
          <div className="flex-1 bg-red-100 opacity-40" style={{ width: "30%" }} />
        </div>
        {/* Score fill */}
        <div
          className={`absolute top-0 left-0 h-full rounded-full transition-all duration-700 ${config.barColor}`}
          style={{ width: `${score}%` }}
        />
      </div>

      {/* Scale labels */}
      <div className="flex justify-between text-xs text-gray-400 font-medium px-1">
        <span>0 — Low</span>
        <span>50 — Medium</span>
        <span>70+ — High</span>
        <span>100</span>
      </div>
    </div>
  );
};

export default ScoreMeter;