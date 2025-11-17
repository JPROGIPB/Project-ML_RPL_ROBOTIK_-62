import api from "./client";

export interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  description: string;
  image_url: string;
  features: string[];
  is_available: boolean;
  stock_quantity: number;
}

export const productApi = {
  getProducts: async (category?: string): Promise<Product[]> => {
    const params = category ? { category } : {};
    const response = await api.get("/products", { params });
    return response.data.products;
  },

  getProduct: async (productId: number): Promise<Product> => {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },
};

