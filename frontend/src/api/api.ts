import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export interface CostItem {
  id: number;
  resource_id: string;
  cost_amount: number;
  currency: string;
  usage_date: string;
  meterCategory: string;
}

export interface CostAnalysis {
  summary: any;
  spikes: any[];
  high_cost_resources: any[];
  unused_resources: any[];
  trends: any;
  score: {
    overall_health: number;
    cost_risk: number;
    waste_risk: number;
  };
  explanation: string;
}

export async function fetchCosts(): Promise<CostItem[]> {
  const response = await axios.get(`${API_BASE}/costs`);
  return response.data;
}

export async function fetchCostAnalysis(): Promise<CostAnalysis> {
  const response = await axios.get(`${API_BASE}/costs/analysis`);
  return response.data;
}
