import { useState, useEffect, createContext, useContext, useCallback } from "react";

const ToastContext = createContext(null);

const TOAST_TYPES = {
  success: { bg: "bg-green-500", icon: "✅" },
  error: { bg: "bg-red-500", icon: "❌" },
  info: { bg: "bg-blue-900", icon: "ℹ️" },
  warning: { bg: "bg-yellow-500", icon: "⚠️" },
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "info", duration = 3000) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, duration);
  }, []);

  const removeToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}

      {/* Toast Container */}
      <div className="fixed top-5 right-5 z-[100] flex flex-col gap-2 pointer-events-none">
        {toasts.map((toast) => {
          const config = TOAST_TYPES[toast.type] || TOAST_TYPES.info;
          return (
            <div
              key={toast.id}
              className={`${config.bg} text-white px-4 py-3 rounded-xl shadow-lg flex items-center gap-3 min-w-64 max-w-sm pointer-events-auto animate-pulse`}
              style={{ animation: "slideIn 0.3s ease-out" }}
            >
              <span className="text-lg flex-shrink-0">{config.icon}</span>
              <p className="text-sm font-medium flex-1">{toast.message}</p>
              <button
                onClick={() => removeToast(toast.id)}
                className="text-white opacity-70 hover:opacity-100 flex-shrink-0 text-lg leading-none"
              >
                ✕
              </button>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) throw new Error("useToast must be used inside ToastProvider");
  return context;
};

export default ToastProvider;