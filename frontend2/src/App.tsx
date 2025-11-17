import React, { useState, useEffect } from "react";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { Certification } from "./components/Certification";
import { Products } from "./components/Products";
import { RentRobot } from "./components/RentRobot";
import { RobotControl } from "./components/RobotControl";
import { Dashboard } from "./components/Dashboard";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import { Technology } from "./components/Technology";
import { Footer } from "./components/Footer";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [currentPage, setCurrentPage] = useState("home");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
  const [isCertified, setIsCertified] = useState(false);
  const [certificationProgress, setCertificationProgress] = useState(0);
  const [loading, setLoading] = useState(true);

  // Check if user is logged in on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem("access_token");
      if (token) {
        const { authApi } = await import("./api/auth");
        const user = await authApi.getCurrentUser();

        setIsLoggedIn(true);
        setUserRole(user.role || "");
        setIsCertified(user.is_certified || false);

        // Load certification progress
        if (user.is_certified) {
          setCertificationProgress(100);
        } else {
          try {
            const { certificationApi } = await import("./api/certification");
            const progress = await certificationApi.getProgress();
            setCertificationProgress(progress.overall_progress || 0);
          } catch (error) {
            // User might not have started certification yet
            setCertificationProgress(0);
          }
        }
      }
    } catch (error) {
      // Token invalid or expired, clear it
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    } finally {
      setLoading(false);
    }
  };

  // Apply dark mode class to html element
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  // Smooth scroll to top when page changes
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentPage]);

  const handleLogin = async (role: string) => {
    setIsLoggedIn(true);
    setUserRole(role);
    setCurrentPage("home");

    // Load user data and certification status
    try {
      const { authApi } = await import("./api/auth");
      const user = await authApi.getCurrentUser();
      setIsCertified(user.is_certified || false);

      if (user.is_certified) {
        setCertificationProgress(100);
      } else {
        try {
          const { certificationApi } = await import("./api/certification");
          const progress = await certificationApi.getProgress();
          setCertificationProgress(progress.overall_progress || 0);
        } catch (error) {
          setCertificationProgress(0);
        }
      }
    } catch (error) {
      console.error("Error loading user data:", error);
    }

    toast.success(`Berhasil login sebagai ${role}`);
  };

  const handleRegister = async (role: string) => {
    setIsLoggedIn(true);
    setUserRole(role);
    setCurrentPage("home");

    // Load user data
    try {
      const { authApi } = await import("./api/auth");
      const user = await authApi.getCurrentUser();
      setIsCertified(user.is_certified || false);
      setCertificationProgress(0); // New user, no progress yet
    } catch (error) {
      console.error("Error loading user data:", error);
    }

    toast.success(`Akun berhasil dibuat sebagai ${role}`);
  };

  const handleLogout = async () => {
    try {
      const { authApi } = await import("./api/auth");
      await authApi.logout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setIsLoggedIn(false);
      setUserRole("");
      setIsCertified(false);
      setCertificationProgress(0);
      setCurrentPage("home");
      toast.info("Anda telah logout");
    }
  };

  const handleCompleteCertification = async () => {
    // This will be handled by Certification component
    // Just update local state when certification is completed
    setIsCertified(true);
    setCertificationProgress(100);

    // Reload user data to get updated certification status
    try {
      const { authApi } = await import("./api/auth");
      const user = await authApi.getCurrentUser();
      setIsCertified(user.is_certified || false);
    } catch (error) {
      console.error("Error reloading user data:", error);
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case "home":
        return <Hero setCurrentPage={setCurrentPage} />;
      case "certification":
        return (
          <Certification
            isCertified={isCertified}
            certificationProgress={certificationProgress}
            onCompleteCertification={handleCompleteCertification}
            setCurrentPage={setCurrentPage}
          />
        );
      case "products":
        return (
          <Products isCertified={isCertified} setCurrentPage={setCurrentPage} />
        );
      case "rent":
        return <RentRobot />;
      case "control":
        // Only admin and operator can access robot control
        if (!isLoggedIn || (userRole !== "admin" && userRole !== "operator")) {
          toast.error("Akses ditolak. Hanya Admin dan Operator yang dapat mengakses kontrol robot.");
          setCurrentPage("home");
          return <Hero setCurrentPage={setCurrentPage} />;
        }
        return <RobotControl />;
      case "dashboard":
        // Only admin can access dashboard
        if (!isLoggedIn || userRole !== "admin") {
          toast.error("Akses ditolak. Hanya Admin yang dapat mengakses dashboard.");
          setCurrentPage("home");
          return <Hero setCurrentPage={setCurrentPage} />;
        }
        return <Dashboard userRole={userRole} />;
      case "login":
        return <Login onLogin={handleLogin} setCurrentPage={setCurrentPage} />;
      case "register":
        return (
          <Register
            onRegister={handleRegister}
            setCurrentPage={setCurrentPage}
          />
        );
      case "technology":
        return <Technology />;
      default:
        return <Hero setCurrentPage={setCurrentPage} />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Memuat...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navbar
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        isLoggedIn={isLoggedIn}
        userRole={userRole}
        onLogout={handleLogout}
      />

      <main>{renderPage()}</main>

      {currentPage !== "login" && currentPage !== "register" && (
        <Footer setCurrentPage={setCurrentPage} />
      )}

      <Toaster position="top-right" richColors />
    </div>
  );
}
