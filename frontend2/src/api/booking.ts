import api from "./client";

export interface Booking {
  booking_id: number;
  user_id: number;
  robot_id: number | null;
  product_id: number | null;
  booking_type: "rental" | "purchase";
  start_date: string;
  end_date: string | null;
  duration_days: number | null;
  location: string;
  status: string;
  total_cost: number;
  created_at: string;
}

export interface CreateBookingData {
  booking_type: "rental" | "purchase";
  start_date: string;
  duration_days?: number;
  location: string;
  robot_id?: number;
  product_id?: number;
}

export interface PaymentData {
  method: string;
}

export interface Payment {
  payment_id: number;
  booking_id: number;
  amount: number;
  method: string;
  status: string;
  paid_at: string | null;
  transaction_id: string;
  created_at: string;
}

export const bookingApi = {
  getBookings: async (status?: string): Promise<Booking[]> => {
    const params = status ? { status } : {};
    const response = await api.get("/bookings", { params });
    return response.data.bookings;
  },

  getBooking: async (bookingId: number): Promise<Booking> => {
    const response = await api.get(`/bookings/${bookingId}`);
    return response.data;
  },

  createBooking: async (data: CreateBookingData): Promise<Booking> => {
    const response = await api.post("/bookings", data);
    return response.data.booking;
  },

  createPayment: async (
    bookingId: number,
    data: PaymentData
  ): Promise<Payment> => {
    const response = await api.post(`/bookings/${bookingId}/payment`, data);
    return response.data.payment;
  },
};

