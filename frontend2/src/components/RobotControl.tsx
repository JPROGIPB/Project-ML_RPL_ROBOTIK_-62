import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Slider } from './ui/slider';
import { 
  ArrowUp, ArrowDown, ArrowLeft, ArrowRight, 
  Circle, AlertTriangle, Gauge, 
  Battery, MapPin, Thermometer, Droplets,
  Play, Pause, RotateCcw
} from 'lucide-react';

interface RobotStatus {
  connected: boolean;
  battery: number;
  latitude: number;
  longitude: number;
  temperature: number;
  pH: number;
  depth: number;
  speed: number;
}

export function RobotControl() {
  const [robotStatus, setRobotStatus] = useState<RobotStatus>({
    connected: true,
    battery: 78,
    latitude: -6.2088,
    longitude: 106.8456,
    temperature: 28,
    pH: 7.2,
    depth: 2.5,
    speed: 0
  });

  const [mode, setMode] = useState<'manual' | 'auto'>('manual');
  const [isRunning, setIsRunning] = useState(false);

  const handleDirectionControl = (direction: string) => {
    console.log(`Moving ${direction}`);
  };

  const handleEmergencyStop = () => {
    setIsRunning(false);
    console.log('Emergency stop activated!');
  };

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-4xl mb-2">Kontrol Robot</h1>
            <p className="text-muted-foreground">Sealen CleanBot #CB-001</p>
          </div>
          <div className="flex gap-3">
            <Badge className={robotStatus.connected ? 'bg-accent' : 'bg-destructive'}>
              {robotStatus.connected ? '● Terhubung' : '● Terputus'}
            </Badge>
            <Button
              variant="outline"
              onClick={() => setMode(mode === 'manual' ? 'auto' : 'manual')}
            >
              Mode: {mode === 'manual' ? 'Manual' : 'Auto'}
            </Button>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column - Status Cards */}
          <div className="space-y-6">
            {/* Battery Status */}
            <Card className="p-6">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Battery className="h-5 w-5 text-primary" />
                  <h3>Baterai</h3>
                </div>
                <span className="text-2xl text-primary">{robotStatus.battery}%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-3">
                <div
                  className={`h-3 rounded-full transition-all ${
                    robotStatus.battery > 50
                      ? 'bg-accent'
                      : robotStatus.battery > 20
                      ? 'bg-chart-3'
                      : 'bg-destructive'
                  }`}
                  style={{ width: `${robotStatus.battery}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Estimasi: {Math.floor(robotStatus.battery / 12.5)} jam tersisa
              </p>
            </Card>

            {/* Location */}
            <Card className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <MapPin className="h-5 w-5 text-primary" />
                <h3>Lokasi GPS</h3>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Latitude:</span>
                  <span>{robotStatus.latitude.toFixed(4)}°</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Longitude:</span>
                  <span>{robotStatus.longitude.toFixed(4)}°</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Kedalaman:</span>
                  <span>{robotStatus.depth}m</span>
                </div>
              </div>
            </Card>

            {/* Environmental Sensors */}
            <Card className="p-6">
              <h3 className="mb-4">Sensor Lingkungan</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Thermometer className="h-5 w-5 text-chart-3" />
                    <span>Suhu Air</span>
                  </div>
                  <span>{robotStatus.temperature}°C</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Droplets className="h-5 w-5 text-primary" />
                    <span>pH</span>
                  </div>
                  <span>{robotStatus.pH}</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Gauge className="h-5 w-5 text-accent" />
                    <span>Kecepatan</span>
                  </div>
                  <span>{robotStatus.speed} knot</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Center Column - Control Panel */}
          <div className="space-y-6">
            <Card className="p-8">
              <h3 className="text-center mb-6">Panel Kontrol</h3>
              
              {/* Joystick Controls */}
              <div className="grid grid-cols-3 gap-3 max-w-xs mx-auto mb-6">
                <div></div>
                <Button
                  size="lg"
                  variant="outline"
                  className="aspect-square"
                  onClick={() => handleDirectionControl('up')}
                  disabled={!robotStatus.connected || !isRunning}
                >
                  <ArrowUp className="h-6 w-6" />
                </Button>
                <div></div>

                <Button
                  size="lg"
                  variant="outline"
                  className="aspect-square"
                  onClick={() => handleDirectionControl('left')}
                  disabled={!robotStatus.connected || !isRunning}
                >
                  <ArrowLeft className="h-6 w-6" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="aspect-square"
                  disabled={!robotStatus.connected || !isRunning}
                >
                  <Circle className="h-6 w-6" />
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="aspect-square"
                  onClick={() => handleDirectionControl('right')}
                  disabled={!robotStatus.connected || !isRunning}
                >
                  <ArrowRight className="h-6 w-6" />
                </Button>

                <div></div>
                <Button
                  size="lg"
                  variant="outline"
                  className="aspect-square"
                  onClick={() => handleDirectionControl('down')}
                  disabled={!robotStatus.connected || !isRunning}
                >
                  <ArrowDown className="h-6 w-6" />
                </Button>
                <div></div>
              </div>

              {/* Speed Control */}
              <div className="mb-6">
                <div className="flex justify-between mb-2">
                  <span className="text-sm">Kecepatan</span>
                  <span className="text-sm text-primary">{robotStatus.speed} knot</span>
                </div>
                <Slider
                  value={[robotStatus.speed]}
                  onValueChange={(value) => setRobotStatus({ ...robotStatus, speed: value[0] })}
                  max={5}
                  step={0.5}
                  disabled={!robotStatus.connected || !isRunning}
                />
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-2 gap-3">
                <Button
                  onClick={() => setIsRunning(!isRunning)}
                  className={isRunning ? 'bg-chart-3' : 'bg-accent'}
                  disabled={!robotStatus.connected}
                >
                  {isRunning ? (
                    <>
                      <Pause className="h-4 w-4 mr-2" />
                      Stop
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Start
                    </>
                  )}
                </Button>
                <Button
                  variant="outline"
                  disabled={!robotStatus.connected}
                >
                  <RotateCcw className="h-4 w-4 mr-2" />
                  Calibration
                </Button>
              </div>
            </Card>

            {/* Emergency Stop */}
            <Card className="p-6 bg-destructive/10 border-destructive">
              <Button
                onClick={handleEmergencyStop}
                className="w-full bg-destructive hover:bg-destructive/90 h-16"
                size="lg"
              >
                <AlertTriangle className="h-6 w-6 mr-2" />
                EMERGENCY STOP
              </Button>
              <p className="text-xs text-muted-foreground text-center mt-3">
                Tekan untuk menghentikan semua operasi robot secara darurat
              </p>
            </Card>
          </div>

          {/* Right Column - Map & Analytics */}
          <div className="space-y-6">
            {/* Navigation Map */}
            <Card className="p-6">
              <h3 className="mb-4">Peta Navigasi</h3>
              <div className="aspect-square bg-secondary rounded-lg flex items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-accent/20">
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                    <div className="w-4 h-4 bg-primary rounded-full animate-pulse" />
                    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                      <div className="w-8 h-8 border-2 border-primary rounded-full animate-ping" />
                    </div>
                  </div>
                  <svg className="w-full h-full">
                    <path
                      d="M 20,80 Q 50,20 80,50 T 150,80"
                      stroke="currentColor"
                      strokeWidth="2"
                      fill="none"
                      className="text-primary opacity-50"
                      strokeDasharray="5,5"
                    />
                  </svg>
                </div>
                <div className="absolute bottom-3 left-3 text-xs bg-background/80 px-2 py-1 rounded">
                  Live Tracking
                </div>
              </div>
              <p className="text-xs text-muted-foreground mt-3">
                Area pembersihan: 2.4 km²
              </p>
            </Card>

            {/* Operation Stats */}
            <Card className="p-6">
              <h3 className="mb-4">Statistik Operasi</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-muted-foreground">Waktu Operasi</span>
                    <span>4h 23m</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div className="bg-primary h-2 rounded-full" style={{ width: '54%' }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-muted-foreground">Sampah Terkumpul</span>
                    <span>68 kg</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div className="bg-accent h-2 rounded-full" style={{ width: '68%' }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-muted-foreground">Efisiensi Energi</span>
                    <span>92%</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div className="bg-chart-3 h-2 rounded-full" style={{ width: '92%' }} />
                  </div>
                </div>
              </div>
            </Card>

            {/* System Status */}
            <Card className="p-6">
              <h3 className="mb-4">Status Sistem</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Motor Propeller</span>
                  <Badge className="bg-accent">Normal</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Sistem AI</span>
                  <Badge className="bg-accent">Aktif</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Sensor Array</span>
                  <Badge className="bg-accent">OK</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">GPS Module</span>
                  <Badge className="bg-accent">Connected</Badge>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
