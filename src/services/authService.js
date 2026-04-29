import api from "./api";

const USE_MOCK = true; // Change to false when backend is ready

// Mock users for testing
const MOCK_USERS = [
  { email: "admin@risk.com", password: "admin123", role: "ADMIN", name: "Admin User" },
  { email: "manager@risk.com", password: "manager123", role: "MANAGER", name: "Manager User" },
  { email: "viewer@risk.com", password: "viewer123", role: "VIEWER", name: "Viewer User" },
];

// Login
export const login = async (email, password) => {
  if (USE_MOCK) {
    await new Promise((res) => setTimeout(res, 1000));
    const user = MOCK_USERS.find(
      (u) => u.email === email && u.password === password
    );
    if (!user) throw new Error("Invalid email or password.");

    // Fake JWT token structure
    const fakeToken = btoa(JSON.stringify({ email: user.email, role: user.role, name: user.name }));
    return { token: fakeToken, role: user.role, name: user.name };
  }

  // Real API call
  const response = await api.post("/auth/login", { email, password });
  return response.data;
};

// Logout
export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};

// Get current user from localStorage
export const getCurrentUser = () => {
  try {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  } catch {
    return null;
  }
};

// Check if token exists
export const isLoggedIn = () => {
  return Boolean(localStorage.getItem("token"));
};