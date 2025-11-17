import React from 'react';
import { Button } from './ui/button';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Waves, Brain, Gauge, Radio } from 'lucide-react';

interface HeroProps {
  setCurrentPage: (page: string) => void;
}

export function Hero({ setCurrentPage }: HeroProps) {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-screen flex items-center justify-center overflow-hidden">
        {/* Background Image */}
        <div className="absolute inset-0 z-0">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1660846477676-49d7e2cc6f66?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvY2VhbiUyMHJvYm90aWNzJTIwdGVjaG5vbG9neXxlbnwxfHx8fDE3NjIzMTY3ODV8MA&ixlib=rb-4.1.0&q=80&w=1080"
            alt="Ocean Robotics"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/70 via-background/50 to-background/90" />
        </div>

        {/* Hero Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl lg:text-7xl mb-6 text-foreground">
            Teknologi Otonom untuk Laut yang Lebih Bersih
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-muted-foreground max-w-3xl mx-auto">
            Sealen menghadirkan solusi berbasis AI untuk menjaga kebersihan laut dan efisiensi operasional.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              onClick={() => setCurrentPage('technology')}
              className="bg-primary hover:bg-primary/90 text-lg px-8 py-6"
            >
              Pelajari Teknologi Kami
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => setCurrentPage('certification')}
              className="text-lg px-8 py-6 border-2"
            >
              Mulai Sekarang
            </Button>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-primary rounded-full flex justify-center">
            <div className="w-1 h-3 bg-primary rounded-full mt-2" />
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<Brain className="h-12 w-12 text-primary" />}
            title="Pembersihan Cerdas"
            description="Navigasi AI yang dapat mendeteksi dan mengumpulkan sampah laut secara otomatis dengan efisiensi tinggi."
          />
          <FeatureCard
            icon={<Gauge className="h-12 w-12 text-accent" />}
            title="Monitoring Lingkungan"
            description="Sensor canggih untuk memantau kualitas air, pH, suhu, dan parameter lingkungan lainnya secara real-time."
          />
          <FeatureCard
            icon={<Radio className="h-12 w-12 text-chart-3" />}
            title="Kontrol Jarak Jauh"
            description="Sistem kontrol berbasis cloud yang memungkinkan operator mengawasi dan mengendalikan robot dari mana saja."
          />
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary/5 dark:bg-primary/10 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl mb-4">
            Siap Menjadi Operator Bersertifikat?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Dapatkan akses penuh ke teknologi Sealen dengan menyelesaikan program sertifikasi kami.
          </p>
          <Button
            size="lg"
            onClick={() => setCurrentPage('certification')}
            className="bg-primary hover:bg-primary/90 text-lg px-8"
          >
            Daftar Sertifikasi
          </Button>
        </div>
      </div>
    </div>
  );
}

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="bg-card border border-border rounded-xl p-8 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
      <div className="mb-4">{icon}</div>
      <h3 className="text-2xl mb-3">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </div>
  );
}
