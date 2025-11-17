# 🌊 SEALEN - Robot Pembersih Laut Otomatis

Platform manajemen dan monitoring robot pembersih laut berbasis AI dengan sistem sertifikasi operator, rental, dan e-commerce.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

---

## 📋 Daftar Isi

- [Tentang Proyek](#-tentang-proyek)
- [Fitur Utama](#-fitur-utama)
- [Teknologi](#-teknologi)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Konfigurasi Database](#-konfigurasi-database)
- [Menjalankan Aplikasi](#-menjalankan-aplikasi)
- [Kredensial Default](#-kredensial-default)
- [Struktur Proyek](#-struktur-proyek)
- [API Documentation](#-api-documentation)
- [Role & Permissions](#-role--permissions)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---

## 🎯 Tentang Proyek

SEALEN adalah platform manajemen robot pembersih laut yang mengintegrasikan teknologi AI dan IoT untuk monitoring real-time, kontrol robot, sistem sertifikasi operator, rental, dan e-commerce produk robot.

### Tujuan
- Memudahkan monitoring dan kontrol robot pembersih laut
- Menyediakan sistem sertifikasi untuk operator
- Memfasilitasi rental dan pembelian robot
- Tracking kinerja dan analitik real-time

---

## ✨ Fitur Utama

### 🔐 Autentikasi & Otorisasi
- Login/Register dengan role-based access control
- JWT Authentication
- 3 Level Role: Admin, Operator, Customer

### 📊 Dashboard
- **Admin**: Monitoring semua robot, analytics, bookings
- **Operator**: Kontrol robot, mission tracking
- **Customer**: Status rental, certification progress

### 🎓 Sistem Sertifikasi
- 4 Modul training interaktif
- Progress tracking
- Certificate generation
- Diperlukan untuk pembelian produk

### 🤖 Manajemen Robot
- Real-time monitoring status robot
- Control panel (Start/Stop/Manual)
- Battery & sensor monitoring
- Mission tracking

### 🛒 E-Commerce
- Katalog produk (Robot, Aksesori, Spare Parts)
- Shopping cart & checkout
- Payment integration (Midtrans simulation)
- Order history

### 💼 Rental System
- Sewa robot tanpa sertifikasi
- Flexible duration (harian, mingguan, bulanan)
- Diskon jangka panjang (10-30%)
- Rental history tracking

### 📈 Analytics & Reporting
- Performance metrics
- Area cleaned tracking
- Energy efficiency monitoring
- Water quality analysis

---

## 🛠 Teknologi

### Backend
- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 3.1.1
- **Authentication**: Flask-JWT-Extended
- **Real-time**: Flask-SocketIO
- **Migrations**: Alembic

### Frontend
- **Framework**: React 18.2
- **Language**: TypeScript
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **State Management**: React Hooks
- **HTTP Client**: Axios

---

## 📦 Prasyarat

Pastikan sistem Anda sudah terinstall:

- **Python** 3.11 atau lebih tinggi
- **Node.js** 18.x atau lebih tinggi
- **PostgreSQL** 14 atau lebih tinggi
- **Git**
- **pip** (Python package manager)
- **npm** atau **yarn**

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd "aduhai"
```

### 2. Setup Backend

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Frontend

```bash
# Buka terminal baru, masuk ke folder frontend
cd frontend

# Install dependencies
npm install
# atau jika menggunakan yarn
yarn install
```

---

## 🗄 Konfigurasi Database

### 1. Buat Database PostgreSQL

```bash
# Login ke PostgreSQL
psql -U postgres

# Buat database
CREATE DATABASE sealen_db;

# Keluar dari psql
\q
```

### 2. Konfigurasi Environment Variables

Buat file `.env` di folder `backend/`:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/sealen_db

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# CORS Configuration
CORS_ORIGINS=http://localhost:5173
```

**⚠️ Ganti `your_password` dengan password PostgreSQL Anda!**

### 3. Inisialisasi Database

```bash
# Masuk ke folder backend (jika belum)
cd backend

# Aktifkan virtual environment
venv\Scripts\activate

# Buat semua tabel
python init_db.py

# Seed data awal (users, robots, products, dll)
python seed_data.py
```

**Output yang diharapkan**:
```
Creating roles...
Creating permissions...
Creating certification modules...
Creating sample products...
Creating sample robots...
Creating demo users...
Seed data created successfully!
```

### 4. Verifikasi Database (Opsional)

```bash
# Cek struktur dan data database
python check_db.py

# Test JWT token generation (jika ada masalah autentikasi)
python debug_jwt.py

# Test API endpoints (pastikan server running)
python test_endpoints.py
```

---

## 🎮 Menjalankan Aplikasi

### 1. Jalankan Backend Server

```bash
# Di folder backend dengan venv aktif
python run.py
```

**Server akan berjalan di**: `http://localhost:5010`

### 2. Jalankan Frontend Development Server

```bash
# Buka terminal baru, masuk ke folder frontend
cd frontend

# Jalankan dev server
npm run dev
# atau
yarn dev
```

**Aplikasi akan berjalan di**: `http://localhost:5173`

### 3. Akses Aplikasi

Buka browser dan akses: `http://localhost:5173`

---

## 🔑 Kredensial Default

### Admin
```
Email: admin@sealen.com
Password: admin123
```
**Akses**: Dashboard, Manajemen Robot, Analytics, Semua Bookings

### Operator
```
Email: operator@sealen.com
Password: operator123
```
**Akses**: Dashboard, Kontrol Robot, Mission Tracking

### Customer
```
Email: customer@sealen.com
Password: customer123
```
**Akses**: Produk, Rental, Sertifikasi, Booking History

---

## 📁 Struktur Proyek

```
aduhai/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration
│   │   ├── models/              # Database models
│   │   │   ├── user.py
│   │   │   ├── robot.py
│   │   │   ├── product.py
│   │   │   ├── booking.py
│   │   │   ├── certificate.py
│   │   │   └── mission.py
│   │   ├── routes/              # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── robots.py
│   │   │   ├── products.py
│   │   │   ├── bookings.py
│   │   │   ├── certification.py
│   │   │   └── dashboard.py
│   │   └── utils/               # Utilities
│   │       └── auth.py
│   ├── instance/                # SQLite database (fallback)
│   ├── migrations/              # Alembic migrations
│   ├── venv/                    # Virtual environment
│   ├── .env                     # Environment variables
│   ├── run.py                   # Application entry point
│   ├── init_db.py              # Database initialization
│   ├── seed_data.py            # Seed data script
│   ├── check_db.py             # Database verification utility
│   ├── debug_jwt.py            # JWT debugging utility
│   ├── test_endpoints.py       # API testing utility
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Products.tsx
│   │   │   ├── RentRobot.tsx
│   │   │   ├── Certification.tsx
│   │   │   └── ui/             # shadcn/ui components
│   │   ├── api/                # API client
│   │   │   ├── client.ts
│   │   │   ├── auth.ts
│   │   │   ├── robot.ts
│   │   │   ├── product.ts
│   │   │   └── booking.ts
│   │   ├── App.tsx             # Main app component
│   │   └── main.tsx            # Entry point
│   ├── public/                 # Static assets
│   ├── package.json            # Dependencies
│   └── vite.config.ts          # Vite configuration
│
└── README.md                    # Documentation
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:5010/api
```

### Authentication Endpoints

#### POST `/auth/register`
Register user baru
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "role": "customer"
}
```

#### POST `/auth/login`
Login user
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### GET `/auth/me`
Get current user info (requires JWT)

### Robot Endpoints

#### GET `/robots`
Get list robots
- Query: `?for_rental=true` - Filter robots for rental

#### GET `/robots/<id>`
Get robot details

#### POST `/robots/<id>/control/start`
Start robot (Admin/Operator only)

#### POST `/robots/<id>/control/stop`
Stop robot (Admin/Operator only)

### Product Endpoints

#### GET `/products`
Get product catalog
- Query: `?category=Robot` - Filter by category

#### GET `/products/<id>`
Get product details

### Booking Endpoints

#### GET `/bookings`
Get user bookings
- Query: `?status=rental` - Filter by status

#### POST `/bookings`
Create booking (rental or purchase)
```json
{
  "booking_type": "rental",
  "robot_id": 1,
  "start_date": "2024-01-01T00:00:00Z",
  "duration_days": 30,
  "location": "Jakarta Bay"
}
```

#### POST `/bookings/<id>/payment`
Create payment
```json
{
  "method": "credit-card"
}
```

### Certification Endpoints

#### GET `/certification/modules`
Get certification modules

#### GET `/certification/progress`
Get user progress (requires JWT)

#### POST `/certification/progress/<module_id>`
Update progress
```json
{
  "progress_percentage": 100,
  "completed": true
}
```

### Dashboard Endpoints (Admin Only)

#### GET `/dashboard/overview`
Get dashboard metrics

#### GET `/dashboard/robots/status`
Get all robots status

#### GET `/dashboard/bookings`
Get all bookings (all users)

---

## 👥 Role & Permissions

### Admin
- ✅ Akses penuh ke semua fitur
- ✅ Manage users, robots, products
- ✅ View all bookings & analytics
- ✅ Control semua robots

### Operator
- ✅ View & control robots
- ✅ Manage missions
- ✅ View own bookings
- ❌ Cannot manage users/products

### Customer
- ✅ View products & robots
- ✅ Create bookings (rental/purchase)
- ✅ Complete certification
- ✅ View own data only
- ❌ Cannot control robots

---

## 🧪 Testing

### Test Database Connection
```bash
cd backend
python -c "from app import create_app, db; from app.config import Config; app = create_app(Config); app.app_context().push(); db.engine.connect(); print('✅ Database connected!')"
```

### Test JWT Token
```bash
cd backend
python debug_jwt.py
```

### Test API Endpoints
```bash
cd backend
python test_endpoints.py
```

### Manual Testing Flow

**1. Test Registration & Login**
- Register user baru
- Login dengan kredensial
- Verify JWT token tersimpan

**2. Test Certification**
- Login sebagai customer
- Complete 4 modul sertifikasi
- Verify certificate generated

**3. Test Product Purchase**
- Browse products
- Add to cart
- Complete checkout
- Verify booking created

**4. Test Robot Rental**
- Select available robot
- Choose duration
- Complete payment
- Verify rental record

**5. Test Admin Dashboard**
- Login sebagai admin
- View all bookings
- Monitor robot status
- Check analytics

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flask_sqlalchemy'"
**Solusi**: Virtual environment belum aktif
```bash
cd backend
venv\Scripts\activate
```

### Error: "Invalid token" atau "422 Unprocessable Entity"
**Solusi**: Logout dan login ulang untuk mendapat token baru
```
Masalah: Token lama menggunakan integer identity
Fix: Token baru menggunakan string identity
```

### Error: "Connection refused" pada port 5010
**Solusi**: Backend server belum running
```bash
cd backend
python run.py
```

### Error: "CORS policy" di browser
**Solusi**: Pastikan CORS_ORIGINS di `.env` sesuai
```env
CORS_ORIGINS=http://localhost:5173
```

### Database connection error
**Solusi**:
1. Pastikan PostgreSQL running
2. Check kredensial di `.env`
3. Database `sealen_db` sudah dibuat

### Frontend cannot connect to backend
**Solusi**: Check `frontend/src/api/client.ts`
```typescript
baseURL: 'http://localhost:5010/api'
```

---

## 📝 Catatan Penting

### Development
- Backend berjalan di port `5010`
- Frontend berjalan di port `5173`
- Database PostgreSQL di port `5432`

### Production Deployment
Untuk production, perlu:
1. Ganti `SECRET_KEY` dan `JWT_SECRET_KEY` dengan nilai random yang aman
2. Set `FLASK_ENV=production`
3. Gunakan production-ready server (Gunicorn, uWSGI)
4. Setup HTTPS/SSL
5. Configure proper CORS
6. Integrate real Midtrans Payment Gateway
7. Setup automated backups untuk database

### Security
- ⚠️ Jangan commit file `.env` ke repository
- ⚠️ Ganti semua secret keys di production
- ⚠️ Gunakan strong passwords
- ⚠️ Enable rate limiting untuk API
- ⚠️ Setup proper firewall rules

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Untuk berkontribusi:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

---

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Kontak & Support

Untuk pertanyaan atau dukungan, silakan hubungi:
- Email: support@sealen.com
- Website: https://sealen.com

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [React](https://react.dev/)
- [shadcn/ui](https://ui.shadcn.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Dibuat dengan ❤️ untuk lingkungan laut yang lebih bersih** 🌊
