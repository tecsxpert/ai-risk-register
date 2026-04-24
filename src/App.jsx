import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import RiskListPage from "./pages/RiskListPage";
import RiskFormPage from "./pages/RiskFormPage";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<Navigate to="/risks" replace />} />

            {/* Protected routes */}
            <Route
              path="/risks"
              element={
                <ProtectedRoute>
                  <RiskListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/risks/:id"
              element={
                <ProtectedRoute>
                  {/* Detail page — coming Day 7 */}
                  <div className="p-6 text-gray-500">Detail page coming soon...</div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/create"
              element={
                <ProtectedRoute allowedRoles={["ADMIN", "MANAGER"]}>
                  <RiskFormPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/risks/:id/edit"
              element={
                <ProtectedRoute allowedRoles={["ADMIN", "MANAGER"]}>
                  <RiskFormPage />
                </ProtectedRoute>
              }
            />

            {/* 404 fallback */}
            <Route
              path="*"
              element={
                <div className="min-h-screen flex items-center justify-center">
                  <div className="text-center">
                    <p className="text-6xl mb-4">404</p>
                    <h2 className="text-xl font-bold text-gray-800 mb-2">Page Not Found</h2>
                    <button
                      onClick={() => window.location.href = "/risks"}
                      className="text-blue-600 hover:underline text-sm"
                    >
                      Go back home
                    </button>
                  </div>
                </div>
              }
            />
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;