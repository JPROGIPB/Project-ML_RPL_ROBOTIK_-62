import api from "./client";

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  role: string;
  username?: string;
}

export interface User {
  user_id: number;
  username: string;
  email: string;
  full_name: string;
  role: string;
  is_certified: boolean;
  created_at: string;
}

export interface AuthResponse {
  message: string;
  access_token: string;
  refresh_token: string;
  user: User;
}

export const authApi = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post("/auth/register", data);
    const { access_token, refresh_token, user } = response.data;

    // Store tokens
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post("/auth/login", data);
    const { access_token, refresh_token, user } = response.data;

    // Store tokens
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    return response.data;
  },

  logout: async (): Promise<void> => {
    try {
      await api.post("/auth/logout");
    } finally {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get("/auth/me");
    return response.data.user;
  },

  refreshToken: async (): Promise<string> => {
    const response = await api.post("/auth/refresh");
    const { access_token } = response.data;
    localStorage.setItem("access_token", access_token);
    return access_token;
  },
};

