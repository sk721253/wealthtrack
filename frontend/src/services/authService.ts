// frontend/src/services/authService.ts

import api from "./api";
import { User, LoginCredentials, RegisterData, AuthResponse } from "../types";

export const authService = {
  // Register new user
  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>("/api/auth/register", data);
    return response.data;
  },

  // Login user
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // Backend expects form data for OAuth2
    const formData = new URLSearchParams();
    formData.append("username", credentials.username);
    formData.append("password", credentials.password);

    const response = await api.post<AuthResponse>("/api/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    // Store token
    localStorage.setItem("access_token", response.data.access_token);

    return response.data;
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>("/api/auth/me");
    // Store user data
    localStorage.setItem("user", JSON.stringify(response.data));
    return response.data;
  },

  // Logout
  logout(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem("access_token");
  },

  // Get stored user
  getStoredUser(): User | null {
    const userStr = localStorage.getItem("user");
    return userStr ? JSON.parse(userStr) : null;
  },
};
