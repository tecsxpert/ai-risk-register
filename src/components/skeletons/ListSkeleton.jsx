const ListSkeleton = () => {
  return (
    <div className="p-6 max-w-7xl mx-auto animate-pulse">

      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <div className="h-7 bg-gray-200 rounded w-36 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-44"></div>
        </div>
        <div className="flex gap-3">
          <div className="h-9 bg-gray-200 rounded-lg w-24"></div>
          <div className="h-9 bg-gray-200 rounded-lg w-24"></div>
        </div>
      </div>

      {/* Search bar */}
      <div className="bg-white rounded-xl shadow p-4 mb-4">
        <div className="h-9 bg-gray-200 rounded-lg w-full"></div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow overflow-hidden">
        {/* Table header */}
        <div className="bg-gray-200 px-4 py-3 flex gap-4">
          {[2, 1, 1, 1, 0.5, 1, 1, 0.5].map((w, i) => (
            <div
              key={i}
              className="h-4 bg-gray-300 rounded"
              style={{ flex: w }}
            />
          ))}
        </div>
        {/* Table rows */}
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="flex gap-4 px-4 py-3 border-b border-gray-100"
          >
            {[2, 1, 1, 1, 0.5, 1, 1, 0.5].map((w, j) => (
              <div
                key={j}
                className="h-4 bg-gray-200 rounded"
                style={{ flex: w }}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ListSkeleton;