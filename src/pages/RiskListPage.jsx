import { useEffect, useState, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getRisks, deleteRisk } from "../services/riskService";
import { useToast } from "../components/Toast";
import TableSkeleton from "../components/TableSkeleton";
import StatusBadge from "../components/StatusBadge";
import PriorityBadge from "../components/PriorityBadge";
import Pagination from "../components/Pagination";
import SortIcon from "../components/SortIcon";
import ConfirmModal from "../components/ConfirmModal";
import SearchFilterBar from "../components/SearchFilterBar";
import EmptyState from "../components/EmptyState";
import ExportButton from "../components/ExportButton";
import PageWrapper from "../components/PageWrapper";


const COLUMNS = [
  { label: "Title", key: "title" },
  { label: "Category", key: "category" },
  { label: "Status", key: "status" },
  { label: "Priority", key: "priority" },
  { label: "Score", key: "score" },
  { label: "Owner", key: "owner" },
  { label: "Created", key: "createdDate" },
];

const RiskListPage = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { addToast } = useToast();

  // Data state
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Pagination state
  const [currentPage, setCurrentPage] = useState(
    parseInt(searchParams.get("page") || "0")
  );
  const [totalPages, setTotalPages] = useState(0);
  const [totalElements, setTotalElements] = useState(0);
  const PAGE_SIZE = 10;

  // Sorting state
  const [sortBy, setSortBy] = useState(
    searchParams.get("sortBy") || "createdDate"
  );
  const [sortDir, setSortDir] = useState(
    searchParams.get("sortDir") || "desc"
  );

  // Filter state
  const [filters, setFilters] = useState({
    search: searchParams.get("search") || "",
    status: searchParams.get("status") || "All",
    priority: searchParams.get("priority") || "All",
    category: searchParams.get("category") || "All",
    startDate: searchParams.get("startDate")
      ? new Date(searchParams.get("startDate"))
      : null,
    endDate: searchParams.get("endDate")
      ? new Date(searchParams.get("endDate"))
      : null,
  });

  // Delete modal state
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Sync to URL
  useEffect(() => {
    const params = {};
    if (filters.search) params.search = filters.search;
    if (filters.status !== "All") params.status = filters.status;
    if (filters.priority !== "All") params.priority = filters.priority;
    if (filters.category !== "All") params.category = filters.category;
    if (filters.startDate)
      params.startDate = filters.startDate.toISOString().split("T")[0];
    if (filters.endDate)
      params.endDate = filters.endDate.toISOString().split("T")[0];
    if (currentPage > 0) params.page = currentPage;
    if (sortBy !== "createdDate") params.sortBy = sortBy;
    if (sortDir !== "desc") params.sortDir = sortDir;
    setSearchParams(params);
  }, [filters, currentPage, sortBy, sortDir]);

  // Fetch data
  const fetchRisks = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getRisks(
        currentPage,
        PAGE_SIZE,
        sortBy,
        sortDir,
        filters.search,
        filters.status,
        filters.priority,
        filters.category,
        filters.startDate,
        filters.endDate
      );
      setRisks(data.content);
      setTotalPages(data.totalPages);
      setTotalElements(data.totalElements);
    } catch (err) {
      setError("Failed to load risks. Please try again.");
      addToast("Failed to load risks.", "error");
    } finally {
      setLoading(false);
    }
  }, [currentPage, sortBy, sortDir, filters]);

  useEffect(() => {
    fetchRisks();
  }, [fetchRisks]);

  // Handle filter change
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setCurrentPage(0);
  };

  // Handle column sort
  const handleSort = (column) => {
    if (sortBy === column) {
      setSortDir((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortBy(column);
      setSortDir("asc");
    }
    setCurrentPage(0);
  };

  // Handle delete confirm
  const handleDeleteConfirm = async () => {
    setDeleteLoading(true);
    try {
      await deleteRisk(deleteTarget.id);
      setDeleteTarget(null);
      addToast("Risk deleted successfully!", "success");
      fetchRisks();
    } catch (err) {
      setError("Failed to delete risk.");
      addToast("Failed to delete risk.", "error");
      setDeleteTarget(null);
    } finally {
      setDeleteLoading(false);
    }
  };

  // Check if any filter is active
  const hasActiveFilters =
    filters.search ||
    filters.status !== "All" ||
    filters.priority !== "All" ||
    filters.category !== "All" ||
    filters.startDate ||
    filters.endDate;

  return (
    <PageWrapper>
    <div className="p-6 max-w-7xl mx-auto">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
  <div>
    <h1 className="text-xl sm:text-2xl font-bold text-gray-800">
      Risk Register
    </h1>
    <p className="text-gray-500 text-sm mt-1">
      {totalElements} total risks tracked
    </p>
  </div>
  <div className="flex items-center gap-3 self-start sm:self-auto">
    <ExportButton risks={risks} />
    <button
      onClick={() => navigate("/create")}
      className="bg-blue-900 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition text-sm whitespace-nowrap"
    >
      + Add Risk
    </button>
  </div>
</div>

      {/* Search and Filter Bar */}
      <SearchFilterBar
        onFilterChange={handleFilterChange}
        initialFilters={filters}
      />

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 text-sm mb-4 flex justify-between items-center">
          <span>{error}</span>
          <button
            onClick={fetchRisks}
            className="underline font-medium ml-4"
          >
            Retry
          </button>
        </div>
      )}

      {/* Table */}
      {/* Table */}
<div className="bg-white rounded-xl shadow overflow-hidden">
  
  {/* This div makes the table scroll sideways on mobile */}
  <div className="overflow-x-auto">
    <table className="w-full text-sm text-left" style={{ minWidth: "700px" }}>
      <thead className="bg-blue-900 text-white text-xs uppercase">
        <tr>
          {COLUMNS.map((col) => (
            <th
              key={col.key}
              onClick={() => handleSort(col.key)}
              className="px-4 py-3 cursor-pointer hover:bg-blue-800 select-none transition whitespace-nowrap"
            >
              {col.label}
              <SortIcon
                column={col.key}
                sortBy={sortBy}
                sortDir={sortDir}
              />
            </th>
          ))}
          <th className="px-4 py-3 whitespace-nowrap">Actions</th>
        </tr>
      </thead>
      <tbody>
        {loading ? (
          <tr>
            <td colSpan={8}>
              <TableSkeleton />
            </td>
          </tr>
        ) : risks.length === 0 ? (
          <tr>
            <td colSpan={8}>
              <EmptyState
                type={
                  filters.search ||
                  filters.status !== "All" ||
                  filters.priority !== "All" ||
                  filters.category !== "All"
                    ? "noResults"
                    : "noRisks"
                }
                onAction={
                  filters.search || filters.status !== "All"
                    ? () =>
                        handleFilterChange({
                          search: "",
                          status: "All",
                          priority: "All",
                          category: "All",
                          startDate: null,
                          endDate: null,
                        })
                    : () => navigate("/create")
                }
                size="md"
              />
            </td>
          </tr>
        ) : (
          risks.map((risk) => (
            <tr
              key={risk.id}
              className="border-b border-gray-100 hover:bg-blue-50 transition cursor-pointer"
              onClick={() => navigate(`/risks/${risk.id}`)}
            >
              <td className="px-4 py-3 font-medium text-gray-800 whitespace-nowrap max-w-[200px] truncate">
                {risk.title}
              </td>
              <td className="px-4 py-3 text-gray-600 whitespace-nowrap">
                {risk.category}
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <StatusBadge status={risk.status} />
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <PriorityBadge priority={risk.priority} />
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <span
                  className={`font-bold ${
                    risk.score >= 70
                      ? "text-red-600"
                      : risk.score >= 50
                      ? "text-yellow-600"
                      : "text-green-600"
                  }`}
                >
                  {risk.score}
                </span>
              </td>
              <td className="px-4 py-3 text-gray-600 whitespace-nowrap">
                {risk.owner}
              </td>
              <td className="px-4 py-3 text-gray-500 whitespace-nowrap">
                {risk.createdDate}
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/risks/${risk.id}/edit`);
                  }}
                  className="text-blue-600 hover:underline text-xs mr-3"
                >
                  Edit
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteTarget(risk);
                  }}
                  className="text-red-500 hover:underline text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))
        )}
      </tbody>
    </table>
  </div>

  {/* Pagination stays OUTSIDE the scroll div */}
  {!loading && totalElements > 0 && (
    <Pagination
      currentPage={currentPage}
      totalPages={totalPages}
      totalElements={totalElements}
      pageSize={PAGE_SIZE}
      onPageChange={setCurrentPage}
    />
  )}
</div>

      {/* Delete Confirmation Modal */}
      {deleteTarget && (
        <ConfirmModal
          message={`Are you sure you want to delete "${deleteTarget.title}"? This action cannot be undone.`}
          onConfirm={handleDeleteConfirm}
          onCancel={() => setDeleteTarget(null)}
          loading={deleteLoading}
        />
      )}
    </div>
    </PageWrapper>
  );
};

export default RiskListPage;