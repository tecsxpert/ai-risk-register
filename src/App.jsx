import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import RiskListPage from "./pages/RiskListPage";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Navigate to="/risks" />} />
          <Route path="/risks" element={<RiskListPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;