const VARIANTS = {
  primary: "bg-[#1B4F8A] hover:bg-[#163d6e] text-white shadow-sm hover:shadow-brand",
  secondary: "border border-gray-300 text-gray-700 hover:bg-gray-50 bg-white",
  danger: "bg-red-500 hover:bg-red-600 text-white",
  ghost: "text-[#1B4F8A] hover:bg-blue-50",
  purple: "bg-purple-700 hover:bg-purple-800 text-white",
  success: "bg-green-600 hover:bg-green-700 text-white",
};

const SIZES = {
  sm: "px-3 text-xs min-h-[36px]",
  md: "px-4 text-sm min-h-[44px]",
  lg: "px-6 text-base min-h-[48px]",
};

const Button = ({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  onClick,
  type = "button",
  className = "",
  fullWidth = false,
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2
        font-semibold rounded-lg transition-all duration-200
        active:scale-95 select-none
        disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100
        ${VARIANTS[variant] || VARIANTS.primary}
        ${SIZES[size] || SIZES.md}
        ${fullWidth ? "w-full" : ""}
        ${className}
      `}
    >
      {loading && (
        <svg
          className="animate-spin h-4 w-4 flex-shrink-0"
          viewBox="0 0 24 24"
          fill="none"
        >
          <circle
            className="opacity-25"
            cx="12" cy="12" r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v8z"
          />
        </svg>
      )}
      {children}
    </button>
  );
};

export default Button;