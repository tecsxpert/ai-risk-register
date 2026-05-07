const ChartCard = ({ title, subtitle, children, action }) => {
  return (
    <div className="bg-white rounded-xl shadow p-5 flex flex-col">
      <div className="flex items-start justify-between mb-1">
        <div>
          <h2 className="text-sm font-bold text-gray-800">{title}</h2>
          {subtitle && (
            <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>
          )}
        </div>
        {action && <div className="ml-2">{action}</div>}
      </div>
      <div className="flex-1 mt-4">{children}</div>
    </div>
  );
};

export default ChartCard;