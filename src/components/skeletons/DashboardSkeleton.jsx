const DashboardSkeleton = () => {
  return (
    <div className="p-6 max-w-7xl mx-auto animate-pulse">

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <div className="h-7 bg-gray-200 rounded w-32 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-48"></div>
        </div>
        <div className="h-9 bg-gray-200 rounded-lg w-32"></div>
      </div>

      {/* KPI Cards Row 1 */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl shadow p-5 flex items-center gap-4">
            <div className="w-14 h-14 bg-gray-200 rounded-xl"></div>
            <div className="flex flex-col gap-2 flex-1">
              <div className="h-7 bg-gray-200 rounded w-12"></div>
              <div className="h-4 bg-gray-200 rounded w-24"></div>
            </div>
          </div>
        ))}
      </div>

      {/* KPI Cards Row 2 */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl shadow p-5 flex items-center gap-4">
            <div className="w-14 h-14 bg-gray-200 rounded-xl"></div>
            <div className="flex flex-col gap-2 flex-1">
              <div className="h-7 bg-gray-200 rounded w-12"></div>
              <div className="h-4 bg-gray-200 rounded w-24"></div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl shadow p-5">
            <div className="h-5 bg-gray-200 rounded w-40 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-56 mb-4"></div>
            <div className="flex items-end gap-3 h-48">
              {[60, 90, 45, 75, 30, 55].map((h, j) => (
                <div
                  key={j}
                  className="bg-gray-200 rounded-t flex-1"
                  style={{ height: `${h}%` }}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DashboardSkeleton;