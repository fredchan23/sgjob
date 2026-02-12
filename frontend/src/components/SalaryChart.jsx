import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { getSalaries } from "../api";

export default function SalaryChart() {
  const [data, setData] = useState([]);
  const [groupBy, setGroupBy] = useState("category");
  const [error, setError] = useState(null);

  useEffect(() => {
    getSalaries(groupBy).then(setData).catch((e) => setError(e.message));
  }, [groupBy]);

  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
    <div>
      <div className="mb-4 flex items-center gap-2">
        <label className="text-sm font-medium text-gray-600">Group by:</label>
        <select
          value={groupBy}
          onChange={(e) => setGroupBy(e.target.value)}
          className="border rounded px-2 py-1 text-sm"
        >
          <option value="category">Category</option>
          <option value="position_level">Position Level</option>
        </select>
      </div>

      {data.length === 0 ? (
        <p className="text-gray-400">Loading...</p>
      ) : (
        <ResponsiveContainer width="100%" height={500}>
          <BarChart
            data={data.slice(0, 20)}
            layout="vertical"
            margin={{ left: 180, right: 20, top: 10, bottom: 10 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tickFormatter={(v) => `$${v.toLocaleString()}`} />
            <YAxis type="category" dataKey="group" width={170} tick={{ fontSize: 12 }} />
            <Tooltip formatter={(v) => `$${v.toLocaleString()}`} />
            <Legend />
            <Bar dataKey="min_salary" fill="#93c5fd" name="Min" />
            <Bar dataKey="avg_salary" fill="#3b82f6" name="Avg" />
            <Bar dataKey="max_salary" fill="#1d4ed8" name="Max" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
