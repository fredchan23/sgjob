import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { getCategories } from "../api";

export default function CategoryChart() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getCategories().then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (data.length === 0) return <p className="text-gray-400">Loading...</p>;

  return (
    <ResponsiveContainer width="100%" height={600}>
      <BarChart
        data={data}
        layout="vertical"
        margin={{ left: 220, right: 20, top: 10, bottom: 10 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" />
        <YAxis type="category" dataKey="category" width={210} tick={{ fontSize: 12 }} />
        <Tooltip formatter={(v) => v.toLocaleString()} />
        <Bar dataKey="count" fill="#3b82f6" name="Job Count" />
      </BarChart>
    </ResponsiveContainer>
  );
}
