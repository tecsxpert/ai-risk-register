import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, LineChart, Line,
  PieChart, Pie, Cell, Legend, AreaChart, Area,
} from "recharts";
import { getStats } from "../services/riskService";
import { generateReport } from "../services/aiService";
import { mockAnalyticsData, mockDetailedAnalytics, mockRisks } from "../services/mockData";
import ExportButton from "../components/ExportButton";
import StreamingReport from "../components/StreamingReport";
import ChartCard from "../components/ChartCard";
import PeriodSelector from "../components/PeriodSelector";
import RiskHeatmap from "../components/RiskHeatmap";
import StatsSummaryTable from "../components/StatsSummaryTable";
import ChartSkeleton from "../components/ChartSkeleton";
import CardSkeleton from "../components/CardSkeleton";
import PageWrapper from "../components/PageWrapper";
const COLORS = ["#1B4F8A", "#EF4444", "#EAB308", "#22C55E", "#8B5CF6", "#F97316"];
const CATEGORY_COLORS = {
  Security: "#1B4F8A",
  "AI Risk": "#8B5CF6",
  Compliance: "#EAB308",
  Operational: "#22C55E",
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg shadow px-3 py-2 text-xs">
        <p className="font-semibold text-gray-700 mb-1">{label}</p>
        {payload.map((p, i) => (
          <p key={i} style={{ color: p.color }}>
            {p.name}: <strong>{p.value}</strong>
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const AnalyticsPage = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [period, setPeriod] = useState("6m");

  // Streaming report
  const [report, setReport] = useState(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportError, setReportError] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getStats();
        setStats(data);
      } catch (err) {
        setError("Failed to load analytics data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Filter data by period
  const getFilteredTrend = () => {
  if (period === "4w") {
    return mockDetailedAnalytics.weeklyNew;
  }

  // For monthly periods — create count from mockAnalyticsData.monthlyTrend
  const all = mockAnalyticsData.monthlyTrend.map((item) => ({
    month: item.month,
    count: item.open + item.inProgress + item.resolved,
  }));

  if (period === "3m") return all.slice(-3);
  if (period === "6m") return all.slice(-6);
  return all;
};

  const getFilteredCategoryTrend = () => {
    const all = mockDetailedAnalytics.categoryTrend;
    if (period === "3m") return all.slice(-3);
    if (period === "6m") return all.slice(-6);
    return all;
  };

  const getFilteredClosureRate = () => {
    const all = mockDetailedAnalytics.closureRate;
    if (period === "3m") return all.slice(-3);
    if (period === "6m") return all.slice(-6);
    return all;
  };

  const handleGenerateReport = async () => {
    setReportLoading(true);
    setReportError("");
    setReport(null);
    setIsStreaming(false);
    try {
      const data = await generateReport(mockRisks);
      setReport(data);
      setIsStreaming(true);
      setTimeout(() => setIsStreaming(false), 8000);
    } catch (err) {
      setReportError("Failed to generate report. Please try again.");
    } finally {
      setReportLoading(false);
    }
  };

  return (
    <PageWrapper>
    <div className="p-6 max-w-7xl mx-auto">

      {/* Page Header */}
      <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Analytics</h1>
          <p className="text-gray-500 text-sm mt-1">
            Deep dive into your risk data
          </p>
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          <PeriodSelector selected={period} onChange={setPeriod} />
          <ExportButton risks={mockRisks} />
          <button
            onClick={() => navigate("/dashboard")}
            className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition text-sm"
          >
            ← Dashboard
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 text-sm mb-6">
          {error}
        </div>
      )}

      {/* KPI Summary Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {loading ? (
          [...Array(4)].map((_, i) => <CardSkeleton key={i} />)
        ) : (
          [
            { label: "Total Risks", value: stats.totalRisks, icon: "📋", color: "text-blue-900", bg: "bg-blue-50 border border-blue-100" },
            { label: "Avg Score", value: stats.averageScore, icon: "📊", color: "text-orange-600", bg: "bg-orange-50 border border-orange-100" },
            { label: "High Priority", value: stats.highPriority, icon: "🚨", color: "text-red-600", bg: "bg-red-50 border border-red-100" },
            { label: "Resolved", value: stats.resolvedRisks, icon: "✅", color: "text-green-600", bg: "bg-green-50 border border-green-100" },
          ].map((kpi, i) => (
            <div key={i} className={`${kpi.bg} rounded-xl p-4`}>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{kpi.icon}</span>
                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                  {kpi.label}
                </span>
              </div>
              <span className={`text-3xl font-bold ${kpi.color}`}>
                {kpi.value}
              </span>
            </div>
          ))
        )}
      </div>

      {/* Row 1 — Trend Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        {/* Line Chart — Risk count over time */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risk Count Over Time"
            subtitle={`Total risks logged — ${period === "4w" ? "Last 4 Weeks" : period === "3m" ? "Last 3 Months" : period === "6m" ? "Last 6 Months" : "All Time"}`}
          >
            <ResponsiveContainer width="100%" height={230}>
              <LineChart
  data={getFilteredTrend()}
  margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
>
  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
  <XAxis
    dataKey={period === "4w" ? "week" : "month"}  // ✅ this is correct
    tick={{ fontSize: 10 }}
  />
  <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
  <Tooltip content={<CustomTooltip />} />
  <Line
    type="monotone"
    dataKey="count"   // ✅ now all periods have count field
    name="Risks"
    stroke="#1B4F8A"
    strokeWidth={2.5}
    dot={{ r: 4, fill: "#1B4F8A" }}
    activeDot={{ r: 6 }}
  />
</LineChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {/* Area Chart — Open vs Closed */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risk Closure Rate"
            subtitle="Risks opened vs closed per month"
          >
            <ResponsiveContainer width="100%" height={230}>
              <AreaChart
                data={getFilteredClosureRate()}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <defs>
                  <linearGradient id="openGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#EF4444" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="closedGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22C55E" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#22C55E" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend
                  formatter={(v) => (
                    <span style={{ fontSize: 11 }}>{v}</span>
                  )}
                />
                <Area
                  type="monotone"
                  dataKey="opened"
                  name="Opened"
                  stroke="#EF4444"
                  fill="url(#openGrad)"
                  strokeWidth={2}
                />
                <Area
                  type="monotone"
                  dataKey="closed"
                  name="Closed"
                  stroke="#22C55E"
                  fill="url(#closedGrad)"
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>
        )}
      </div>

      {/* Row 2 — Category and Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        {/* Bar Chart — By Category */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risks by Category"
            subtitle="Distribution across risk categories"
          >
            <ResponsiveContainer width="100%" height={230}>
              <BarChart
                data={stats.byCategory}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis
                  dataKey="category"
                  tick={{ fontSize: 10 }}
                  interval={0}
                  angle={-15}
                  textAnchor="end"
                />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" name="Risks" radius={[4, 4, 0, 0]}>
                  {stats.byCategory.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {/* Pie Chart — By Status */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risks by Status"
            subtitle="Current status breakdown"
          >
            <ResponsiveContainer width="100%" height={230}>
              <PieChart>
                <Pie
                  data={stats.byStatus}
                  dataKey="count"
                  nameKey="status"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  innerRadius={35}
                  paddingAngle={3}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  labelLine={false}
                >
                  {stats.byStatus.map((_, i) => (
                    <Cell
                      key={i}
                      fill={["#EF4444", "#EAB308", "#22C55E"][i % 3]}
                    />
                  ))}
                </Pie>
                <Legend
                  formatter={(v) => (
                    <span style={{ fontSize: 11 }}>{v}</span>
                  )}
                />
                <Tooltip
                  contentStyle={{ borderRadius: "8px", fontSize: "12px" }}
                />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
        )}
      </div>

      {/* Row 3 — Category Score Trend and Priority */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        {/* Line Chart — Score per Category over time */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Avg Score per Category Over Time"
            subtitle="How category risk scores have changed"
          >
            <ResponsiveContainer width="100%" height={230}>
              <LineChart
                data={getFilteredCategoryTrend()}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Legend
                  formatter={(v) => (
                    <span style={{ fontSize: 11 }}>{v}</span>
                  )}
                />
                {Object.keys(CATEGORY_COLORS).map((cat) => (
                  <Line
                    key={cat}
                    type="monotone"
                    dataKey={cat}
                    name={cat}
                    stroke={CATEGORY_COLORS[cat]}
                    strokeWidth={2}
                    dot={{ r: 3 }}
                    activeDot={{ r: 5 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {/* Bar Chart — By Priority */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risks by Priority"
            subtitle="Distribution of High, Medium and Low priority"
          >
            <ResponsiveContainer width="100%" height={230}>
              <BarChart
                data={stats.byPriority}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="priority" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" name="Risks" radius={[4, 4, 0, 0]}>
                  {stats.byPriority.map((_, i) => (
                    <Cell
                      key={i}
                      fill={["#EF4444", "#EAB308", "#22C55E"][i % 3]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}
      </div>

      {/* Row 4 — Heatmap and Risk Age */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        {/* Heatmap — Category vs Priority */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risk Heatmap"
            subtitle="Category vs Priority — darker means more risks"
          >
            <RiskHeatmap data={mockDetailedAnalytics.heatmap} />
          </ChartCard>
        )}

        {/* Bar Chart — Risk Age */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Risk Age Distribution"
            subtitle="How long risks have been open"
          >
            <ResponsiveContainer width="100%" height={230}>
              <BarChart
                data={mockDetailedAnalytics.riskAge}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="bucket" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" name="Risks" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}
      </div>

      {/* Row 5 — Score Distribution and Risk Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

        {/* Bar Chart — Score Distribution */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="Score Distribution"
            subtitle="How risks are spread across score ranges"
          >
            <ResponsiveContainer width="100%" height={230}>
              <BarChart
                data={mockAnalyticsData.scoreDistribution}
                margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="range" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" name="Risks" radius={[4, 4, 0, 0]}>
                  {mockAnalyticsData.scoreDistribution.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {/* Risk Summary Table */}
        {loading ? <ChartSkeleton /> : (
          <ChartCard
            title="All Risks Summary"
            subtitle="Quick reference table of all risks"
          >
            <StatsSummaryTable risks={mockRisks} />
          </ChartCard>
        )}
      </div>

      {/* AI Report Section */}
      <div className="bg-white rounded-xl shadow p-5 mb-6">
        <div className="flex items-center justify-between mb-2">
          <div>
            <h2 className="text-base font-bold text-gray-800">
              🤖 AI Generated Executive Report
            </h2>
            <p className="text-xs text-gray-400 mt-0.5">
              AI analyses all risk data and streams a professional report
            </p>
          </div>
          <button
            onClick={handleGenerateReport}
            disabled={reportLoading}
            className="bg-purple-700 text-white px-4 py-2 rounded-lg hover:bg-purple-800 transition text-sm disabled:opacity-50 flex items-center gap-2"
          >
            {reportLoading ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                </svg>
                Generating...
              </>
            ) : (
              <>{report ? "🔄 Regenerate" : "🚀 Generate"} Report</>
            )}
          </button>
        </div>

        {reportError && (
          <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 text-sm mt-3">
            {reportError}
          </div>
        )}

        {reportLoading && (
          <div className="flex items-center gap-3 py-6 justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-700"></div>
            <p className="text-gray-500 text-sm">
              AI is analysing your risk data...
            </p>
          </div>
        )}

        {!report && !reportLoading && !reportError && (
          <div className="flex flex-col items-center py-6 gap-2 text-gray-400">
            <span className="text-4xl">📊</span>
            <p className="text-sm">
              Click Generate Report to get an AI executive summary
            </p>
          </div>
        )}
      </div>

      {/* Streaming Report Output */}
      <StreamingReport report={report} isStreaming={isStreaming} />

    </div>
    </PageWrapper>
  );
};

export default AnalyticsPage;