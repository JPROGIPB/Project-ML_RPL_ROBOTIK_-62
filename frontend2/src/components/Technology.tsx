import React from 'react';
import { Card } from './ui/card';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Brain, Cpu, Wifi, Camera, Database, Zap } from 'lucide-react';

export function Technology() {
  const technologies = [
    {
      icon: <Brain className="h-12 w-12" />,
      title: 'AI & Machine Learning',
      description: 'Algoritma pembelajaran mendalam untuk deteksi dan klasifikasi sampah laut secara real-time',
      details: [
        'Convolutional Neural Networks untuk object detection',
        'Reinforcement Learning untuk optimasi rute',
        'Transfer learning dari dataset laut global'
      ],
      color: 'primary'
    },
    {
      icon: <Cpu className="h-12 w-12" />,
      title: 'Autonomous Navigation',
      description: 'Sistem navigasi otonom dengan sensor multi-spektrum dan path planning cerdas',
      details: [
        'GPS dan IMU sensor fusion',
        'Obstacle avoidance dengan sonar',
        'Dynamic path replanning'
      ],
      color: 'accent'
    },
    {
      icon: <Camera className="h-12 w-12" />,
      title: 'Computer Vision',
      description: 'Kamera underwater berkualitas tinggi dengan pemrosesan gambar real-time',
      details: [
        '4K underwater camera',
        'Low-light enhancement',
        'Multi-object tracking'
      ],
      color: 'chart-3'
    },
    {
      icon: <Database className="h-12 w-12" />,
      title: 'Cloud Analytics',
      description: 'Platform berbasis cloud untuk monitoring, analitik, dan pelaporan data operasional',
      details: [
        'Real-time data streaming',
        'Predictive maintenance',
        'Environmental impact reports'
      ],
      color: 'chart-1'
    },
    {
      icon: <Wifi className="h-12 w-12" />,
      title: 'IoT Connectivity',
      description: 'Konektivitas 4G/5G dan komunikasi satelit untuk kontrol jarak jauh',
      details: [
        '4G LTE connectivity',
        'Satellite backup',
        'Mesh networking antar robot'
      ],
      color: 'chart-2'
    },
    {
      icon: <Zap className="h-12 w-12" />,
      title: 'Energy Management',
      description: 'Sistem manajemen energi pintar dengan optimasi konsumsi daya',
      details: [
        'Lithium-ion battery packs',
        'Solar charging compatibility',
        'Adaptive power modes'
      ],
      color: 'chart-5'
    }
  ];

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl mb-4">
            Teknologi Sealen
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Kombinasi AI, Robotika, dan IoT untuk solusi pembersihan laut yang revolusioner
          </p>
        </div>

        <div className="relative h-96 rounded-2xl overflow-hidden mb-16">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1758411897888-3ca658535fdf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNobm9sb2d5JTIwZGFzaGJvYXJkfGVufDF8fHx8MTc2MjI0NjcwNnww&ixlib=rb-4.1.0&q=80&w=1080"
            alt="Technology Dashboard"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent flex items-end p-8">
            <div className="max-w-2xl">
              <h2 className="text-3xl mb-3">Robot Pembersih Laut Berbasis AI</h2>
              <p className="text-muted-foreground">
                Teknologi canggih yang menggabungkan kecerdasan buatan, pembelajaran mesin, 
                dan sistem otonom untuk membersihkan laut secara efisien dan berkelanjutan.
              </p>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {technologies.map((tech, index) => (
            <Card key={index} className="p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
              <div className={`inline-flex p-4 rounded-xl bg-${tech.color}/10 mb-4`}>
                <div className={`text-${tech.color}`}>{tech.icon}</div>
              </div>
              <h3 className="text-xl mb-3">{tech.title}</h3>
              <p className="text-muted-foreground mb-4">{tech.description}</p>
              <ul className="space-y-2">
                {tech.details.map((detail, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm">
                    <div className={`w-1.5 h-1.5 rounded-full bg-${tech.color} mt-1.5 flex-shrink-0`} />
                    <span>{detail}</span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>

        <Card className="p-8 md:p-12 bg-gradient-to-br from-primary/5 to-accent/5">
          <h2 className="text-3xl mb-8 text-center">Spesifikasi Teknis</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <SpecItem label="Kapasitas Sampah" value="100L" description="Per siklus operasi" />
            <SpecItem label="Durasi Baterai" value="8 jam" description="Operasi penuh" />
            <SpecItem label="Kecepatan Maksimal" value="5 knot" description="Dalam air tenang" />
            <SpecItem label="Jangkauan GPS" value="±2m" description="Akurasi posisi" />
            <SpecItem label="Kedalaman Operasi" value="0-5m" description="Di bawah permukaan" />
            <SpecItem label="Akurasi AI" value="95%" description="Deteksi sampah" />
            <SpecItem label="Konektivitas" value="4G/5G" description="+ Satellite backup" />
            <SpecItem label="Berat Robot" value="85kg" description="Termasuk baterai" />
          </div>
        </Card>

        <div className="mt-16">
          <h2 className="text-3xl mb-8 text-center">Cara Kerja</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <ProcessStep
              number="1"
              title="Scan & Detect"
              description="Kamera AI mendeteksi sampah laut dan mengklasifikasikan jenisnya"
            />
            <ProcessStep
              number="2"
              title="Navigate"
              description="Sistem navigasi otonom merencanakan rute optimal untuk pengumpulan"
            />
            <ProcessStep
              number="3"
              title="Collect"
              description="Mekanisme pengumpulan mengambil sampah dan menyimpannya di kontainer"
            />
            <ProcessStep
              number="4"
              title="Report"
              description="Data operasi dan dampak lingkungan dikirim ke cloud untuk analisis"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

interface SpecItemProps {
  label: string;
  value: string;
  description: string;
}

function SpecItem({ label, value, description }: SpecItemProps) {
  return (
    <div className="text-center">
      <div className="text-3xl md:text-4xl text-primary mb-2">{value}</div>
      <div className="text-sm mb-1">{label}</div>
      <div className="text-xs text-muted-foreground">{description}</div>
    </div>
  );
}

interface ProcessStepProps {
  number: string;
  title: string;
  description: string;
}

function ProcessStep({ number, title, description }: ProcessStepProps) {
  return (
    <div className="relative">
      <div className="text-center">
        <div className="w-16 h-16 rounded-full bg-primary/10 text-primary flex items-center justify-center text-2xl mx-auto mb-4">
          {number}
        </div>
        <h4 className="text-lg mb-2">{title}</h4>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
      {number !== "4" && (
        <div className="hidden md:block absolute top-8 left-full w-full h-0.5 bg-border -z-10" />
      )}
    </div>
  );
}
