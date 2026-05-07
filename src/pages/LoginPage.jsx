import { useState } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { login } from "../services/authService";
import { useAuth } from "../context/AuthContext";

const LoginPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, loginUser } = useAuth();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [loginError, setLoginError] = useState("");

  if (isAuthenticated) return <Navigate to="/dashboard" replace />;

  const validate = () => {
    const errs = {};
    if (!formData.email.trim()) errs.email = "Email is required.";
    else if (!/\S+@\S+\.\S+/.test(formData.email))
      errs.email = "Enter a valid email.";
    if (!formData.password.trim()) errs.password = "Password is required.";
    else if (formData.password.length < 6)
      errs.password = "Password must be at least 6 characters.";
    return errs;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: "" }));
    setLoginError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    setLoading(true);
    try {
      const data = await login(formData.email, formData.password);
      loginUser(data.token, {
        email: formData.email,
        role: data.role,
        name: data.name,
      });
      navigate("/dashboard");
    } catch (err) {
      setLoginError(err.message || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-white rounded-2xl mb-4 shadow-lg">
            <span className="text-3xl sm:text-4xl">🛡️</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white">
            AI Risk Register
          </h1>
          <p className="text-blue-200 text-sm mt-1">
            Sign in to your account
          </p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 sm:p-8">

          {/* Error Banner */}
          {loginError && (
            <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 text-sm mb-5">
              {loginError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">

            {/* Email */}
            <div className="flex flex-col gap-1">
              <label className="text-sm font-semibold text-gray-700">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="you@example.com"
                className={`border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.email
                    ? "border-red-500 bg-red-50"
                    : "border-gray-300"
                }`}
              />
              {errors.email && (
                <p className="text-red-500 text-xs">{errors.email}</p>
              )}
            </div>

            {/* Password */}
            <div className="flex flex-col gap-1">
              <label className="text-sm font-semibold text-gray-700">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className={`border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.password
                    ? "border-red-500 bg-red-50"
                    : "border-gray-300"
                }`}
              />
              {errors.password && (
                <p className="text-red-500 text-xs">{errors.password}</p>
              )}
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-900 text-white py-2.5 rounded-lg hover:bg-blue-800 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 mt-2 font-medium"
            >
              {loading && (
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                </svg>
              )}
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          {/* Demo credentials */}
          <div className="mt-6 p-3 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs font-semibold text-gray-500 mb-2">
              Demo Credentials:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-1 text-xs text-gray-600">
              <button
                onClick={() => setFormData({ email: "admin@risk.com", password: "admin123" })}
                className="text-left hover:text-blue-700 transition p-1 rounded hover:bg-blue-50"
              >
                👤 Admin
              </button>
              <button
                onClick={() => setFormData({ email: "manager@risk.com", password: "manager123" })}
                className="text-left hover:text-blue-700 transition p-1 rounded hover:bg-blue-50"
              >
                👤 Manager
              </button>
              <button
                onClick={() => setFormData({ email: "viewer@risk.com", password: "viewer123" })}
                className="text-left hover:text-blue-700 transition p-1 rounded hover:bg-blue-50"
              >
                👤 Viewer
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              Click a role above to auto-fill credentials
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;