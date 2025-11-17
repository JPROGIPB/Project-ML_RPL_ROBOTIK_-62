import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { Badge } from "./ui/badge";
import { Calendar, Loader2 } from "lucide-react";
import { robotApi, Robot } from "../api/robot";
import { bookingApi, Booking } from "../api/booking";
import { toast } from "sonner";

interface RentalForm {
  robot: string;
  startDate: string;
  duration: string;
  location: string;
}

const RENTAL_PRICE_PER_DAY = 1500000; // Default rental price per day

export function RentRobot() {
  const [rentalForm, setRentalForm] = useState<RentalForm>({
    robot: "",
    startDate: "",
    duration: "",
    location: "",
  });
  const [robots, setRobots] = useState<Robot[]>([]);
  const [rentalHistory, setRentalHistory] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // Check if user is logged in
      const token = localStorage.getItem("access_token");

      // Load robots (requires login)
      let robotsData: Robot[] = [];
      let bookingsData: Booking[] = [];

      if (token) {
        [robotsData, bookingsData] = await Promise.all([
          robotApi.getRobots(true).catch((err) => {
            console.error("Error loading robots:", err);
            return [];
          }),
          bookingApi.getBookings("rental").catch(() => []),
        ]);
      } else {
        // If not logged in, just load robots for rental
        robotsData = await robotApi.getRobots(true).catch((err) => {
          console.error("Error loading robots:", err);
          return [];
        });
      }

      console.log("Robots loaded:", robotsData); // Debug log

      // Backend already filters for rental (owner_id is null or current user)
      // Just filter out maintenance/broken status
      const availableRobots = robotsData.filter((r) => {
        return (
          r.status !== "maintenance" &&
          r.status !== "broken" &&
          r.status !== null
        );
      });

      console.log("Available robots after filter:", availableRobots); // Debug log

      setRobots(availableRobots);
      setRentalHistory(bookingsData);
    } catch (error: any) {
      console.error("Error loading data:", error);
      if (error.response?.status !== 401) {
        toast.error("Gagal memuat data");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof RentalForm, value: string) => {
    setRentalForm({ ...rentalForm, [field]: value });
  };

  const calculatePrice = () => {
    if (!rentalForm.robot || !rentalForm.duration) return 0;

    const days = parseInt(rentalForm.duration);
    let basePrice = RENTAL_PRICE_PER_DAY * days;

    // Apply discounts for long-term rental
    if (days >= 180) {
      basePrice *= 0.7; // 30% discount
    } else if (days >= 90) {
      basePrice *= 0.8; // 20% discount
    } else if (days >= 30) {
      basePrice *= 0.9; // 10% discount
    }

    return basePrice;
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(price);
  };

  const handleSubmit = async () => {
    // Check if user is logged in
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Silakan login terlebih dahulu untuk menyewa robot");
      return;
    }

    if (
      !rentalForm.robot ||
      !rentalForm.startDate ||
      !rentalForm.duration ||
      !rentalForm.location
    ) {
      toast.error("Harap lengkapi semua field");
      return;
    }

    try {
      setProcessing(true);

      // Create rental booking
      const booking = await bookingApi.createBooking({
        booking_type: "rental",
        start_date: new Date(rentalForm.startDate).toISOString(),
        duration_days: parseInt(rentalForm.duration),
        location: rentalForm.location,
        robot_id: parseInt(rentalForm.robot),
      });

      // Create payment
      await bookingApi.createPayment(booking.booking_id, {
        method: "credit-card", // Default payment method
      });

      toast.success("Penyewaan berhasil! Robot akan dikirim sesuai jadwal.");

      // Reset form
      setRentalForm({
        robot: "",
        startDate: "",
        duration: "",
        location: "",
      });

      // Reload data
      await loadData();
    } catch (error: any) {
      console.error("Rental error:", error);
      toast.error(error.response?.data?.error || "Gagal membuat penyewaan");
    } finally {
      setProcessing(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("id-ID");
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case "confirmed":
      case "active":
        return "bg-accent";
      case "completed":
      case "selesai":
        return "bg-muted";
      case "pending":
        return "bg-chart-3";
      default:
        return "bg-muted";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 pb-16 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const selectedRobot = robots.find(
    (r) => r.robot_id.toString() === rentalForm.robot
  );
  const totalPrice = calculatePrice();

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl mb-4">Sewa Robot Sealen</h1>
          <p className="text-xl text-muted-foreground">
            Solusi fleksibel untuk kebutuhan pembersihan laut sementara
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Rental Form */}
          <Card className="p-8">
            <h2 className="text-2xl mb-6">Form Penyewaan</h2>

            <div className="space-y-6">
              {/* Robot Selection */}
              <div>
                <Label htmlFor="robot">Pilih Robot</Label>
                <Select
                  value={rentalForm.robot}
                  onValueChange={(value) => handleInputChange("robot", value)}
                >
                  <SelectTrigger id="robot" className="mt-2">
                    <SelectValue placeholder="Pilih robot yang ingin disewa" />
                  </SelectTrigger>
                  <SelectContent>
                    {robots.length === 0 ? (
                      <SelectItem value="none" disabled>
                        Tidak ada robot tersedia
                      </SelectItem>
                    ) : (
                      robots.map((robot) => (
                        <SelectItem
                          key={robot.robot_id}
                          value={robot.robot_id.toString()}
                        >
                          {robot.robot_name} ({robot.model}) -{" "}
                          {formatPrice(RENTAL_PRICE_PER_DAY)}/hari
                        </SelectItem>
                      ))
                    )}
                  </SelectContent>
                </Select>
              </div>

              {/* Start Date */}
              <div>
                <Label htmlFor="startDate">Tanggal Mulai</Label>
                <div className="relative mt-2">
                  <Input
                    id="startDate"
                    type="date"
                    value={rentalForm.startDate}
                    onChange={(e) =>
                      handleInputChange("startDate", e.target.value)
                    }
                    min={new Date().toISOString().split("T")[0]}
                  />
                  <Calendar className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
                </div>
              </div>

              {/* Duration */}
              <div>
                <Label htmlFor="duration">Durasi Sewa (hari)</Label>
                <Select
                  value={rentalForm.duration}
                  onValueChange={(value) =>
                    handleInputChange("duration", value)
                  }
                >
                  <SelectTrigger id="duration" className="mt-2">
                    <SelectValue placeholder="Pilih durasi sewa" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1 hari - Harian</SelectItem>
                    <SelectItem value="7">7 hari - Mingguan</SelectItem>
                    <SelectItem value="14">14 hari - 2 Minggu</SelectItem>
                    <SelectItem value="30">30 hari - Bulanan (-10%)</SelectItem>
                    <SelectItem value="90">90 hari - 3 Bulan (-20%)</SelectItem>
                    <SelectItem value="180">
                      180 hari - 6 Bulan (-30%)
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Location */}
              <div>
                <Label htmlFor="location">Lokasi Pengiriman</Label>
                <Input
                  id="location"
                  type="text"
                  placeholder="Masukkan alamat lengkap"
                  value={rentalForm.location}
                  onChange={(e) =>
                    handleInputChange("location", e.target.value)
                  }
                  className="mt-2"
                />
              </div>

              {/* Price Estimate */}
              {rentalForm.robot && rentalForm.duration && totalPrice > 0 && (
                <div className="bg-primary/10 rounded-lg p-4 border border-primary">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-muted-foreground">
                      Estimasi Total
                    </span>
                    <span className="text-2xl text-primary">
                      {formatPrice(totalPrice)}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Harga sudah termasuk asuransi dan pemeliharaan dasar
                  </p>
                </div>
              )}

              {/* Submit Button */}
              <Button
                className="w-full bg-primary hover:bg-primary/90"
                size="lg"
                disabled={
                  !rentalForm.robot ||
                  !rentalForm.startDate ||
                  !rentalForm.duration ||
                  !rentalForm.location ||
                  processing
                }
                onClick={handleSubmit}
              >
                {processing ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Memproses...
                  </>
                ) : (
                  "Lanjut ke Pembayaran"
                )}
              </Button>
            </div>
          </Card>

          {/* Available Robots Info */}
          <div className="space-y-6">
            <Card className="p-8">
              <h3 className="text-xl mb-4">Keuntungan Sewa Robot</h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="bg-accent text-accent-foreground rounded-full p-1 mt-0.5">
                    <svg
                      className="h-4 w-4"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <div>
                    <h4>Tanpa Sertifikasi</h4>
                    <p className="text-sm text-muted-foreground">
                      Tidak perlu sertifikasi operator untuk menyewa
                    </p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="bg-accent text-accent-foreground rounded-full p-1 mt-0.5">
                    <svg
                      className="h-4 w-4"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <div>
                    <h4>Pemeliharaan Termasuk</h4>
                    <p className="text-sm text-muted-foreground">
                      Kami yang mengurus maintenance dan repair
                    </p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="bg-accent text-accent-foreground rounded-full p-1 mt-0.5">
                    <svg
                      className="h-4 w-4"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <div>
                    <h4>Fleksibel</h4>
                    <p className="text-sm text-muted-foreground">
                      Pilih durasi sesuai kebutuhan proyek
                    </p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="bg-accent text-accent-foreground rounded-full p-1 mt-0.5">
                    <svg
                      className="h-4 w-4"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <div>
                    <h4>Support 24/7</h4>
                    <p className="text-sm text-muted-foreground">
                      Tim teknis siap membantu kapan saja
                    </p>
                  </div>
                </li>
              </ul>
            </Card>

            <Card className="p-8 bg-gradient-to-br from-primary/10 to-accent/10">
              <h3 className="text-xl mb-3">Diskon Sewa Jangka Panjang</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Sewa 30 hari</span>
                  <Badge className="bg-accent">-10%</Badge>
                </div>
                <div className="flex justify-between">
                  <span>Sewa 90 hari</span>
                  <Badge className="bg-accent">-20%</Badge>
                </div>
                <div className="flex justify-between">
                  <span>Sewa 180 hari</span>
                  <Badge className="bg-accent">-30%</Badge>
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Rental History */}
        <Card className="p-8">
          <h2 className="text-2xl mb-6">Riwayat Penyewaan</h2>
          {rentalHistory.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">
              Belum ada riwayat penyewaan
            </p>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID Transaksi</TableHead>
                    <TableHead>Robot</TableHead>
                    <TableHead>Tanggal Mulai</TableHead>
                    <TableHead>Durasi</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Total</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rentalHistory.map((rental) => {
                    const robot = robots.find(
                      (r) => r.robot_id === rental.robot_id
                    );
                    return (
                      <TableRow key={rental.booking_id}>
                        <TableCell className="font-mono">
                          #{rental.booking_id}
                        </TableCell>
                        <TableCell>{robot?.robot_name || "Unknown"}</TableCell>
                        <TableCell>{formatDate(rental.start_date)}</TableCell>
                        <TableCell>{rental.duration_days || 0} hari</TableCell>
                        <TableCell>
                          <Badge className={getStatusBadgeClass(rental.status)}>
                            {rental.status}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">
                          {formatPrice(rental.total_cost)}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
