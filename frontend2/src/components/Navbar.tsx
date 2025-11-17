import React, { useState } from 'react';
import { Menu, X, Sun, Moon, Waves } from 'lucide-react';
import { Button } from './ui/button';

interface NavbarProps {
  darkMode: boolean;
  setDarkMode: (value: boolean) => void;
  currentPage: string;
  setCurrentPage: (page: string) => void;
  isLoggedIn: boolean;
  userRole: string;
  onLogout: () => void;
}

export function Navbar({ darkMode, setDarkMode, currentPage, setCurrentPage, isLoggedIn, userRole, onLogout }: NavbarProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const menuItems = [
    { name: 'Beranda', page: 'home' },
    { name: 'Produk', page: 'products' },
    { name: 'Teknologi', page: 'technology' },
    { name: 'Sertifikasi', page: 'certification' },
    { name: 'Sewa Robot', page: 'rent' },
  ];

  // Add role-based menu items
  if (isLoggedIn) {
    // Admin and Operator can access Robot Control
    if (userRole === 'admin' || userRole === 'operator') {
      menuItems.push({ name: 'Kontrol Robot', page: 'control' });
    }

    // Only Admin can access Dashboard
    if (userRole === 'admin') {
      menuItems.push({ name: 'Dashboard', page: 'dashboard' });
    }
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-2 cursor-pointer"
            onClick={() => setCurrentPage('home')}
          >
            <Waves className="h-8 w-8 text-primary" />
            <span className="text-xl font-semibold text-foreground">Sealen</span>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-6">
            {menuItems.map((item) => (
              <button
                key={item.page}
                onClick={() => setCurrentPage(item.page)}
                className={`transition-colors ${
                  currentPage === item.page
                    ? 'text-primary'
                    : 'text-foreground hover:text-primary'
                }`}
              >
                {item.name}
              </button>
            ))}
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-3">
            {/* Dark Mode Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setDarkMode(!darkMode)}
              className="rounded-full"
            >
              {darkMode ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>

            {/* Login/Profile */}
            {isLoggedIn ? (
              <div className="hidden md:flex items-center gap-2">
                <span className="text-sm text-muted-foreground">{userRole}</span>
                <Button variant="outline" size="sm" onClick={onLogout}>
                  Logout
                </Button>
              </div>
            ) : (
              <Button
                onClick={() => setCurrentPage('login')}
                className="hidden md:inline-flex bg-primary hover:bg-primary/90"
              >
                Login / Register
              </Button>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X /> : <Menu />}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-card border-t border-border">
          <div className="px-4 py-3 space-y-2">
            {menuItems.map((item) => (
              <button
                key={item.page}
                onClick={() => {
                  setCurrentPage(item.page);
                  setMobileMenuOpen(false);
                }}
                className={`block w-full text-left px-4 py-2 rounded-lg transition-colors ${
                  currentPage === item.page
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-secondary'
                }`}
              >
                {item.name}
              </button>
            ))}
            {!isLoggedIn && (
              <Button
                onClick={() => {
                  setCurrentPage('login');
                  setMobileMenuOpen(false);
                }}
                className="w-full bg-primary hover:bg-primary/90"
              >
                Login / Register
              </Button>
            )}
            {isLoggedIn && (
              <Button
                variant="outline"
                onClick={() => {
                  onLogout();
                  setMobileMenuOpen(false);
                }}
                className="w-full"
              >
                Logout
              </Button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
