// frontend/src/services/investmentService.ts

import api from "./api";
import {
  Investment,
  InvestmentCreate,
  InvestmentUpdate,
  InvestmentListResponse,
  AssetAllocation,
  AssetType,
} from "../types";

export const investmentService = {
  // Get all investments
  async getInvestments(params?: {
    skip?: number;
    limit?: number;
    asset_type?: AssetType;
    platform?: string;
  }): Promise<InvestmentListResponse> {
    const response = await api.get<InvestmentListResponse>("/api/investments/", { params });
    return response.data;
  },

  // Get single investment
  async getInvestment(id: string): Promise<Investment> {
    const response = await api.get<Investment>(`/api/investments/${id}`);
    return response.data;
  },

  // Create investment
  async createInvestment(data: InvestmentCreate): Promise<Investment> {
    const response = await api.post<Investment>("/api/investments/", data);
    return response.data;
  },

  // Update investment
  async updateInvestment(id: string, data: InvestmentUpdate): Promise<Investment> {
    const response = await api.put<Investment>(`/api/investments/${id}`, data);
    return response.data;
  },

  // Update price only
  async updatePrice(id: string, currentPrice: number): Promise<Investment> {
    const response = await api.patch<Investment>(`/api/investments/${id}/price`, {
      current_price: currentPrice,
    });
    return response.data;
  },

  // Delete investment
  async deleteInvestment(id: string): Promise<void> {
    await api.delete(`/api/investments/${id}`);
  },

  // Get asset allocation
  async getAssetAllocation(): Promise<AssetAllocation[]> {
    const response = await api.get<AssetAllocation[]>(
      "/api/investments/analytics/asset-allocation"
    );
    return response.data;
  },

  // Get top performers
  async getTopPerformers(limit: number = 5): Promise<Investment[]> {
    const response = await api.get<Investment[]>("/api/investments/analytics/top-performers", {
      params: { limit },
    });
    return response.data;
  },

  // Get worst performers
  async getWorstPerformers(limit: number = 5): Promise<Investment[]> {
    const response = await api.get<Investment[]>("/api/investments/analytics/worst-performers", {
      params: { limit },
    });
    return response.data;
  },

  // Get platform summary
  async getPlatformSummary(): Promise<any[]> {
    const response = await api.get("/api/investments/analytics/platform-summary");
    return response.data;
  },

  // Get investment statistics
  async getStatistics(): Promise<any> {
    const response = await api.get("/api/investments/analytics/statistics");
    return response.data;
  },

  // Export investments as CSV
  async exportCSV(): Promise<Blob> {
    const response = await api.get("/api/export/investments/csv", {
      responseType: "blob",
    });
    return response.data;
  },
};
