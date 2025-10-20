// frontend/src/services/dashboardService.ts

import api from "./api";
import { DashboardData, HealthScore } from "../types";

export const dashboardService = {
  // Get complete dashboard data
  async getDashboard(): Promise<DashboardData> {
    const response = await api.get<DashboardData>("/api/dashboard/");
    return response.data;
  },

  // Get financial health score
  async getHealthScore(): Promise<HealthScore> {
    const response = await api.get<HealthScore>("/api/dashboard/health-score");
    return response.data;
  },

  // Export complete data
  async exportComplete(): Promise<any> {
    const response = await api.get("/api/export/complete");
    return response.data;
  },
};
