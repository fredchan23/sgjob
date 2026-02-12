import { useState, useEffect } from "react";
import { getCompanies } from "../api";

export default function CompanyTable() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getCompanies(20).then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (data.length === 0) return <p className="text-gray-400">Loading...</p>;

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white rounded-lg shadow">
        <thead>
          <tr className="bg-gray-100 text-left text-sm font-medium text-gray-600">
            <th className="px-4 py-3">#</th>
            <th className="px-4 py-3">Company</th>
            <th className="px-4 py-3 text-right">Job Count</th>
            <th className="px-4 py-3 text-right">Avg Salary (SGD)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr
              key={row.company}
              className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}
            >
              <td className="px-4 py-2 text-sm text-gray-500">{i + 1}</td>
              <td className="px-4 py-2 text-sm font-medium">{row.company}</td>
              <td className="px-4 py-2 text-sm text-right">
                {row.job_count.toLocaleString()}
              </td>
              <td className="px-4 py-2 text-sm text-right">
                ${row.avg_salary.toLocaleString(undefined, { maximumFractionDigits: 0 })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
