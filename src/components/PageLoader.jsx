const PageLoader = ({ message = "Loading..." }) => {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center gap-4">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-blue-100 rounded-full"></div>
        <div className="w-16 h-16 border-4 border-blue-900 border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
      </div>
      <p className="text-gray-500 text-sm font-medium">{message}</p>
    </div>
  );
};

export default PageLoader;