import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const roleBadgeStyles = {
  ADMIN: "bg-red-500",
  MANAGER: "bg-yellow-500",
  VIEWER: "bg-green-500",
};

const Navbar = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logoutUser } = useAuth();

  const handleLogout = () => {
    logoutUser();
    navigate("/login");
  };

  return (
    <nav className="bg-blue-900 text-white px-6 py-3 flex justify-between items-center shadow">
      {/* Left — Logo */}
      <div
        className="flex items-center gap-2 cursor-pointer"
        onClick={() => navigate("/risks")}
      >
        <span className="text-xl">🛡️</span>
        <span className="font-bold text-lg">AI Risk Register</span>
      </div>

      {/* Right — User info and logout */}
      {isAuthenticated && user && (
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm">
            <span className="text-blue-200">👤</span>
            <span>{user.name}</span>
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
            className="text-sm bg-blue-800 hover:bg-blue-700 px-3 py-1.5 rounded-lg transition"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;