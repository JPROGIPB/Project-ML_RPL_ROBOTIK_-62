import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { Waves, Eye, EyeOff, Check, X } from "lucide-react";
import { authApi } from "../api/auth";
import { toast } from "sonner";

interface RegisterProps {
  onRegister: (role: string) => void;
  setCurrentPage: (page: string) => void;
}

interface FormData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: string;
}

interface Errors {
  name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  role?: string;
}

export function Register({ onRegister, setCurrentPage }: RegisterProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "",
  });
  const [errors, setErrors] = useState<Errors>({});

  const passwordRequirements = [
    { text: "Minimal 8 karakter", valid: formData.password.length >= 8 },
    { text: "Mengandung huruf besar", valid: /[A-Z]/.test(formData.password) },
    { text: "Mengandung huruf kecil", valid: /[a-z]/.test(formData.password) },
    { text: "Mengandung angka", valid: /[0-9]/.test(formData.password) },
  ];

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Errors = {};

    if (!formData.name) newErrors.name = "Nama wajib diisi";
    if (!formData.email) {
      newErrors.email = "Email wajib diisi";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Format email tidak valid";
    }
    if (!formData.password) {
      newErrors.password = "Password wajib diisi";
    } else if (!passwordRequirements.every((req) => req.valid)) {
      newErrors.password = "Password tidak memenuhi persyaratan";
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Password tidak cocok";
    }
    if (!formData.role) newErrors.role = "Pilih role";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    try {
      const response = await authApi.register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: formData.role,
      });

      toast.success(`Akun berhasil dibuat sebagai ${response.user.role}`);
      onRegister(response.user.role);
    } catch (error: any) {
      toast.error(error.response?.data?.error || "Registrasi gagal");
      if (error.response?.data?.error?.includes("Email")) {
        setErrors({ email: error.response.data.error });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-16 flex items-center justify-center">
      <div className="w-full max-w-6xl mx-4 my-8">
        <div className="grid md:grid-cols-2 bg-card rounded-2xl overflow-hidden shadow-2xl border border-border">
          <div className="relative hidden md:block">
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1610093366806-b2907e880fb7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvY2VhbiUyMHBvbGx1dGlvbiUyMGNsZWFudXB8ZW58MXx8fHwxNzYyMzExMTc1fDA&ixlib=rb-4.1.0&q=80&w=1080"
              alt="Ocean Cleanup"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-accent/80 via-accent/40 to-transparent flex items-end p-8">
              <div className="text-white">
                <h2 className="text-3xl mb-2">Bergabung dengan Sealen</h2>
                <p className="text-white/90">
                  Mulai perjalanan Anda menuju laut yang lebih bersih
                </p>
              </div>
            </div>
          </div>

          <div className="p-8 md:p-12 flex flex-col justify-center max-h-screen overflow-y-auto">
            <div className="flex items-center gap-2 mb-6">
              <Waves className="h-10 w-10 text-primary" />
              <span className="text-2xl">Sealen</span>
            </div>

            <h1 className="text-3xl mb-2">Daftar Akun</h1>
            <p className="text-muted-foreground mb-6">
              Buat akun untuk mengakses platform Sealen
            </p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <Label htmlFor="name">Nama Lengkap</Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="John Doe"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className={`mt-2 ${errors.name ? "border-destructive" : ""}`}
                />
                {errors.name && (
                  <p className="text-destructive text-sm mt-1">{errors.name}</p>
                )}
              </div>

              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="nama@email.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className={`mt-2 ${errors.email ? "border-destructive" : ""}`}
                />
                {errors.email && (
                  <p className="text-destructive text-sm mt-1">
                    {errors.email}
                  </p>
                )}
              </div>

              <div>
                <Label htmlFor="password">Password</Label>
                <div className="relative mt-2">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Buat password"
                    value={formData.password}
                    onChange={(e) =>
                      setFormData({ ...formData, password: e.target.value })
                    }
                    className={
                      errors.password ? "border-destructive pr-10" : "pr-10"
                    }
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>

                {formData.password && (
                  <div className="mt-2 space-y-1">
                    {passwordRequirements.map((req, idx) => (
                      <div
                        key={idx}
                        className="flex items-center gap-2 text-xs"
                      >
                        {req.valid ? (
                          <Check className="h-3 w-3 text-accent" />
                        ) : (
                          <X className="h-3 w-3 text-muted-foreground" />
                        )}
                        <span
                          className={
                            req.valid ? "text-accent" : "text-muted-foreground"
                          }
                        >
                          {req.text}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <Label htmlFor="confirmPassword">Konfirmasi Password</Label>
                <div className="relative mt-2">
                  <Input
                    id="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Ulangi password"
                    value={formData.confirmPassword}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        confirmPassword: e.target.value,
                      })
                    }
                    className={
                      errors.confirmPassword
                        ? "border-destructive pr-10"
                        : "pr-10"
                    }
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="text-destructive text-sm mt-1">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>

              <div>
                <Label htmlFor="role">Role</Label>
                <Select
                  value={formData.role}
                  onValueChange={(value) =>
                    setFormData({ ...formData, role: value })
                  }
                >
                  <SelectTrigger
                    id="role"
                    className={`mt-2 ${
                      errors.role ? "border-destructive" : ""
                    }`}
                  >
                    <SelectValue placeholder="Pilih role Anda" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="operator">Operator</SelectItem>
                    <SelectItem value="customer">Customer</SelectItem>
                  </SelectContent>
                </Select>
                {errors.role && (
                  <p className="text-destructive text-sm mt-1">{errors.role}</p>
                )}
              </div>

              <Button
                type="submit"
                className="w-full bg-accent hover:bg-accent/90"
                size="lg"
                disabled={loading}
              >
                {loading ? "Memproses..." : "Daftar Sekarang"}
              </Button>

              <p className="text-center text-sm text-muted-foreground">
                Sudah punya akun?{" "}
                <button
                  type="button"
                  onClick={() => setCurrentPage("login")}
                  className="text-primary hover:underline"
                >
                  Login di sini
                </button>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
