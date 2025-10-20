// frontend/src/pages/Dashboard.tsx

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  TrendingUp,
  TrendingDown,
  Wallet,
  DollarSign,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
} from "lucide-react";
import { Card, CardHeader } from "../components/Card";
import { dashboardService } from "../services/dashboardService";
import { DashboardData, HealthScore } from "../types";
import { toast } from "sonner";

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [healthScore, setHealthScore] = useState<HealthScore | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [dashboardData, health] = await Promise.all([
        dashboardService.getDashboard(),
        dashboardService.getHealthScore(),
      ]);
      setData(dashboardData);
      setHealthScore(health);
    } catch (error) {
      toast.error("Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Failed to load dashboard data</p>
      </div>
    );
  }

  const { summary, expenses, investments } = data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to your financial overview</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Net Worth */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Net Worth</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                ₹{summary.net_worth.toLocaleString()}
              </p>
            </div>
            <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-primary-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Investment portfolio value</p>
        </Card>

        {/* Investment Gains */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Investment Gains</p>
              <p className="text-2xl font-bold text-green-600 mt-1">
                ₹{summary.investment_gains.toLocaleString()}
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="flex items-center mt-2">
            {summary.investment_gains_percentage >= 0 ? (
              <ArrowUpRight className="w-4 h-4 text-green-600" />
            ) : (
              <ArrowDownRight className="w-4 h-4 text-red-600" />
            )}
            <span
              className={`text-xs font-medium ml-1 ${
                summary.investment_gains_percentage >= 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              {summary.investment_gains_percentage.toFixed(2)}%
            </span>
          </div>
        </Card>

        {/* Monthly Expenses */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">This Month</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                ₹{summary.current_month_expenses.toLocaleString()}
              </p>
            </div>
            <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
              <Wallet className="w-6 h-6 text-orange-600" />
            </div>
          </div>
          <div className="flex items-center mt-2">
            {summary.expense_change_percentage > 0 ? (
              <ArrowUpRight className="w-4 h-4 text-red-600" />
            ) : (
              <ArrowDownRight className="w-4 h-4 text-green-600" />
            )}
            <span
              className={`text-xs font-medium ml-1 ${
                summary.expense_change_percentage > 0 ? "text-red-600" : "text-green-600"
              }`}
            >
              {Math.abs(summary.expense_change_percentage).toFixed(1)}% vs last month
            </span>
          </div>
        </Card>

        {/* Health Score */}
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Health Score</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{healthScore?.score || 0}/100</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <Activity className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">{healthScore?.rating || "Good"}</p>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Expense Categories */}
        <Card>
          <CardHeader title="Top Expense Categories" subtitle="This month" />
          {expenses.top_categories.length > 0 ? (
            <div className="space-y-3">
              {expenses.top_categories.slice(0, 5).map((cat, index) => {
                const percentage =
                  expenses.current_month_total > 0
                    ? (cat.total_amount / expenses.current_month_total) * 100
                    : 0;
                return (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700">{cat.category}</span>
                      <span className="text-sm font-semibold text-gray-900">
                        ₹{cat.total_amount.toLocaleString()}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No expenses yet</p>
          )}
          <Link
            to="/expenses"
            className="mt-4 text-sm text-primary-600 hover:text-primary-700 font-medium inline-flex items-center"
          >
            View all expenses
            <ArrowUpRight className="w-4 h-4 ml-1" />
          </Link>
        </Card>

        {/* Top Performing Investments */}
        <Card>
          <CardHeader title="Top Performers" subtitle="Best investments" />
          {investments.top_performers.length > 0 ? (
            <div className="space-y-3">
              {investments.top_performers.slice(0, 5).map((inv, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between py-2 border-b last:border-0"
                >
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{inv.asset_name}</p>
                    <p className="text-xs text-gray-500">{inv.asset_type}</p>
                  </div>
                  <div className="text-right">
                    <p
                      className={`text-sm font-semibold ${
                        inv.percentage_gain >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      {inv.percentage_gain >= 0 ? "+" : ""}
                      {inv.percentage_gain.toFixed(2)}%
                    </p>
                    <p className="text-xs text-gray-500">₹{inv.current_value.toLocaleString()}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No investments yet</p>
          )}
          <Link
            to="/investments"
            className="mt-4 text-sm text-primary-600 hover:text-primary-700 font-medium inline-flex items-center"
          >
            View portfolio
            <ArrowUpRight className="w-4 h-4 ml-1" />
          </Link>
        </Card>
      </div>

      {/* Financial Health */}
      {healthScore && healthScore.recommendations.length > 0 && (
        <Card>
          <CardHeader title="Financial Health Recommendations" />
          <div className="space-y-3">
            {healthScore.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-xs font-bold">{index + 1}</span>
                </div>
                <p className="text-sm text-gray-700">{rec}</p>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};
