const ConfirmModal = ({ message, onConfirm, onCancel, title = "Confirm Action", confirmLabel = "Yes, Delete", confirmVariant = "danger" }) => {
  const confirmStyles = {
    danger: "bg-red-500 hover:bg-red-600 text-white",
    primary: "bg-[#1B4F8A] hover:bg-[#163d6e] text-white",
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-modal w-full max-w-sm animate-slideUp">

        {/* Icon */}
        <div className="flex flex-col items-center pt-8 pb-4 px-6">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
            <span className="text-3xl">🗑️</span>
          </div>
          <h2 className="text-lg font-bold text-gray-800 text-center mb-2">
            {title}
          </h2>
          <p className="text-gray-500 text-sm text-center leading-relaxed">
            {message}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3 px-6 pb-6 pt-2">
          <button
            onClick={onCancel}
            className="flex-1 min-h-[44px] border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition font-semibold text-sm"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className={`flex-1 min-h-[44px] rounded-xl font-semibold text-sm transition active:scale-95 ${
              confirmStyles[confirmVariant] || confirmStyles.danger
            }`}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;