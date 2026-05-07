const VARIANTS = {
  default: "bg-white rounded-xl border border-gray-100 shadow-card",
  hover: "bg-white rounded-xl border border-gray-100 shadow-card hover:shadow-card-hover hover:border-blue-100 transition-all duration-200 cursor-pointer",
  flat: "bg-white rounded-xl border border-gray-100",
  colored: "rounded-xl border",
};

const Card = ({
  children,
  variant = "default",
  className = "",
  onClick,
  padding = "p-5",
}) => {
  return (
    <div
      onClick={onClick}
      className={`${VARIANTS[variant] || VARIANTS.default} ${padding} ${className}`}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({ title, subtitle, action }) => (
  <div className="flex items-start justify-between mb-4">
    <div>
      <h2 className="text-sm font-bold text-gray-800">{title}</h2>
      {subtitle && (
        <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>
      )}
    </div>
    {action && <div className="ml-3 flex-shrink-0">{action}</div>}
  </div>
);

export const CardDivider = () => (
  <hr className="border-gray-100 my-4" />
);

export default Card;