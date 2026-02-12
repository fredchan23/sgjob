import { useState } from "react";
import Overview from "./components/Overview";
import SalaryChart from "./components/SalaryChart";
import CategoryChart from "./components/CategoryChart";
import CompanyTable from "./components/CompanyTable";
import TrendsChart from "./components/TrendsChart";

const TABS = [
  { key: "overview", label: "Overview", component: Overview },
  { key: "salaries", label: "Salaries", component: SalaryChart },
  { key: "categories", label: "Categories", component: CategoryChart },
  { key: "companies", label: "Companies", component: CompanyTable },
  { key: "trends", label: "Trends", component: TrendsChart },
];

export default function App() {
  const [activeTab, setActiveTab] = useState("overview");
  const ActiveComponent = TABS.find((t) => t.key === activeTab).component;

  return (
    <div className="min-h-screen">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-800">
            SG Job Data Dashboard
          </h1>
        </div>
      </header>

      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 flex gap-1">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab.key
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <ActiveComponent />
      </main>
    </div>
  );
}
