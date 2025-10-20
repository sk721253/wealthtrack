// frontend/src/pages/Expenses.tsx

import React, { useEffect, useState } from "react";
import { Plus, Download, Pencil, Trash2, Filter } from "lucide-react";
import { Card, CardHeader } from "../components/Card";
import { Button } from "../components/Button";
import { Modal } from "../components/Modal";
import { Input } from "../components/Input";
import { expenseService } from "../services/expenseService";
import { Expense, ExpenseCreate } from "../types";
import { toast } from "sonner";
import { format } from "date-fns";

const CATEGORIES = [
  "Food",
  "Transport",
  "Entertainment",
  "Shopping",
  "Bills",
  "Healthcare",
  "Education",
  "Other",
];

export const Expenses: React.FC = () => {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingExpense, setEditingExpense] = useState<Expense | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>("");

  const [formData, setFormData] = useState<ExpenseCreate>({
    title: "",
    amount: 0,
    category: "Food",
    date: format(new Date(), "yyyy-MM-dd"),
    payment_method: "",
    notes: "",
  });

  useEffect(() => {
    loadExpenses();
  }, [categoryFilter]);

  const loadExpenses = async () => {
    try {
      const data = await expenseService.getExpenses({
        category: categoryFilter || undefined,
      });
      setExpenses(data.expenses);
      setTotalAmount(data.total_amount);
      setTotalCount(data.total_count);
    } catch (error) {
      toast.error("Failed to load expenses");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingExpense) {
        await expenseService.updateExpense(editingExpense.id, formData);
        toast.success("Expense updated successfully");
      } else {
        await expenseService.createExpense(formData);
        toast.success("Expense created successfully");
      }
      closeModal();
      loadExpenses();
    } catch (error) {
      toast.error("Failed to save expense");
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this expense?")) return;

    try {
      await expenseService.deleteExpense(id);
      toast.success("Expense deleted successfully");
      loadExpenses();
    } catch (error) {
      toast.error("Failed to delete expense");
    }
  };

  const handleEdit = (expense: Expense) => {
    setEditingExpense(expense);
    setFormData({
      title: expense.title,
      amount: expense.amount,
      category: expense.category,
      date: expense.date,
      payment_method: expense.payment_method || "",
      notes: expense.notes || "",
    });
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingExpense(null);
    setFormData({
      title: "",
      amount: 0,
      category: "Food",
      date: format(new Date(), "yyyy-MM-dd"),
      payment_method: "",
      notes: "",
    });
  };

  const handleExportCSV = async () => {
    try {
      const blob = await expenseService.exportCSV();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `expenses_${format(new Date(), "yyyy-MM-dd")}.csv`;
      a.click();
      toast.success("Expenses exported successfully");
    } catch (error) {
      toast.error("Failed to export expenses");
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
          <h1 className="text-3xl font-bold text-gray-900">Expenses</h1>
          <p className="text-gray-600 mt-2">Track and manage your expenses</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExportCSV}>
            <Download className="w-4 h-4 mr-2" />
            Export CSV
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Add Expense
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <p className="text-sm font-medium text-gray-600">Total Expenses</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{totalCount}</p>
        </Card>
        <Card>
          <p className="text-sm font-medium text-gray-600">Total Amount</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">₹{totalAmount.toLocaleString()}</p>
        </Card>
        <Card>
          <p className="text-sm font-medium text-gray-600">Average Expense</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            ₹{totalCount > 0 ? (totalAmount / totalCount).toFixed(2) : 0}
          </p>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <div className="flex items-center space-x-4">
          <Filter className="w-5 h-5 text-gray-400" />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">All Categories</option>
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* Expenses List */}
      <Card>
        <CardHeader title="Recent Expenses" />
        {expenses.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Date</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">Title</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-600">
                    Category
                  </th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">Amount</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-gray-600">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {expenses.map((expense) => (
                  <tr key={expense.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4 text-sm text-gray-600">
                      {format(new Date(expense.date), "MMM dd, yyyy")}
                    </td>
                    <td className="py-3 px-4">
                      <p className="text-sm font-medium text-gray-900">{expense.title}</p>
                      {expense.notes && <p className="text-xs text-gray-500">{expense.notes}</p>}
                    </td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                        {expense.category}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right text-sm font-semibold text-gray-900">
                      ₹{expense.amount.toLocaleString()}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleEdit(expense)}
                        className="text-primary-600 hover:text-primary-800 mr-3"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(expense.id)}
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
            <p className="text-gray-500">No expenses found</p>
            <Button className="mt-4" onClick={() => setIsModalOpen(true)}>
              Add Your First Expense
            </Button>
          </div>
        )}
      </Card>

      {/* Add/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={editingExpense ? "Edit Expense" : "Add New Expense"}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
            placeholder="e.g., Grocery Shopping"
          />

          <Input
            type="number"
            step="0.01"
            label="Amount"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: parseFloat(e.target.value) })}
            required
            placeholder="0.00"
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category <span className="text-red-500">*</span>
            </label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            >
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          <Input
            type="date"
            label="Date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />

          <Input
            label="Payment Method"
            value={formData.payment_method}
            onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
            placeholder="e.g., Cash, Credit Card, UPI"
          />

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
              {editingExpense ? "Update" : "Create"} Expense
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
