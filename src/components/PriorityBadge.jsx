const priorityStyles = {
  High: "bg-red-500 text-white",
  Medium: "bg-yellow-500 text-white",
  Low: "bg-green-500 text-white",
};

const PriorityBadge = ({ priority }) => {
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${priorityStyles[priority] || "bg-gray-300 text-gray-700"}`}>
      {priority}
    </span>
  );
};

export default PriorityBadge;