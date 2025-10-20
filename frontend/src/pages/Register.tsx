// frontend/src/pages/Register.tsx

import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Mail, Lock, User, TrendingUp } from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { toast } from "sonner";

export const Register: React.FC = () => {
  const navigate = useNavigate();
  const { register, isLoading, error, clearError } = useAuthStore();

  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [validationError, setValidationError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    setValidationError("");

    // Validation
    if (formData.password.length < 8) {
      setValidationError("Password must be at least 8 characters");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setValidationError("Passwords do not match");
      return;
    }

    try {
      await register(formData.email, formData.fullName, formData.password);
      toast.success("Registration successful! Welcome to WealthTrack!");
      navigate("/dashboard");
    } catch (err) {
      toast.error("Registration failed. Please try again.");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-full mb-4">
            <TrendingUp className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">WealthTrack</h1>
          <p className="text-gray-600 mt-2">Start your wealth journey today</p>
        </div>

        {/* Register Card */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Create Account</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="text"
              name="fullName"
              label="Full Name"
              placeholder="John Doe"
              value={formData.fullName}
              onChange={handleChange}
              required
              icon={<User className="w-5 h-5 text-gray-400" />}
            />

            <Input
              type="email"
              name="email"
              label="Email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleChange}
              required
              icon={<Mail className="w-5 h-5 text-gray-400" />}
            />

            <Input
              type="password"
              name="password"
              label="Password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              required
              icon={<Lock className="w-5 h-5 text-gray-400" />}
            />

            <Input
              type="password"
              name="confirmPassword"
              label="Confirm Password"
              placeholder="••••••••"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              icon={<Lock className="w-5 h-5 text-gray-400" />}
            />

            {(validationError || error) && (
              <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg text-sm">
                {validationError || error}
              </div>
            )}

            <Button type="submit" className="w-full" isLoading={isLoading}>
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{" "}
              <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-600 mt-8">
          © 2025 WealthTrack. All rights reserved.
        </p>
      </div>
    </div>
  );
};
