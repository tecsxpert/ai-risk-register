const PERIODS = [
  { label: "4 Weeks", value: "4w" },
  { label: "3 Months", value: "3m" },
  { label: "6 Months", value: "6m" },
  { label: "All Time", value: "all" },
];

const PeriodSelector = ({ selected, onChange }) => {
  return (
    <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
      {PERIODS.map((p) => (
        <button
          key={p.value}
          onClick={() => onChange(p.value)}
          className={`px-3 py-1.5 rounded-md text-xs font-medium transition ${
            selected === p.value
              ? "bg-white text-blue-900 shadow font-semibold"
              : "text-gray-500 hover:text-gray-700"
          }`}
        >
          {p.label}
        </button>
      ))}
    </div>
  );
};

export default PeriodSelector;