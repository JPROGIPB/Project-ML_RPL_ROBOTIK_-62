import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Badge } from "./ui/badge";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { Lock, Check, Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "./ui/dialog";
import { productApi, Product } from "../api/product";
import { bookingApi } from "../api/booking";
import { toast } from "sonner";

interface ProductsProps {
  isCertified: boolean;
  setCurrentPage: (page: string) => void;
}

export function Products({ isCertified, setCurrentPage }: ProductsProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [showPayment, setShowPayment] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState("credit-card");
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const data = await productApi.getProducts();
      setProducts(data);
    } catch (error: any) {
      console.error("Error loading products:", error);
      if (error.response?.status !== 401) {
        toast.error("Gagal memuat produk");
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = (product: Product) => {
    if (!isCertified) {
      toast.error("Anda harus menyelesaikan sertifikasi terlebih dahulu");
      setCurrentPage("certification");
      return;
    }
    setSelectedProduct(product);
    setShowPayment(true);
  };

  const handlePayment = async () => {
    if (!selectedProduct) return;

    try {
      setProcessing(true);

      // Create booking for purchase
      const booking = await bookingApi.createBooking({
        booking_type: "purchase",
        start_date: new Date().toISOString(),
        location: "Jakarta", // Default location, bisa diambil dari user profile
        product_id: selectedProduct.id,
      });

      // Create payment
      await bookingApi.createPayment(booking.booking_id, {
        method: paymentMethod,
      });

      toast.success("Pembayaran berhasil! Pesanan Anda sedang diproses.");
      setShowPayment(false);
      setSelectedProduct(null);
    } catch (error: any) {
      console.error("Payment error:", error);
      toast.error(error.response?.data?.error || "Gagal memproses pembayaran");
    } finally {
      setProcessing(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(price);
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 pb-16 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl mb-4">Produk Sealen</h1>
          <p className="text-xl text-muted-foreground">
            Teknologi terdepan untuk kebersihan laut yang berkelanjutan
          </p>
        </div>

        {/* Certification Notice */}
        {!isCertified && (
          <div className="bg-accent/10 border border-accent rounded-lg p-6 mb-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="flex items-start gap-3">
                <Lock className="h-6 w-6 text-accent flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-lg mb-1">
                    Sertifikasi Diperlukan untuk Pembelian
                  </h3>
                  <p className="text-muted-foreground">
                    Dapatkan sertifikasi operator untuk mengakses pembelian
                    produk. Atau pilih opsi sewa.
                  </p>
                </div>
              </div>
              <Button
                onClick={() => setCurrentPage("certification")}
                className="bg-accent hover:bg-accent/90 flex-shrink-0"
              >
                Mulai Sertifikasi
              </Button>
            </div>
          </div>
        )}

        {/* Products Grid */}
        {products.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Tidak ada produk tersedia</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {products
              .filter((product) => product.is_available)
              .map((product) => (
                <Card
                  key={product.id}
                  className="overflow-hidden hover:shadow-xl transition-all duration-300"
                >
                  <div className="relative h-48 overflow-hidden">
                    <ImageWithFallback
                      src={product.image_url}
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                    <Badge className="absolute top-3 right-3 bg-primary">
                      {product.category}
                    </Badge>
                    {product.stock_quantity === 0 && (
                      <Badge className="absolute top-3 left-3 bg-destructive">
                        Stok Habis
                      </Badge>
                    )}
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl mb-2">{product.name}</h3>
                    <p className="text-muted-foreground text-sm mb-4">
                      {product.description}
                    </p>

                    <ul className="space-y-2 mb-4">
                      {product.features.map((feature, idx) => (
                        <li
                          key={idx}
                          className="flex items-center gap-2 text-sm"
                        >
                          <Check className="h-4 w-4 text-accent flex-shrink-0" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>

                    <div className="flex items-center justify-between pt-4 border-t border-border">
                      <span className="text-xl text-primary">
                        {formatPrice(product.price)}
                      </span>
                      <Button
                        size="sm"
                        onClick={() => handlePurchase(product)}
                        disabled={!isCertified || product.stock_quantity === 0}
                        className={
                          isCertified ? "bg-primary hover:bg-primary/90" : ""
                        }
                      >
                        {isCertified ? (
                          "Beli Sekarang"
                        ) : (
                          <Lock className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
          </div>
        )}

        {/* Rent Option */}
        <div className="text-center bg-secondary rounded-xl p-8">
          <h3 className="text-2xl mb-3">Belum Siap Membeli?</h3>
          <p className="text-muted-foreground mb-6">
            Anda bisa menyewa robot Sealen untuk kebutuhan sementara tanpa perlu
            sertifikasi
          </p>
          <Button
            size="lg"
            variant="outline"
            onClick={() => setCurrentPage("rent")}
          >
            Lihat Opsi Sewa
          </Button>
        </div>
      </div>

      {/* Payment Dialog */}
      <Dialog open={showPayment} onOpenChange={setShowPayment}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Pembayaran - {selectedProduct?.name}</DialogTitle>
            <DialogDescription>
              Integrasi Midtrans Payment Gateway
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-6">
            {/* Order Summary */}
            <div className="bg-secondary rounded-lg p-4">
              <h4 className="mb-3">Ringkasan Pesanan</h4>
              <div className="flex justify-between mb-2">
                <span>{selectedProduct?.name}</span>
                <span>
                  {selectedProduct && formatPrice(selectedProduct.price)}
                </span>
              </div>
              <div className="flex justify-between text-sm text-muted-foreground mb-2">
                <span>Pajak (11%)</span>
                <span>
                  {selectedProduct && formatPrice(selectedProduct.price * 0.11)}
                </span>
              </div>
              <div className="border-t border-border pt-2 flex justify-between">
                <span>Total</span>
                <span className="text-primary">
                  {selectedProduct && formatPrice(selectedProduct.price * 1.11)}
                </span>
              </div>
            </div>

            {/* Payment Methods */}
            <div>
              <h4 className="mb-3">Pilih Metode Pembayaran</h4>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { id: "credit-card", name: "Kartu Kredit", icon: "💳" },
                  { id: "e-wallet", name: "E-Wallet", icon: "📱" },
                  { id: "bank-transfer", name: "Transfer Bank", icon: "🏦" },
                ].map((method) => (
                  <button
                    key={method.id}
                    onClick={() => setPaymentMethod(method.id)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      paymentMethod === method.id
                        ? "border-primary bg-primary/10"
                        : "border-border hover:border-primary/50"
                    }`}
                  >
                    <div className="text-3xl mb-2">{method.icon}</div>
                    <div className="text-sm">{method.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Payment Status */}
            <div className="flex gap-3">
              <Button
                className="flex-1 bg-accent hover:bg-accent/90"
                onClick={handlePayment}
                disabled={processing}
              >
                {processing ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Memproses...
                  </>
                ) : (
                  "Proses Pembayaran"
                )}
              </Button>
              <Button
                variant="outline"
                onClick={() => setShowPayment(false)}
                disabled={processing}
              >
                Batal
              </Button>
            </div>

            <p className="text-xs text-muted-foreground text-center">
              Pembayaran aman dengan Midtrans Payment Gateway
            </p>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
