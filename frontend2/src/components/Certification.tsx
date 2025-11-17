import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Progress } from "./ui/progress";
import { Badge } from "./ui/badge";
import { CheckCircle2, Lock, PlayCircle, Award, Loader2 } from "lucide-react";
import {
  certificationApi,
  CertificationModule,
  CertificationProgress,
  Certificate,
} from "../api/certification";
import { toast } from "sonner";

interface CertificationProps {
  isCertified: boolean;
  certificationProgress: number;
  onCompleteCertification: () => void;
  setCurrentPage: (page: string) => void;
}

export function Certification({
  isCertified,
  certificationProgress,
  onCompleteCertification,
  setCurrentPage,
}: CertificationProps) {
  const [selectedModule, setSelectedModule] =
    useState<CertificationModule | null>(null);
  const [modules, setModules] = useState<CertificationModule[]>([]);
  const [progress, setProgress] = useState<CertificationProgress | null>(null);
  const [certificate, setCertificate] = useState<Certificate | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);

  // Load modules and progress on mount
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // Always load modules (public endpoint)
      const modulesData = await certificationApi.getModules();
      setModules(modulesData);

      // Try to load progress (requires login)
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const progressData = await certificationApi.getProgress();
          setProgress(progressData);

          // Update parent component if needed
          if (progressData.is_certified && !isCertified) {
            onCompleteCertification();
          }
        }
      } catch (progressError: any) {
        // If user not logged in, just continue without progress
        if (progressError.response?.status !== 401) {
          console.error("Error loading progress:", progressError);
        }
      }
    } catch (error: any) {
      console.error("Error loading certification data:", error);
      toast.error("Gagal memuat data sertifikasi");
    } finally {
      setLoading(false);
    }
  };

  const handleModuleClick = async (module: CertificationModule) => {
    setSelectedModule(module);

    // Check if user is logged in
    const token = localStorage.getItem("access_token");
    if (!token) {
      toast.error("Silakan login terlebih dahulu untuk memulai sertifikasi");
      return;
    }

    // If module not completed, simulate progress update
    const moduleProgress = progress?.modules.find((m) => m.id === module.id);
    if (!moduleProgress?.completed) {
      try {
        // Simulate completing module (in real app, this would be after user completes the content)
        await certificationApi.updateProgress(module.id, 100, true);
        toast.success(`Modul ${module.module_number} selesai!`);
        await loadData(); // Reload progress
      } catch (error: any) {
        toast.error(error.response?.data?.error || "Gagal memperbarui progress");
      }
    }
  };

  const handleCompleteCertification = async () => {
    try {
      setCompleting(true);
      const cert = await certificationApi.completeCertification();
      setCertificate(cert);
      toast.success("Selamat! Sertifikasi berhasil diselesaikan!");
      await loadData(); // Reload to get updated status
      onCompleteCertification();
    } catch (error: any) {
      toast.error(
        error.response?.data?.error || "Gagal menyelesaikan sertifikasi"
      );
    } finally {
      setCompleting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 pb-16 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const currentProgress = progress?.overall_progress || certificationProgress;
  const isUserCertified = progress?.is_certified || isCertified;

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl mb-4">
            Sertifikasi Operator Sealen
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Dapatkan sertifikasi resmi dan akses penuh ke produk robot pembersih
            laut Sealen
          </p>
        </div>

        {isUserCertified ? (
          // Certified View
          <div className="space-y-8">
            <Card className="bg-gradient-to-r from-accent/20 to-primary/20 border-2 border-accent p-8">
              <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="flex items-center gap-4">
                  <div className="bg-accent text-accent-foreground rounded-full p-4">
                    <Award className="h-12 w-12" />
                  </div>
                  <div>
                    <Badge className="mb-2 bg-accent text-accent-foreground">
                      ✓ Tersertifikasi Resmi
                    </Badge>
                    <h2 className="text-2xl mb-1">
                      Selamat! Anda Sudah Bersertifikat
                    </h2>
                    <p className="text-muted-foreground">
                      Anda memiliki akses penuh ke semua produk dan layanan
                      Sealen
                    </p>
                  </div>
                </div>
                <Button
                  size="lg"
                  onClick={() => setCurrentPage("products")}
                  className="bg-primary hover:bg-primary/90"
                >
                  Lihat Produk Sealen
                </Button>
              </div>
            </Card>

            {/* Certificate Display */}
            {certificate && (
              <Card className="p-8 bg-card border-2 border-border">
                <div className="text-center space-y-4">
                  <h3 className="text-2xl">Sertifikat Digital Anda</h3>
                  <div className="max-w-2xl mx-auto bg-gradient-to-br from-primary/10 to-accent/10 p-8 rounded-lg border-2 border-primary">
                    <div className="space-y-4">
                      <Award className="h-16 w-16 mx-auto text-primary" />
                      <h4 className="text-xl">{certificate.cert_type}</h4>
                      <p className="text-muted-foreground">Diberikan kepada:</p>
                      <p className="text-2xl">Operator Bersertifikat</p>
                      <p className="text-sm text-muted-foreground">
                        Tanggal:{" "}
                        {new Date(certificate.issued_date).toLocaleDateString(
                          "id-ID"
                        )}
                      </p>
                      <div className="pt-4 border-t border-border">
                        <p className="text-sm text-muted-foreground">
                          ID Sertifikat: {certificate.cert_number}
                        </p>
                        <p className="text-xs text-muted-foreground mt-2">
                          Status: {certificate.status}
                        </p>
                      </div>
                    </div>
                  </div>
                  <Button variant="outline">Download Sertifikat (PDF)</Button>
                </div>
              </Card>
            )}
          </div>
        ) : (
          // Not Certified View
          <div className="space-y-8">
            {/* Progress Overview */}
            <Card className="p-8 bg-card">
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-2xl">Progress Sertifikasi</h3>
                  <span className="text-2xl text-primary">
                    {currentProgress}%
                  </span>
                </div>
                <Progress value={currentProgress} className="h-3" />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>
                    {progress?.completed_modules || 0} dari{" "}
                    {progress?.total_modules || modules.length} modul selesai
                  </span>
                  <span>
                    {progress?.total_modules || modules.length} modul total
                  </span>
                </div>
                <p className="text-muted-foreground">
                  Selesaikan semua modul untuk mendapatkan sertifikasi dan akses
                  pembelian robot
                </p>
              </div>
            </Card>

            {/* Notice */}
            <div className="bg-accent/10 border border-accent rounded-lg p-6">
              <div className="flex gap-3">
                <Lock className="h-6 w-6 text-accent flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-lg mb-1">Akses Terbatas</h4>
                  <p className="text-muted-foreground">
                    Selesaikan sertifikasi untuk membuka akses pembelian robot
                    Sealen. Anda masih dapat menyewa robot tanpa sertifikasi.
                  </p>
                </div>
              </div>
            </div>

            {/* Course Modules */}
            <div className="grid md:grid-cols-2 gap-6">
              {(
                progress?.modules ||
                modules.map((m) => ({
                  ...m,
                  completed: false,
                  progress_percentage: 0,
                }))
              ).map((module) => {
                const moduleData =
                  modules.find((m) => m.id === module.id) || module;
                const isCompleted =
                  "completed" in module ? module.completed : false;
                const progressPercent =
                  "progress_percentage" in module
                    ? module.progress_percentage
                    : 0;

                return (
                  <Card
                    key={module.id}
                    className={`p-6 cursor-pointer transition-all hover:shadow-lg ${
                      isCompleted ? "border-accent" : "border-border"
                    }`}
                    onClick={() => handleModuleClick(moduleData)}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        {isCompleted ? (
                          <CheckCircle2 className="h-6 w-6 text-accent" />
                        ) : (
                          <PlayCircle className="h-6 w-6 text-muted-foreground" />
                        )}
                        <Badge
                          variant={isCompleted ? "default" : "secondary"}
                          className={isCompleted ? "bg-accent" : ""}
                        >
                          Modul {module.module_number || module.id}
                        </Badge>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        {moduleData.duration_minutes} menit
                      </span>
                    </div>
                    <h4 className="text-lg mb-2">{moduleData.title}</h4>
                    <p className="text-sm text-muted-foreground mb-3">
                      {moduleData.description}
                    </p>
                    {!isCompleted && progressPercent > 0 && (
                      <div className="mt-2">
                        <Progress value={progressPercent} className="h-2" />
                        <p className="text-xs text-muted-foreground mt-1">
                          {progressPercent}% selesai
                        </p>
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              {currentProgress === 100 && !isUserCertified ? (
                <Button
                  size="lg"
                  onClick={handleCompleteCertification}
                  className="bg-accent hover:bg-accent/90"
                  disabled={completing}
                >
                  {completing ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Memproses...
                    </>
                  ) : (
                    "Selesaikan Sertifikasi"
                  )}
                </Button>
              ) : (
                <Button
                  size="lg"
                  onClick={() => {
                    if (modules.length > 0) {
                      handleModuleClick(modules[0]);
                    }
                  }}
                  className="bg-accent hover:bg-accent/90"
                >
                  Mulai Sertifikasi
                </Button>
              )}
              <Button
                size="lg"
                variant="outline"
                onClick={() => setCurrentPage("rent")}
              >
                Sewa Robot (Tanpa Sertifikasi)
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
