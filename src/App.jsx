import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ToastProvider } from "./components/Toast";
import ErrorBoundary from "./components/ErrorBoundary";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import RiskListPage from "./pages/RiskListPage";
import RiskFormPage from "./pages/RiskFormPage";
import DashboardPage from "./pages/DashboardPage";
import RiskDetailPage from "./pages/RiskDetailPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import AiPanel from "./components/AiPanel";

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <BrowserRouter>
          <div className="min-h-screen bg-gray-50">
            <Navbar />

            {/* Global Error Boundary wraps all routes */}
            <ErrorBoundary>
              <Routes>

                {/* Public */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />

                {/* Dashboard */}
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <ErrorBoundary>
                        <DashboardPage />
                      </ErrorBoundary>
                    </ProtectedRoute>
                  }
                />

                {/* Risk List */}
                <Route
                  path="/risks"
                  element={
                    <ProtectedRoute>
                      <ErrorBoundary>
                        <RiskListPage />
                      </ErrorBoundary>
                    </ProtectedRoute>
                  }
                />

                {/* Risk Detail */}
                <Route
                  path="/risks/:id"
                  element={
                    <ProtectedRoute>
                      <ErrorBoundary>
                        <RiskDetailPage />
                      </ErrorBoundary>
                    </ProtectedRoute>
                  }
                />

                {/* Create Risk */}
                <Route
                  path="/create"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN", "MANAGER"]}>
                      <ErrorBoundary>
                        <RiskFormPage />
                      </ErrorBoundary>
                    </ProtectedRoute>
                  }
                />

                {/* Edit Risk */}
                <Route
                  path="/risks/:id/edit"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN", "MANAGER"]}>
                      <ErrorBoundary>
                        <RiskFormPage />
                      </ErrorBoundary>
                    </ProtectedRoute>
                  }
                />

                {/* Analytics */}
                <Route
                  path="/analytics"
                  element={
                    <ProtectedRoute>
                      <ErrorBoundary>
                        <AnalyticsPage />
                      </ErrorBoundary>
                    </ProtectedRoute>
                  }
                />

                {/* 404 */}
                <Route
                  path="*"
                  element={
                    <div className="min-h-screen flex items-center justify-center">
                      <div className="text-center">
                        <p className="text-8xl mb-4 font-bold text-gray-200">
                          404
                        </p>
                        <h2 className="text-xl font-bold text-gray-800 mb-2">
                          Page Not Found
                        </h2>
                        <p className="text-gray-500 text-sm mb-6">
                          The page you are looking for does not exist.
                        </p>
                        <button
                          onClick={() => (window.location.href = "/dashboard")}
                          className="bg-blue-900 text-white px-5 py-2 rounded-lg hover:bg-blue-800 transition text-sm"
                        >
                          Go to Dashboard
                        </button>
                      </div>
                    </div>
                  }
                />
              </Routes>
            </ErrorBoundary>

            {/* Floating AI Panel */}
            <AiPanel />
          </div>
        </BrowserRouter>
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;