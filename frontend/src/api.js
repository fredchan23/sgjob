const BASE = "/api";

async function fetchJSON(path) {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function getOverview() {
  return fetchJSON("/overview");
}

export function getSalaries(groupBy = "category") {
  return fetchJSON(`/salaries?group_by=${groupBy}`);
}

export function getCategories() {
  return fetchJSON("/categories");
}

export function getCompanies(limit = 20) {
  return fetchJSON(`/companies?limit=${limit}`);
}

export function getTrends(interval = "month") {
  return fetchJSON(`/trends?interval=${interval}`);
}
