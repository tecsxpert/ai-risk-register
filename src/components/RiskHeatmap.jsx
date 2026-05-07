const PRIORITIES = ["High", "Medium", "Low"];

const getColor = (value) => {
  if (value === 0) return "bg-gray-100 text-gray-300";
  if (value === 1) return "bg-yellow-200 text-yellow-800";
  if (value === 2) return "bg-orange-300 text-orange-900";
  return "bg-red-500 text-white";
};

const RiskHeatmap = ({ data }) => {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr>
            <th className="text-left text-xs text-gray-400 font-medium pb-3 pr-4">
              Category
            </th>
            {PRIORITIES.map((p) => (
              <th
                key={p}
                className="text-center text-xs font-semibold pb-3 px-3"
              >
                <span
                  className={`px-2 py-1 rounded-full text-xs ${
                    p === "High"
                      ? "bg-red-100 text-red-700"
                      : p === "Medium"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-green-100 text-green-700"
                  }`}
                >
                  {p}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-t border-gray-50">
              <td className="py-2 pr-4 text-xs font-medium text-gray-600">
                {row.category}
              </td>
              {PRIORITIES.map((p) => (
                <td key={p} className="py-2 px-3 text-center">
                  <div
                    className={`inline-flex items-center justify-center w-10 h-10 rounded-xl text-sm font-bold transition ${getColor(
                      row[p]
                    )}`}
                  >
                    {row[p]}
                  </div>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex items-center gap-3 mt-4 flex-wrap">
        <span className="text-xs text-gray-400 font-medium">Legend:</span>
        {[
          { label: "None", style: "bg-gray-100" },
          { label: "1 risk", style: "bg-yellow-200" },
          { label: "2 risks", style: "bg-orange-300" },
          { label: "3+ risks", style: "bg-red-500" },
        ].map((l, i) => (
          <div key={i} className="flex items-center gap-1.5">
            <div className={`w-4 h-4 rounded ${l.style}`} />
            <span className="text-xs text-gray-500">{l.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RiskHeatmap;