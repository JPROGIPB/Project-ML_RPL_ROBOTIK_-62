import React from 'react';
import { Waves, Linkedin, Youtube, Instagram, Mail, Phone, MapPin } from 'lucide-react';

interface FooterProps {
  setCurrentPage: (page: string) => void;
}

export function Footer({ setCurrentPage }: FooterProps) {
  const quickLinks = [
    { name: 'Beranda', page: 'home' },
    { name: 'Produk', page: 'products' },
    { name: 'Teknologi', page: 'technology' },
    { name: 'Sertifikasi', page: 'certification' }
  ];

  const support = [
    { name: 'FAQ', page: 'home' },
    { name: 'Manual Pengguna', page: 'home' },
    { name: 'Live Chat', page: 'home' },
    { name: 'Feedback', page: 'home' }
  ];

  return (
    <footer className="border-t border-border bg-card">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Waves className="h-8 w-8 text-primary" />
              <span className="text-xl">Sealen</span>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              Smart Robotics for Cleaner Oceans
            </p>
            <p className="text-sm text-muted-foreground">
              Teknologi AI untuk kebersihan laut yang berkelanjutan
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="mb-4">Menu Cepat</h4>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.page}>
                  <button
                    onClick={() => setCurrentPage(link.page)}
                    className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  >
                    {link.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="mb-4">Bantuan</h4>
            <ul className="space-y-2">
              {support.map((item, index) => (
                <li key={index}>
                  <button
                    className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  >
                    {item.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="mb-4">Kontak</h4>
            <ul className="space-y-3">
              <li className="flex items-start gap-2 text-sm text-muted-foreground">
                <Mail className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>info@sealen.com</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-muted-foreground">
                <Phone className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>+62 21 1234 5678</span>
              </li>
              <li className="flex items-start gap-2 text-sm text-muted-foreground">
                <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>Jakarta, Indonesia</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Social Media & Copyright */}
        <div className="pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-muted-foreground">
            © 2025 Sealen Technologies. All rights reserved.
          </p>
          
          {/* Social Icons */}
          <div className="flex gap-4">
            <a
              href="https://linkedin.com"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 rounded-full bg-secondary hover:bg-primary hover:text-primary-foreground flex items-center justify-center transition-all"
            >
              <Linkedin className="h-5 w-5" />
            </a>
            <a
              href="https://youtube.com"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 rounded-full bg-secondary hover:bg-primary hover:text-primary-foreground flex items-center justify-center transition-all"
            >
              <Youtube className="h-5 w-5" />
            </a>
            <a
              href="https://instagram.com"
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 rounded-full bg-secondary hover:bg-primary hover:text-primary-foreground flex items-center justify-center transition-all"
            >
              <Instagram className="h-5 w-5" />
            </a>
          </div>
        </div>
      </div>

      {/* Chatbot */}
      <div className="fixed bottom-6 right-6 z-40">
        <button className="w-14 h-14 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg flex items-center justify-center transition-all hover:scale-110">
          <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </button>
      </div>
    </footer>
  );
}
