import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { Waves, Eye, EyeOff } from "lucide-react";
import { authApi } from "../api/auth";
import { toast } from "sonner";

interface LoginProps {
  onLogin: (role: string) => void;
  setCurrentPage: (page: string) => void;
}

interface FormData {
  email: string;
  password: string;
  remember: boolean;
}

interface Errors {
  email?: string;
  password?: string;
}

export function Login({ onLogin, setCurrentPage }: LoginProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: "",
    remember: false,
  });
  const [errors, setErrors] = useState<Errors>({});

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Errors = {};

    if (!formData.email) {
      newErrors.email = "Email wajib diisi";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Format email tidak valid";
    }

    if (!formData.password) {
      newErrors.password = "Password wajib diisi";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password minimal 6 karakter";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    try {
      const response = await authApi.login({
        email: formData.email,
        password: formData.password,
      });

      toast.success(`Berhasil login sebagai ${response.user.role}`);
      onLogin(response.user.role);
    } catch (error: any) {
      toast.error(error.response?.data?.error || "Login gagal");
      setErrors({ email: "Email atau password salah" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-16 flex items-center justify-center">
      <div className="w-full max-w-6xl mx-4 my-8">
        <div className="grid md:grid-cols-2 bg-card rounded-2xl overflow-hidden shadow-2xl border border-border">
          {/* Left Panel - Image */}
          <div className="relative hidden md:block">
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1711062717295-b12347cb17e6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjbGVhbiUyMG9jZWFuJTIwd2F0ZXJ8ZW58MXx8fHwxNzYyMjQ3NzAxfDA&ixlib=rb-4.1.0&q=80&w=1080"
              alt="Ocean"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-primary/80 via-primary/40 to-transparent flex items-end p-8">
              <div className="text-white">
                <h2 className="text-3xl mb-2">Selamat Datang Kembali</h2>
                <p className="text-white/90">
                  Lanjutkan misi kebersihan laut bersama Sealen
                </p>
              </div>
            </div>
          </div>

          {/* Right Panel - Form */}
          <div className="p-8 md:p-12 flex flex-col justify-center">
            <div className="flex items-center gap-2 mb-8">
              <Waves className="h-10 w-10 text-primary" />
              <span className="text-2xl">Sealen</span>
            </div>

            <h1 className="text-3xl mb-2">Login</h1>
            <p className="text-muted-foreground mb-8">
              Masuk ke akun Anda untuk mengakses dashboard
            </p>

            <form onSubmit={handleSubmit} className="space-y-6">
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
                    placeholder="Masukkan password"
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
                {errors.password && (
                  <p className="text-destructive text-sm mt-1">
                    {errors.password}
                  </p>
                )}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Checkbox
                    id="remember"
                    checked={formData.remember}
                    onCheckedChange={(checked) =>
                      setFormData({ ...formData, remember: !!checked })
                    }
                  />
                  <Label htmlFor="remember" className="cursor-pointer">
                    Ingat saya
                  </Label>
                </div>
                <button
                  type="button"
                  className="text-sm text-primary hover:underline"
                >
                  Lupa Password?
                </button>
              </div>

              <Button
                type="submit"
                className="w-full bg-primary hover:bg-primary/90"
                size="lg"
                disabled={loading}
              >
                {loading ? "Memproses..." : "Masuk"}
              </Button>

              <div className="grid grid-cols-2 gap-3">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => onLogin("Admin")}
                  className="text-sm"
                >
                  Demo Admin
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => onLogin("Operator")}
                  className="text-sm"
                >
                  Demo Operator
                </Button>
              </div>

              <p className="text-center text-sm text-muted-foreground">
                Belum punya akun?{" "}
                <button
                  type="button"
                  onClick={() => setCurrentPage("register")}
                  className="text-primary hover:underline"
                >
                  Daftar sekarang
                </button>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
