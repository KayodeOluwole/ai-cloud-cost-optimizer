import React, { useEffect, useState } from "react";
import { fetchCosts, fetchCostAnalysis } from "../api/api.ts";
import type { CostItem, CostAnalysis } from "../api/api.ts";
import Charts from "./Charts";



const CostDashboard: React.FC = () => {
  const [costs, setCosts] = useState<CostItem[]>([]);
  const [analysis, setAnalysis] = useState<CostAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [costData, analysisData] = await Promise.all([
          fetchCosts(),
          fetchCostAnalysis(),
        ]);
        setCosts(costData);
        setAnalysis(analysisData);
      } catch (err: any) {
        setError("Failed to load data");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: "red" }}>{error}</div>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Azure Cost Dashboard</h1>

      <table border={1} cellPadding={8} style={{ marginBottom: "2rem" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Resource</th>
            <th>Amount</th>
            <th>Currency</th>
            <th>Date</th>
            <th>Category</th>
          </tr>
        </thead>

        <tbody>
          {costs.map((c) => (
            <tr key={c.id}>
              <td>{c.id}</td>
              <td>{c.resource_id}</td>
              <td>{c.cost_amount}</td>
              <td>{c.currency}</td>
              <td>{c.usage_date}</td>
              <td>{c.meterCategory}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <Charts costs={costs} />

      {analysis && (
        <div style={{ marginTop: "2rem" }}>
          <h2>AI Cost Insights</h2>
          <p><b>Score:</b> {analysis.score.overall_health}/100</p>
          <p><b>Explanation:</b> {analysis.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default CostDashboard;
