// frontend/src/pages/Investments.tsx

import React, { useEffect, useState } from "react";
import { Plus, Download, Pencil, Trash2, TrendingUp, TrendingDown } from "lucide-react";
import { Card, CardHeader } from "../components/Card";
import { Button } from "../components/Button";
import { Modal } from "../components/Modal";
import { Input } from "../components/Input";
import { investmentService } from "../services/investmentService";
import { Investment, InvestmentCreate, AssetType } from "../types";
import { toast } from "sonner";
import { format } from "date-fns";

const ASSET_TYPES: AssetType[] = ["Stock", "MutualFund", "FD", "Gold", "Crypto", "Bond", "Other"];

export const Investments: React.FC = () => {
  const [investments, setInvestments] = useState<Investment[]>([]);
  const [portfolioSummary, setPortfolioSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingInvestment, setEditingInvestment] = useState<Investment | null>(null);

  const [formData, setFormData] = useState<InvestmentCreate>({
    asset_type: "Stock",
    asset_name: "",
    symbol: "",
    quantity: 0,
    purchase_price: 0,
    current_price: 0,
    purchase_date: format(new Date(), "yyyy-MM-dd"),
    platform: "",
    notes: "",
  });

  useEffect(() => {
    loadInvestments();
  }, []);

  const loadInvestments = async () => {
    try {
      const data = await investmentService.getInvestments();
      setInvestments(data.investments);
      setPortfolioSummary(data.portfolio_summary);
    } catch (error) {
      toast.error("Failed to load investments");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingInvestment) {
        await investmentService.updateInvestment(editingInvestment.id, formData);
        toast.success("Investment updated successfully");
      } else {
        await investmentService.createInvestment(formData);
        toast.success("Investment created successfully");
      }
      closeModal();
      loadInvestments();
    } catch (error) {
      toast.error("Failed to save investment");
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this investment?")) return;

    try {
      await investmentService.deleteInvestment(id);
      toast.success("Investment deleted successfully");
      loadInvestments();
    } catch (error) {
      toast.error("Failed to delete investment");
    }
  };

  const handleEdit = (investment: Investment) => {
    setEditingInvestment(investment);
    setFormData({
      asset_type: investment.asset_type,
      asset_name: investment.asset_name,
      symbol: investment.symbol || "",
      quantity: investment.quantity,
      purchase_price: investment.purchase_price,
      current_price: investment.current_price,
      purchase_date: investment.purchase_date,
      maturity_date: investment.maturity_date || "",
      platform: investment.platform || "",
      interest_rate: investment.interest_rate || undefined,
      notes: investment.notes || "",
    });
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingInvestment(null);
    setFormData({
      asset_type: "Stock",
      asset_name: "",
      symbol: "",
      quantity: 0,
      purchase_price: 0,
      current_price: 0,
      purchase_date: format(new Date(), "yyyy-MM-dd"),
      platform: "",
      notes: "",
    });
  };

  const handleExportCSV = async () => {
    try {
      const blob = await investmentService.exportCSV();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `investments_${format(new Date(), "yyyy-MM-dd")}.csv`;
      a.click();
      toast.success("Investments exported successfully");
    } catch (error) {
      toast.error("Failed to export investments");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Investments</h1>
          <p className="text-gray-600 mt-2">Manage your investment portfolio</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExportCSV}>
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Add Investment
          </Button>
        </div>
      </div>

      {/* Portfolio Summary */}
      {portfolioSummary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <p className="text-sm font-medium text-gray-600">Total Invested</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              ₹{portfolioSummary.total_invested.toLocaleString()}
            </p>
          </Card>
          <Card>
            <p className="text-sm font-medium text-gray-600">Current Value</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              ₹{portfolioSummary.total_current_value.toLocaleString()}
            </p>
          </Card>
          <Card>
            <p className="text-sm font-medium text-gray-600">Total Gain/Loss</p>
            <p
              className={`text-3xl font-bold mt-2 ${
                portfolioSummary.total_gain_loss >= 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              ₹{portfolioSummary.total_gain_loss.toLocaleString()}
            </p>
          </Card>
          <Card>
            <p className="text-sm font-medium text-gray-600">Returns</p>
            <p
              className={`text-3xl font-bold mt-2 ${
                portfolioSummary.total_gain_loss_percentage >= 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              {portfolioSummary.total_gain_loss_percentage.toFixed(2)}%
            </p>
          </Card>
        </div>
      )}

      {/* Investments List */}
      <Card>
        <CardHeader title="Your Portfolio" subtitle={`${investments.length} investments`} />
        {investments.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Asset</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Type</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">
                    Quantity
                  </th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">
                    Invested
                  </th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">
                    Current Value
                  </th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">
                    Gain/Loss
                  </th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {investments.map((investment) => (
                  <tr key={investment.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4">
                      <p className="text-sm font-medium text-gray-900">{investment.asset_name}</p>
                      {investment.symbol && (
                        <p className="text-xs text-gray-500">{investment.symbol}</p>
                      )}
                      {investment.platform && (
                        <p className="text-xs text-gray-500">{investment.platform}</p>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {investment.asset_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right text-sm text-gray-600">
                      {investment.quantity}
                    </td>
                    <td className="py-3 px-4 text-right text-sm text-gray-900">
                      ₹{investment.invested_amount.toLocaleString()}
                    </td>
                    <td className="py-3 px-4 text-right text-sm font-semibold text-gray-900">
                      ₹{investment.current_value.toLocaleString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div
                        className={`flex items-center justify-end ${
                          investment.percentage_gain >= 0 ? "text-green-600" : "text-red-600"
                        }`}
                      >
                        {investment.percentage_gain >= 0 ? (
                          <TrendingUp className="w-4 h-4 mr-1" />
                        ) : (
                          <TrendingDown className="w-4 h-4 mr-1" />
                        )}
                        <span className="text-sm font-semibold">
                          {investment.percentage_gain >= 0 ? "+" : ""}
                          {investment.percentage_gain.toFixed(2)}%
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">
                        ₹{investment.absolute_gain.toLocaleString()}
                      </p>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleEdit(investment)}
                        className="text-primary-600 hover:text-primary-800 mr-3"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(investment.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">No investments yet</p>
            <Button className="mt-4" onClick={() => setIsModalOpen(true)}>
              Add Your First Investment
            </Button>
          </div>
        )}
      </Card>

      {/* Add/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={editingInvestment ? "Edit Investment" : "Add New Investment"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Asset Type <span className="text-red-500">*</span>
              </label>
              <select
                value={formData.asset_type}
                onChange={(e) =>
                  setFormData({ ...formData, asset_type: e.target.value as AssetType })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              >
                {ASSET_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>

            <Input
              label="Asset Name"
              value={formData.asset_name}
              onChange={(e) => setFormData({ ...formData, asset_name: e.target.value })}
              required
              placeholder="e.g., Reliance Industries"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Symbol/Ticker"
              value={formData.symbol}
              onChange={(e) => setFormData({ ...formData, symbol: e.target.value })}
              placeholder="e.g., RELIANCE, BTC"
            />

            <Input
              type="number"
              step="0.00000001"
              label="Quantity"
              value={formData.quantity}
              onChange={(e) =>
                setFormData({ ...formData, quantity: parseFloat(e.target.value) || 0 })
              }
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              type="number"
              step="0.01"
              label="Purchase Price (per unit)"
              value={formData.purchase_price}
              onChange={(e) =>
                setFormData({ ...formData, purchase_price: parseFloat(e.target.value) || 0 })
              }
              required
            />

            <Input
              type="number"
              step="0.01"
              label="Current Price (per unit)"
              value={formData.current_price}
              onChange={(e) =>
                setFormData({ ...formData, current_price: parseFloat(e.target.value) || 0 })
              }
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              type="date"
              label="Purchase Date"
              value={formData.purchase_date}
              onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })}
              required
            />

            <Input
              type="date"
              label="Maturity Date"
              value={formData.maturity_date || ""}
              onChange={(e) => setFormData({ ...formData, maturity_date: e.target.value })}
              placeholder="For FD, Bonds"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Platform/Broker"
              value={formData.platform}
              onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
              placeholder="e.g., Zerodha, Groww"
            />

            <Input
              type="number"
              step="0.01"
              label="Interest Rate (%)"
              value={formData.interest_rate || ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  interest_rate: e.target.value ? parseFloat(e.target.value) : undefined,
                })
              }
              placeholder="For FD, Bonds"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows={3}
              placeholder="Additional notes..."
            />
          </div>

          <div className="flex space-x-3 pt-4">
            <Button type="button" variant="secondary" onClick={closeModal} className="flex-1">
              Cancel
            </Button>
            <Button type="submit" className="flex-1">
              {editingInvestment ? "Update" : "Create"} Investment
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
