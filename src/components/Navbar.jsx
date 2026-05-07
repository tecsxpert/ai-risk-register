import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const roleBadgeStyles = {
  ADMIN: "bg-red-500",
  MANAGER: "bg-yellow-500",
  VIEWER: "bg-green-500",
};

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, isAuthenticated, logoutUser } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logoutUser();
    navigate("/login");
    setMenuOpen(false);
  };

  const navLinks = [
    { label: "🏠 Dashboard", path: "/dashboard" },
    { label: "📋 Risk List", path: "/risks" },
    { label: "📊 Analytics", path: "/analytics" },
  ];

  const isActive = (path) => location.pathname === path;

  const handleNavClick = (path) => {
    navigate(path);
    setMenuOpen(false);
  };

  return (
    <nav className="bg-blue-900 text-white shadow relative z-40">
      <div className="px-4 sm:px-6 py-3 flex justify-between items-center">

        {/* Left — Logo */}
        <div
          className="flex items-center gap-2 cursor-pointer flex-shrink-0"
          onClick={() => navigate("/dashboard")}
        >
          <span className="text-xl">🛡️</span>
          <span className="font-bold text-base sm:text-lg tracking-tight">
            AI Risk Register
          </span>
        </div>

        {/* Centre — Nav Links — hidden on mobile */}
        {isAuthenticated && (
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <button
                key={link.path}
                onClick={() => handleNavClick(link.path)}
                className={`px-3 py-1.5 rounded-lg text-sm transition ${
                  isActive(link.path)
                    ? "bg-white text-blue-900 font-semibold"
                    : "text-blue-100 hover:bg-blue-800"
                }`}
              >
                {link.label}
              </button>
            ))}
          </div>
        )}

        {/* Right — User info — hidden on mobile */}
        {isAuthenticated && user && (
          <div className="hidden md:flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm">
              <div className="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center font-bold text-xs">
                {user.name?.charAt(0).toUpperCase()}
              </div>
              <div className="flex flex-col leading-tight">
                <span className="text-sm font-medium">{user.name}</span>
                <span className="text-xs text-blue-300">{user.email}</span>
              </div>
              <span
                className={`text-xs px-2 py-0.5 rounded-full text-white font-semibold ${
                  roleBadgeStyles[user.role] || "bg-gray-500"
                }`}
              >
                {user.role}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="text-sm bg-blue-800 hover:bg-red-600 px-3 py-1.5 rounded-lg transition"
            >
              Logout
            </button>
          </div>
        )}

        {/* Hamburger — mobile only */}
        {isAuthenticated && (
          <button
            onClick={() => setMenuOpen((prev) => !prev)}
            className="md:hidden flex flex-col gap-1.5 p-2 rounded-lg hover:bg-blue-800 transition"
            aria-label="Toggle menu"
          >
            <span className={`block w-5 h-0.5 bg-white transition-transform ${menuOpen ? "rotate-45 translate-y-2" : ""}`} />
            <span className={`block w-5 h-0.5 bg-white transition-opacity ${menuOpen ? "opacity-0" : ""}`} />
            <span className={`block w-5 h-0.5 bg-white transition-transform ${menuOpen ? "-rotate-45 -translate-y-2" : ""}`} />
          </button>
        )}
      </div>

      {/* Mobile Menu Dropdown */}
      {isAuthenticated && menuOpen && (
        <div className="md:hidden bg-blue-800 px-4 pb-4 flex flex-col gap-1 border-t border-blue-700">

          {/* Nav links */}
          {navLinks.map((link) => (
            <button
              key={link.path}
              onClick={() => handleNavClick(link.path)}
              className={`w-full text-left px-4 py-3 rounded-lg text-sm transition ${
                isActive(link.path)
                  ? "bg-white text-blue-900 font-semibold"
                  : "text-blue-100 hover:bg-blue-700"
              }`}
            >
              {link.label}
            </button>
          ))}

          {/* Divider */}
          <div className="border-t border-blue-700 my-2" />

          {/* User info */}
          {user && (
            <div className="flex items-center gap-3 px-4 py-2">
              <div className="w-9 h-9 rounded-full bg-blue-700 flex items-center justify-center font-bold text-sm">
                {user.name?.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="text-sm font-medium">{user.name}</p>
                <p className="text-xs text-blue-300">{user.email}</p>
              </div>
              <span
                className={`text-xs px-2 py-0.5 rounded-full text-white font-semibold ml-auto ${
                  roleBadgeStyles[user.role] || "bg-gray-500"
                }`}
              >
                {user.role}
              </span>
            </div>
          )}

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-3 rounded-lg text-sm text-red-300 hover:bg-blue-700 transition"
          >
            ⏻ Logout
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;