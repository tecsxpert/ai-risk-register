import StatusBadge from "./StatusBadge";
import PriorityBadge from "./PriorityBadge";

const StatsSummaryTable = ({ risks }) => {
  if (!risks || risks.length === 0) {
    return (
      <p className="text-sm text-gray-400 text-center py-4">No data available</p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead>
          <tr className="border-b border-gray-100">
            <th className="text-left text-gray-400 font-semibold pb-2 uppercase tracking-wide">
              Title
            </th>
            <th className="text-left text-gray-400 font-semibold pb-2 uppercase tracking-wide">
              Status
            </th>
            <th className="text-left text-gray-400 font-semibold pb-2 uppercase tracking-wide">
              Priority
            </th>
            <th className="text-right text-gray-400 font-semibold pb-2 uppercase tracking-wide">
              Score
            </th>
          </tr>
        </thead>
        <tbody>
          {risks.map((risk, i) => (
            <tr key={i} className="border-b border-gray-50 hover:bg-gray-50">
              <td className="py-2 pr-3 text-gray-700 font-medium max-w-xs truncate">
                {risk.title}
              </td>
              <td className="py-2 pr-3">
                <StatusBadge status={risk.status} />
              </td>
              <td className="py-2 pr-3">
                <PriorityBadge priority={risk.priority} />
              </td>
              <td className="py-2 text-right">
                <span
                  className={`font-bold ${
                    risk.score >= 70
                      ? "text-red-600"
                      : risk.score >= 50
                      ? "text-yellow-600"
                      : "text-green-600"
                  }`}
                >
                  {risk.score}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StatsSummaryTable;