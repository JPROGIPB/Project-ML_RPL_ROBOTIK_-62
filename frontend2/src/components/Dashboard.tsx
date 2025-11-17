import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Activity, TrendingUp, Zap, Droplets, BarChart3, Settings, Bell, Download, Loader2, ShoppingCart } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { dashboardApi } from '../api/dashboard';
import { bookingApi, Booking } from '../api/booking';
import { toast } from 'sonner';

interface DashboardProps {
  userRole: string;
}

interface DashboardData {
  robots_active: number;
  robots_total: number;
  area_cleaned_today: number;
  waste_collected_today: number;
  energy_efficiency: number;
  water_quality_avg: number;
  recent_activity: any[];
}

interface RobotStatus {
  robot_id: number;
  name: string;
  status: string;
  battery: number;
  area_cleaned: number;
  current_mission: any;
}

export function Dashboard({ userRole }: DashboardProps) {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [robotsStatus, setRobotsStatus] = useState<RobotStatus[]>([]);
  const [performanceData, setPerformanceData] = useState<any[]>([]);
  const [activityLog, setActivityLog] = useState<any[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);

      // Use admin endpoint for bookings if available
      const bookingsPromise = userRole === 'admin'
        ? dashboardApi.getAllBookings().catch(() => [])
        : bookingApi.getBookings().catch(() => []);

      const [overview, robots, performance, activity, bookingsData] = await Promise.all([
        dashboardApi.getOverview(),
        dashboardApi.getRobotsStatus(),
        dashboardApi.getPerformance(),
        dashboardApi.getActivityLog(),
        bookingsPromise,
      ]);

      setDashboardData(overview);
      setRobotsStatus(robots);
      setPerformanceData(performance);
      setActivityLog(activity);
      setBookings(bookingsData);
    } catch (error: any) {
      console.error('Error loading dashboard data:', error);
      toast.error('Gagal memuat data dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 pb-16 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-4xl mb-2">Dashboard</h1>
            <p className="text-muted-foreground">Monitoring & Analytics Robot Sealen</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" size="icon">
              <Bell className="h-4 w-4" />
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Export Data
            </Button>
            <Button variant="outline">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Button>
          </div>
        </div>

        {/* Metrics Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            icon={<Activity className="h-6 w-6" />}
            title="Robot Aktif"
            value={`${dashboardData?.robots_active || 0}/${dashboardData?.robots_total || 0}`}
            change="Hari ini"
            trend="up"
            color="primary"
          />
          <MetricCard
            icon={<BarChart3 className="h-6 w-6" />}
            title="Area Dibersihkan"
            value={`${dashboardData?.area_cleaned_today || 0} km²`}
            change="Hari ini"
            trend="up"
            color="accent"
          />
          <MetricCard
            icon={<Zap className="h-6 w-6" />}
            title="Efisiensi Energi"
            value={`${dashboardData?.energy_efficiency || 0}%`}
            change="Rata-rata"
            trend="up"
            color="chart-3"
          />
          <MetricCard
            icon={<Droplets className="h-6 w-6" />}
            title="Kualitas Air"
            value={`pH ${dashboardData?.water_quality_avg || 0}`}
            change="Normal"
            trend="neutral"
            color="chart-1"
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          {/* Performance Chart */}
          <Card className="lg:col-span-2 p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl">Performa 24 Jam</h2>
              <div className="flex gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-primary rounded-full" />
                  <span className="text-muted-foreground">Area (km²)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-accent rounded-full" />
                  <span className="text-muted-foreground">Energi (%)</span>
                </div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorEnergy" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--color-accent)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--color-accent)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="time" stroke="currentColor" opacity={0.5} />
                <YAxis stroke="currentColor" opacity={0.5} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'var(--color-card)', 
                    border: '1px solid var(--color-border)',
                    borderRadius: '8px'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="area" 
                  stroke="var(--color-primary)" 
                  fillOpacity={1} 
                  fill="url(#colorArea)" 
                />
                <Area 
                  type="monotone" 
                  dataKey="energy" 
                  stroke="var(--color-accent)" 
                  fillOpacity={1} 
                  fill="url(#colorEnergy)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          {/* Activity Log */}
          <Card className="p-6">
            <h2 className="text-xl mb-6">Log Aktivitas</h2>
            <div className="space-y-4">
              {activityLog.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-8">
                  Belum ada aktivitas
                </p>
              ) : (
                activityLog.map((log) => (
                  <div key={log.id} className="flex gap-3">
                    <div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${
                      log.status === 'success' ? 'bg-accent' :
                      log.status === 'warning' ? 'bg-chart-3' :
                      'bg-primary'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm">{log.activity}</p>
                      <p className="text-xs text-muted-foreground">{log.time}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </Card>
        </div>

        {/* Robot Status Table */}
        <Card className="p-6 mb-8">
          <h2 className="text-xl mb-6">Status Robot</h2>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID Robot</TableHead>
                  <TableHead>Nama</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Baterai</TableHead>
                  <TableHead>Area Dibersihkan (km²)</TableHead>
                  <TableHead className="text-right">Aksi</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {robotsStatus.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                      Tidak ada robot tersedia
                    </TableCell>
                  </TableRow>
                ) : (
                  robotsStatus.map((robot) => (
                    <TableRow key={robot.robot_id}>
                      <TableCell className="font-mono">#{robot.robot_id}</TableCell>
                      <TableCell>{robot.name}</TableCell>
                      <TableCell>
                        <Badge className={robot.status === 'active' ? 'bg-accent' : 'bg-chart-3'}>
                          {robot.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <div className="w-20 h-2 bg-secondary rounded-full overflow-hidden">
                            <div
                              className={`h-full ${
                                robot.battery > 50 ? 'bg-accent' :
                                robot.battery > 20 ? 'bg-chart-3' :
                                'bg-destructive'
                              }`}
                              style={{ width: `${robot.battery}%` }}
                            />
                          </div>
                          <span className="text-sm">{robot.battery}%</span>
                        </div>
                      </TableCell>
                      <TableCell>{robot.area_cleaned.toFixed(1)}</TableCell>
                      <TableCell className="text-right">
                        <Button size="sm" variant="outline">
                          Detail
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </Card>

        {/* Booking / Rental Table */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl">Riwayat Booking & Sewa</h2>
            <ShoppingCart className="h-5 w-5 text-muted-foreground" />
          </div>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Tipe</TableHead>
                  <TableHead>Robot/Produk</TableHead>
                  <TableHead>Tanggal Mulai</TableHead>
                  <TableHead>Durasi</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Total</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {bookings.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} className="text-center text-muted-foreground py-8">
                      Belum ada booking
                    </TableCell>
                  </TableRow>
                ) : (
                  bookings.slice(0, 10).map((booking) => (
                    <TableRow key={booking.booking_id}>
                      <TableCell className="font-mono">#{booking.booking_id}</TableCell>
                      <TableCell>
                        <Badge variant={booking.booking_type === 'rental' ? 'default' : 'secondary'}>
                          {booking.booking_type === 'rental' ? 'Sewa' : 'Beli'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {booking.robot_id ? `Robot #${booking.robot_id}` : `Produk #${booking.product_id}`}
                      </TableCell>
                      <TableCell>
                        {new Date(booking.start_date).toLocaleDateString('id-ID')}
                      </TableCell>
                      <TableCell>
                        {booking.duration_days ? `${booking.duration_days} hari` : '-'}
                      </TableCell>
                      <TableCell>
                        <Badge className={
                          booking.status === 'confirmed' ? 'bg-accent' :
                          booking.status === 'pending' ? 'bg-chart-3' :
                          'bg-muted'
                        }>
                          {booking.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        {formatPrice(booking.total_cost)}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </Card>
      </div>
    </div>
  );
}

interface MetricCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  change: string;
  trend: string;
  color: string;
}

function MetricCard({ icon, title, value, change, trend, color }: MetricCardProps) {
  return (
    <Card className="p-6">
      <div className="flex items-start justify-between mb-3">
        <div className={`p-3 rounded-lg bg-${color}/10`}>
          <div className={`text-${color}`}>{icon}</div>
        </div>
        {trend === 'up' && (
          <TrendingUp className="h-4 w-4 text-accent" />
        )}
      </div>
      <p className="text-muted-foreground text-sm mb-1">{title}</p>
      <p className="text-2xl mb-2">{value}</p>
      <p className="text-xs text-muted-foreground">{change}</p>
    </Card>
  );
}
