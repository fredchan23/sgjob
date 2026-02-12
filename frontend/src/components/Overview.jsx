import { useState, useEffect } from "react";
import { getOverview } from "../api";

function KpiCard({ label, value }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <p className="text-sm text-gray-500 mb-1">{label}</p>
      <p className="text-2xl font-semibold text-gray-800">{value}</p>
    </div>
  );
}

export default function Overview() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getOverview().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (!data) return <p className="text-gray-400">Loading...</p>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <KpiCard label="Total Jobs" value={data.total_jobs.toLocaleString()} />
      <KpiCard
        label="Average Salary (SGD)"
        value={`$${data.avg_salary.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
      />
      <KpiCard
        label="Total Vacancies"
        value={data.total_vacancies.toLocaleString()}
      />
      <KpiCard label="Top Category" value={data.top_category} />
      <KpiCard label="Earliest Posting" value={data.date_min} />
      <KpiCard label="Latest Posting" value={data.date_max} />
    </div>
  );
}
