const DetailPageSkeleton = () => {
  return (
    <div className="p-6 max-w-4xl mx-auto animate-pulse">

      {/* Back button */}
      <div className="h-4 bg-gray-200 rounded w-28 mb-6"></div>

      {/* Header card */}
      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="flex justify-between">
          <div className="flex flex-col gap-3 flex-1 mr-4">
            <div className="h-7 bg-gray-200 rounded w-3/4"></div>
            <div className="flex gap-2">
              <div className="h-6 bg-gray-200 rounded-full w-20"></div>
              <div className="h-6 bg-gray-200 rounded-full w-20"></div>
              <div className="h-6 bg-gray-200 rounded-full w-24"></div>
            </div>
          </div>
          <div className="flex gap-2">
            <div className="h-9 bg-gray-200 rounded-lg w-16"></div>
            <div className="h-9 bg-gray-200 rounded-lg w-16"></div>
          </div>
        </div>
      </div>

      {/* Score card */}
      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="h-4 bg-gray-200 rounded w-24 mb-4"></div>
        <div className="flex justify-between mb-2">
          <div className="h-8 bg-gray-200 rounded w-16"></div>
          <div className="h-6 bg-gray-200 rounded-full w-24"></div>
        </div>
        <div className="h-3 bg-gray-200 rounded-full w-full mb-2"></div>
        <div className="flex justify-between">
          <div className="h-3 bg-gray-200 rounded w-4"></div>
          <div className="h-3 bg-gray-200 rounded w-4"></div>
          <div className="h-3 bg-gray-200 rounded w-6"></div>
        </div>
      </div>

      {/* Details grid */}
      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="h-4 bg-gray-200 rounded w-28 mb-5"></div>
        <div className="grid grid-cols-2 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="flex flex-col gap-2">
              <div className="h-3 bg-gray-200 rounded w-20"></div>
              <div className="h-5 bg-gray-200 rounded w-36"></div>
            </div>
          ))}
        </div>
        <div className="mt-6 pt-6 border-t border-gray-100">
          <div className="h-3 bg-gray-200 rounded w-24 mb-3"></div>
          <div className="flex flex-col gap-2">
            <div className="h-4 bg-gray-200 rounded w-full"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>

      {/* AI card */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="h-5 bg-gray-200 rounded w-28"></div>
          <div className="h-5 bg-gray-200 rounded-full w-40"></div>
        </div>
        <div className="flex flex-col items-center py-6 gap-3">
          <div className="h-12 w-12 bg-gray-200 rounded-full"></div>
          <div className="h-4 bg-gray-200 rounded w-64"></div>
          <div className="h-9 bg-gray-200 rounded-lg w-36"></div>
        </div>
      </div>
    </div>
  );
};

export default DetailPageSkeleton;