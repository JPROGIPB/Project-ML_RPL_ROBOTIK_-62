# Sealen Backend - Flask API

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Database

```bash
# Create PostgreSQL database
createdb sealen_db

# Or using psql:
# psql -U postgres
# CREATE DATABASE sealen_db;
```

### 3. Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://username:password@localhost:5432/sealen_db
```

### 4. Initialize Database

```bash
# Create migrations
flask db init  # First time only
flask db migrate -m "Initial migration"
flask db upgrade

# Seed initial data
python seed_data.py
```

### 5. Run Development Server

```bash
python run.py
```

Server akan berjalan di `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user

### Robots

- `GET /api/robots` - List robots
- `GET /api/robots/{id}` - Get robot details
- `GET /api/robots/{id}/status` - Get robot status
- `POST /api/robots/{id}/control/start` - Start robot
- `POST /api/robots/{id}/control/stop` - Stop robot
- `POST /api/robots/{id}/control/manual` - Manual control

### Products

- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product details

### Bookings

- `GET /api/bookings` - List bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/{id}` - Get booking
- `POST /api/bookings/{id}/payment` - Create payment

### Certification

- `GET /api/certification/modules` - Get modules
- `GET /api/certification/progress` - Get progress
- `POST /api/certification/progress/{id}` - Update progress
- `POST /api/certification/complete` - Complete certification

### Dashboard

- `GET /api/dashboard/overview` - Dashboard overview
- `GET /api/dashboard/robots/status` - Robots status
- `GET /api/dashboard/analytics/performance` - Performance data
- `GET /api/dashboard/activity-log` - Activity log

## Demo Users

Setelah run `seed_data.py`, tersedia demo users:

- **Admin**: `admin@sealen.com` / `admin123`
- **Operator**: `operator@sealen.com` / `operator123`
- **Customer**: `customer@sealen.com` / `customer123`

## Database Models

Semua models ada di `app/models/`:

- User, Role, Permission
- Certificate, CertificationModule
- Product, Robot
- Booking, Payment
- Mission, OperationLog, SensorData, MLDecision
- Waste, Feedback
- AIModel, TrainingData

## Development

```bash
# Run with auto-reload
flask run --debug

# Create new migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade
```

