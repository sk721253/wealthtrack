// frontend/src/services/expenseService.ts

import api from "./api";
import {
  Expense,
  ExpenseCreate,
  ExpenseUpdate,
  ExpenseListResponse,
  CategorySummary,
  MonthlySummary,
} from "../types";

export const expenseService = {
  // Get all expenses with filters
  async getExpenses(params?: {
    skip?: number;
    limit?: number;
    category?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<ExpenseListResponse> {
    const response = await api.get<ExpenseListResponse>("/api/expenses/", { params });
    return response.data;
  },

  // Get single expense
  async getExpense(id: string): Promise<Expense> {
    const response = await api.get<Expense>(`/api/expenses/${id}`);
    return response.data;
  },

  // Create expense
  async createExpense(data: ExpenseCreate): Promise<Expense> {
    const response = await api.post<Expense>("/api/expenses/", data);
    return response.data;
  },

  // Update expense
  async updateExpense(id: string, data: ExpenseUpdate): Promise<Expense> {
    const response = await api.put<Expense>(`/api/expenses/${id}`, data);
    return response.data;
  },

  // Delete expense
  async deleteExpense(id: string): Promise<void> {
    await api.delete(`/api/expenses/${id}`);
  },

  // Get category summary
  async getCategorySummary(params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<CategorySummary[]> {
    const response = await api.get<CategorySummary[]>("/api/expenses/summary/by-category", {
      params,
    });
    return response.data;
  },

  // Get monthly summary
  async getMonthlySummary(year?: number): Promise<MonthlySummary[]> {
    const response = await api.get<MonthlySummary[]>("/api/expenses/summary/by-month", {
      params: year ? { year } : undefined,
    });
    return response.data;
  },

  // Export expenses as CSV
  async exportCSV(): Promise<Blob> {
    const response = await api.get("/api/export/expenses/csv", {
      responseType: "blob",
    });
    return response.data;
  },
};
