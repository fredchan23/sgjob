import { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { getTrends } from "../api";

export default function TrendsChart() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getTrends("month").then(setData).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (data.length === 0) return <p className="text-gray-400">Loading...</p>;

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="period"
          tick={{ fontSize: 11 }}
          interval={Math.floor(data.length / 12)}
        />
        <YAxis tickFormatter={(v) => v.toLocaleString()} />
        <Tooltip formatter={(v) => v.toLocaleString()} />
        <Line
          type="monotone"
          dataKey="count"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={false}
          name="Job Postings"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
