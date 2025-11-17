-- =====================================================
-- Sealen Database Schema - Final Version
-- Menggabungkan ERD yang ada dengan kebutuhan Frontend
-- =====================================================

-- =====================================================
-- 1. USER MANAGEMENT & ACCESS CONTROL
-- =====================================================

-- Permission Table
CREATE TABLE permission (
    perm_id SERIAL PRIMARY KEY,
    perm_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Role Table
CREATE TABLE role (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Role Permission Junction Table
CREATE TABLE role_permission (
    role_id INTEGER REFERENCES role(role_id) ON DELETE CASCADE,
    perm_id INTEGER REFERENCES permission(perm_id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, perm_id)
);

-- User Table (disesuaikan dengan ERD + kebutuhan frontend)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Hashed password
    full_name VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES role(role_id),
    is_certified BOOLEAN DEFAULT FALSE,  -- Quick check flag
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_user_email (email),
    INDEX idx_user_role (role_id)
);

-- Certificate Table
CREATE TABLE certificate (
    cert_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    cert_type VARCHAR(100) NOT NULL,
    issued_date TIMESTAMP NOT NULL,
    expiry_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',  -- 'active', 'expired', 'revoked'
    cert_number VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_cert_user (user_id),
    INDEX idx_cert_status (status)
);

-- Certification Module Table (NEW - untuk frontend certification component)
CREATE TABLE certification_module (
    id SERIAL PRIMARY KEY,
    module_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    duration_minutes INTEGER,
    description TEXT,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(module_number)
);

-- User Certification Progress (NEW - untuk track progress)
CREATE TABLE user_certification_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    module_id INTEGER REFERENCES certification_module(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, module_id),
    INDEX idx_progress_user (user_id)
);

-- =====================================================
-- 2. PRODUCT CATALOG (NEW - untuk frontend Products component)
-- =====================================================

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,  -- 'Robot', 'Aksesori', 'Spare Part'
    price DECIMAL(15, 2) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    features JSONB,  -- Array of feature strings
    is_available BOOLEAN DEFAULT TRUE,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_product_category (category),
    INDEX idx_product_available (is_available)
);

-- =====================================================
-- 3. ROBOT MANAGEMENT
-- =====================================================

-- Robot Table (disesuaikan dengan ERD + kebutuhan simulasi)
CREATE TABLE robot (
    robot_id SERIAL PRIMARY KEY,
    robot_name VARCHAR(255) NOT NULL,
    model VARCHAR(100),
    model_type VARCHAR(100),  -- 'CleanBot', 'Vision AI', etc.
    status VARCHAR(50) DEFAULT 'offline',  -- 'active', 'charging', 'maintenance', 'offline'
    battery_lvl INTEGER DEFAULT 100 CHECK (battery_lvl >= 0 AND battery_lvl <= 100),
    location VARCHAR(255),  -- General location description
    current_position JSONB,  -- {latitude, longitude, depth} - NEW
    firmware_version VARCHAR(50),  -- NEW
    owner_id INTEGER REFERENCES users(user_id),  -- NEW - untuk purchased robots
    last_maint TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_robot_status (status),
    INDEX idx_robot_owner (owner_id)
);

-- =====================================================
-- 4. BOOKING & PAYMENT
-- =====================================================

-- Booking Table (disesuaikan untuk rental dan purchase)
CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    robot_id INTEGER REFERENCES robot(robot_id),
    product_id INTEGER REFERENCES product(id),  -- NEW - untuk purchase
    booking_type VARCHAR(50) NOT NULL,  -- 'rental' or 'purchase' - NEW
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,  -- NULL untuk purchase
    duration_days INTEGER,  -- NEW - untuk rental
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'confirmed', 'active', 'completed', 'cancelled'
    total_cost DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_booking_user (user_id),
    INDEX idx_booking_robot (robot_id),
    INDEX idx_booking_status (status),
    INDEX idx_booking_type (booking_type)
);

-- Payment Table
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES booking(booking_id) ON DELETE CASCADE,
    amount DECIMAL(15, 2) NOT NULL,
    method VARCHAR(50) NOT NULL,  -- 'credit-card', 'e-wallet', 'bank-transfer'
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'completed', 'failed', 'refunded'
    paid_at TIMESTAMP,
    transaction_id VARCHAR(255) UNIQUE,  -- Payment gateway transaction ID
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_payment_booking (booking_id),
    INDEX idx_payment_status (status)
);

-- =====================================================
-- 5. MISSION & OPERATIONS
-- =====================================================

-- Mission Table (disesuaikan dengan ERD)
CREATE TABLE mission (
    mission_id SERIAL PRIMARY KEY,
    robot_id INTEGER REFERENCES robot(robot_id) ON DELETE CASCADE,
    operator_id INTEGER REFERENCES users(user_id),  -- User yang menjalankan mission
    ai_model_id INTEGER REFERENCES ai_model(model_id),  -- ML model yang digunakan
    name VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    area_coords JSONB,  -- Changed to JSONB untuk fleksibilitas
    status VARCHAR(50) DEFAULT 'planned',  -- 'planned', 'active', 'completed', 'cancelled'
    area_covered DECIMAL(10, 2) DEFAULT 0,  -- km²
    waste_collected DECIMAL(10, 2) DEFAULT 0,  -- kg
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_mission_robot (robot_id),
    INDEX idx_mission_operator (operator_id),
    INDEX idx_mission_status (status)
);

-- Operation Log Table
CREATE TABLE operation_log (
    log_id SERIAL PRIMARY KEY,
    mission_id INTEGER REFERENCES mission(mission_id) ON DELETE CASCADE,
    robot_id INTEGER REFERENCES robot(robot_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    action_type VARCHAR(100) NOT NULL,  -- 'start', 'stop', 'move', 'collect', etc.
    parameters JSONB,  -- Action parameters
    results JSONB,  -- Action results
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_log_mission (mission_id),
    INDEX idx_log_robot (robot_id),
    INDEX idx_log_timestamp (timestamp)
);

-- Sensor Data Table (NEW - untuk simulated sensor readings)
CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    robot_id INTEGER REFERENCES robot(robot_id) ON DELETE CASCADE,
    mission_id INTEGER REFERENCES mission(mission_id),
    timestamp TIMESTAMP DEFAULT NOW(),
    
    -- GPS Data
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    depth DECIMAL(5, 2),
    
    -- Environmental
    temperature DECIMAL(5, 2),
    ph DECIMAL(4, 2),
    water_quality DECIMAL(5, 2),
    
    -- Robot State
    battery_level INTEGER,
    speed DECIMAL(5, 2),
    
    -- Camera & LIDAR (JSONB untuk fleksibilitas)
    camera_data JSONB,  -- {image_url, detections: [...]}
    lidar_data JSONB,  -- Array of point cloud data
    
    -- Waste Detection
    waste_detected JSONB,  -- {count, items: [...]}
    
    INDEX idx_sensor_robot_timestamp (robot_id, timestamp),
    INDEX idx_sensor_mission_timestamp (mission_id, timestamp)
);

-- ML Decision Table (NEW - untuk ML inference results)
CREATE TABLE ml_decision (
    id SERIAL PRIMARY KEY,
    robot_id INTEGER REFERENCES robot(robot_id) ON DELETE CASCADE,
    mission_id INTEGER REFERENCES mission(mission_id),
    sensor_data_id INTEGER REFERENCES sensor_data(id),
    ai_model_id INTEGER REFERENCES ai_model(model_id),
    timestamp TIMESTAMP DEFAULT NOW(),
    
    -- Action Output
    velocity DECIMAL(5, 2),
    turn_direction DECIMAL(6, 2),
    waste_collector_status VARCHAR(50),
    navigation_mode VARCHAR(50),  -- 'explore', 'collect', 'return', 'avoid'
    target_position JSONB,  -- {x, y, z}
    
    -- ML Metadata
    confidence_score DECIMAL(5, 4),
    reward_value DECIMAL(10, 4),
    
    INDEX idx_ml_robot_timestamp (robot_id, timestamp),
    INDEX idx_ml_mission_timestamp (mission_id, timestamp),
    INDEX idx_ml_model (ai_model_id)
);

-- Maintenance Table (dari ERD - untuk future admin features)
CREATE TABLE maintenance (
    maint_id SERIAL PRIMARY KEY,
    robot_id INTEGER REFERENCES robot(robot_id) ON DELETE CASCADE,
    tech_id INTEGER REFERENCES users(user_id),  -- Technician user
    maint_type VARCHAR(100) NOT NULL,  -- 'routine', 'repair', 'upgrade'
    schedule_dt TIMESTAMP,
    completed_dt TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled',  -- 'scheduled', 'in_progress', 'completed', 'cancelled'
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_maint_robot (robot_id),
    INDEX idx_maint_tech (tech_id),
    INDEX idx_maint_status (status)
);

-- =====================================================
-- 6. WASTE TRACKING
-- =====================================================

-- Waste Table (dari ERD - perfect!)
CREATE TABLE waste (
    waste_id SERIAL PRIMARY KEY,
    mission_id INTEGER REFERENCES mission(mission_id) ON DELETE CASCADE,
    waste_type VARCHAR(100) NOT NULL,  -- 'plastic_bottle', 'plastic_bag', etc.
    weight DECIMAL(10, 2) NOT NULL,  -- kg
    location JSONB,  -- {latitude, longitude, depth}
    detected_at TIMESTAMP NOT NULL,
    collected BOOLEAN DEFAULT FALSE,
    collected_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_waste_mission (mission_id),
    INDEX idx_waste_type (waste_type),
    INDEX idx_waste_collected (collected)
);

-- =====================================================
-- 7. AI/ML MODEL
-- =====================================================

-- AI Model Table (dari ERD)
CREATE TABLE ai_model (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    accuracy DECIMAL(5, 4),  -- 0.0000 to 1.0000
    trained_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',  -- 'active', 'deprecated', 'training'
    model_path VARCHAR(500),  -- Path to saved model file
    hyperparameters JSONB,  -- Model hyperparameters
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(model_name, version),
    INDEX idx_model_status (status)
);

-- Training Data Table (dari ERD)
CREATE TABLE training_data (
    data_id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES ai_model(model_id) ON DELETE CASCADE,
    input_data JSONB NOT NULL,  -- State/input data
    output_data JSONB,  -- Expected output/action
    reward DECIMAL(10, 4),  -- Reward value
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_training_model (model_id)
);

-- =====================================================
-- 8. FEEDBACK (Optional - untuk future feature)
-- =====================================================

-- Feedback Table (dari ERD)
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    booking_id INTEGER REFERENCES booking(booking_id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_feedback_user (user_id),
    INDEX idx_feedback_booking (booking_id)
);

-- =====================================================
-- INITIAL DATA / SEED DATA
-- =====================================================

-- Insert default roles
INSERT INTO role (role_name, description) VALUES
    ('admin', 'System administrator with full access'),
    ('operator', 'Certified robot operator'),
    ('customer', 'Regular customer');

-- Insert default permissions (example)
INSERT INTO permission (perm_name, description) VALUES
    ('view_dashboard', 'View dashboard and analytics'),
    ('control_robot', 'Control robot operations'),
    ('manage_robots', 'Manage robot inventory'),
    ('manage_users', 'Manage user accounts'),
    ('view_reports', 'View reports and analytics');

-- Link admin role to all permissions (example)
INSERT INTO role_permission (role_id, perm_id)
SELECT 1, perm_id FROM permission;  -- Assuming admin is role_id = 1

-- Insert certification modules (sesuai frontend)
INSERT INTO certification_module (module_number, title, duration_minutes, description, order_index) VALUES
    (1, 'Pengenalan Teknologi Sealen', 30, 'Pelajari dasar-dasar robot pembersih laut dan teknologi AI yang digunakan.', 1),
    (2, 'Navigasi dan Kontrol Robot', 45, 'Memahami sistem kontrol, navigasi otonom, dan antarmuka operator.', 2),
    (3, 'Pemeliharaan dan Troubleshooting', 40, 'Prosedur pemeliharaan rutin dan penanganan masalah umum.', 3),
    (4, 'Keselamatan dan Regulasi', 35, 'Standar keselamatan operasional dan regulasi maritim yang berlaku.', 4);

-- =====================================================
-- END OF SCHEMA
-- =====================================================

