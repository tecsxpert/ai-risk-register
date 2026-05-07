const PRIORITY_MAP = {
  High: {
    bg: "bg-red-500",
    text: "text-white",
    label: "🔴 High",
  },
  Medium: {
    bg: "bg-yellow-500",
    text: "text-white",
    label: "🟡 Medium",
  },
  Low: {
    bg: "bg-green-500",
    text: "text-white",
    label: "🟢 Low",
  },
};

const PriorityBadge = ({ priority }) => {
  const config = PRIORITY_MAP[priority] || {
    bg: "bg-gray-400",
    text: "text-white",
    label: priority,
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${config.bg} ${config.text}`}
    >
      {config.label}
    </span>
  );
};

export default PriorityBadge;