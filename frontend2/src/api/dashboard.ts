import api from "./client";

export interface DashboardOverview {
  robots_active: number;
  robots_total: number;
  area_cleaned_today: number;
  waste_collected_today: number;
  energy_efficiency: number;
  water_quality_avg: number;
  recent_activity: {
    id: number;
    time: string;
    activity: string;
    status: string;
  }[];
}

export interface RobotStatus {
  robot_id: number;
  name: string;
  status: string;
  battery: number;
  area_cleaned: number;
  current_mission: {
    id: number;
    name: string;
  } | null;
}

export interface PerformanceData {
  time: string;
  area: number;
  energy: number;
}

export const dashboardApi = {
  getOverview: async (): Promise<DashboardOverview> => {
    const response = await api.get("/dashboard/overview");
    return response.data;
  },

  getRobotsStatus: async (): Promise<RobotStatus[]> => {
    const response = await api.get("/dashboard/robots/status");
    return response.data.robots;
  },

  getPerformance: async (): Promise<PerformanceData[]> => {
    const response = await api.get("/dashboard/analytics/performance");
    return response.data.performance_data;
  },

  getActivityLog: async (limit?: number): Promise<any[]> => {
    const params = limit ? { limit } : {};
    const response = await api.get("/dashboard/activity-log", { params });
    return response.data.activity;
  },

  getAllBookings: async (limit?: number): Promise<any[]> => {
    const params = limit ? { limit } : {};
    const response = await api.get("/dashboard/bookings", { params });
    return response.data.bookings;
  },
};

