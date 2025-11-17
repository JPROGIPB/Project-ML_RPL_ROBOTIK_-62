import api from "./client";

export interface Robot {
  robot_id: number;
  robot_name: string;
  model: string;
  model_type: string;
  status: string;
  battery_lvl: number;
  location: string;
  current_position: {
    latitude: number;
    longitude: number;
    depth: number;
  } | null;
  firmware_version: string;
  owner_id: number | null;
  last_maint: string | null;
  created_at: string;
}

export interface RobotStatus {
  robot_id: number;
  connected: boolean;
  battery: number;
  position: {
    latitude: number;
    longitude: number;
    depth: number;
  };
  sensors: {
    temperature: number | null;
    ph: number | null;
    water_quality: number | null;
  };
  speed: number;
  status: string;
  timestamp: string | null;
}

export interface ManualControlData {
  action: string;
  direction?: string;
  speed?: number;
}

export const robotApi = {
  getRobots: async (forRental = false): Promise<Robot[]> => {
    const params = forRental ? { for_rental: 'true' } : {};
    const response = await api.get("/robots", { params });
    return response.data.robots;
  },

  getRobot: async (robotId: number): Promise<Robot> => {
    const response = await api.get(`/robots/${robotId}`);
    return response.data;
  },

  getRobotStatus: async (robotId: number): Promise<RobotStatus> => {
    const response = await api.get(`/robots/${robotId}/status`);
    return response.data;
  },

  startRobot: async (robotId: number): Promise<void> => {
    await api.post(`/robots/${robotId}/control/start`);
  },

  stopRobot: async (robotId: number): Promise<void> => {
    await api.post(`/robots/${robotId}/control/stop`);
  },

  manualControl: async (
    robotId: number,
    data: ManualControlData
  ): Promise<void> => {
    await api.post(`/robots/${robotId}/control/manual`, data);
  },

  switchMode: async (
    robotId: number,
    mode: "manual" | "auto"
  ): Promise<void> => {
    await api.put(`/robots/${robotId}/control/mode`, { mode });
  },
};

