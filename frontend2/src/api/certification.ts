import api from "./client";

export interface CertificationModule {
  id: number;
  module_number: number;
  title: string;
  duration_minutes: number;
  description: string;
  order_index: number;
}

export interface UserProgress {
  id: number;
  module_id: number;
  completed: boolean;
  progress_percentage: number;
  completed_at: string | null;
}

export interface CertificationProgress {
  modules: (CertificationModule & {
    completed: boolean;
    progress_percentage: number;
  })[];
  overall_progress: number;
  completed_modules: number;
  total_modules: number;
  is_certified: boolean;
}

export interface Certificate {
  cert_id: number;
  user_id: number;
  cert_type: string;
  issued_date: string;
  expiry_date: string | null;
  status: string;
  cert_number: string;
}

export const certificationApi = {
  getModules: async (): Promise<CertificationModule[]> => {
    const response = await api.get("/certification/modules");
    return response.data.modules;
  },

  getProgress: async (): Promise<CertificationProgress> => {
    const response = await api.get("/certification/progress");
    return response.data;
  },

  updateProgress: async (
    moduleId: number,
    progress: number,
    completed: boolean
  ): Promise<UserProgress> => {
    const response = await api.post(`/certification/progress/${moduleId}`, {
      progress_percentage: progress,
      completed,
    });
    return response.data.progress;
  },

  completeCertification: async (): Promise<Certificate> => {
    const response = await api.post("/certification/complete");
    return response.data.certificate;
  },
};

