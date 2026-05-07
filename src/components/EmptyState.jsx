const EMPTY_CONFIGS = {
  noRisks: {
    icon: "📋",
    title: "No risks registered yet",
    subtitle: "Start by adding your first risk to the register.",
    actionLabel: "+ Add First Risk",
    actionPath: "/create",
  },
  noResults: {
    icon: "🔍",
    title: "No results found",
    subtitle: "Try adjusting your search terms or clearing your filters.",
    actionLabel: "Clear Filters",
    actionPath: null,
  },
  noData: {
    icon: "📊",
    title: "No data available",
    subtitle: "Data will appear here once risks are added to the register.",
    actionLabel: null,
    actionPath: null,
  },
  noReport: {
    icon: "📄",
    title: "No report generated yet",
    subtitle: "Click Generate Report to create an AI-powered executive summary.",
    actionLabel: null,
    actionPath: null,
  },
  error: {
    icon: "❌",
    title: "Failed to load data",
    subtitle: "Something went wrong while fetching data. Please try again.",
    actionLabel: "Retry",
    actionPath: null,
  },
  noAi: {
    icon: "🤖",
    title: "AI analysis not run yet",
    subtitle: "Click Analyse with AI to get insights on this risk.",
    actionLabel: null,
    actionPath: null,
  },
};

const EmptyState = ({
  type = "noData",
  title,
  subtitle,
  actionLabel,
  onAction,
  size = "md",
}) => {
  const config = EMPTY_CONFIGS[type] || EMPTY_CONFIGS.noData;

  const finalTitle = title || config.title;
  const finalSubtitle = subtitle || config.subtitle;
  const finalActionLabel = actionLabel || config.actionLabel;

  const sizeStyles = {
    sm: { wrapper: "py-8", icon: "text-4xl", title: "text-base", subtitle: "text-xs" },
    md: { wrapper: "py-12", icon: "text-5xl", title: "text-lg", subtitle: "text-sm" },
    lg: { wrapper: "py-16", icon: "text-6xl", title: "text-xl", subtitle: "text-sm" },
  };

  const s = sizeStyles[size] || sizeStyles.md;

  return (
    <div className={`flex flex-col items-center justify-center ${s.wrapper} px-4`}>

      {/* Illustration circle */}
      <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-5">
        <span className={s.icon}>{config.icon}</span>
      </div>

      {/* Text */}
      <h3 className={`${s.title} font-bold text-gray-700 mb-2 text-center`}>
        {finalTitle}
      </h3>
      <p className={`${s.subtitle} text-gray-400 text-center max-w-xs`}>
        {finalSubtitle}
      </p>

      {/* Action button */}
      {finalActionLabel && onAction && (
        <button
          onClick={onAction}
          className="mt-5 bg-blue-900 text-white px-5 py-2 rounded-lg hover:bg-blue-800 transition text-sm font-medium"
        >
          {finalActionLabel}
        </button>
      )}
    </div>
  );
};

export default EmptyState;