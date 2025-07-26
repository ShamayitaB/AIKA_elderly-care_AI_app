-- Regions table (with supervisor info)
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    supervisor_name VARCHAR(100),
    supervisor_phone VARCHAR(20)
);

-- Users table (with password, no city_id)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL, -- Plain text for now (no JWT)
    phone VARCHAR(20),
    address TEXT,
    region_id INT REFERENCES regions(region_id) ON DELETE SET NULL,
    role VARCHAR(20) CHECK (role IN ('elderly', 'volunteer', 'caregiver', 'lovedone')) DEFAULT 'elderly',
    age INT,
    gender VARCHAR(20),
    blood_group VARCHAR(10),
    dob DATE,
    emergency_contact VARCHAR(20),
    aadhaar_no VARCHAR(20),
    state VARCHAR(100),
    pin_code VARCHAR(20),
    landmark TEXT,
    residence_type VARCHAR(50),
    years_at_address INT,
    medical_conditions JSONB,
    allergies JSONB,
    dietary_restrictions TEXT,
    special_needs TEXT,
    primary_doctor_name VARCHAR(100),
    primary_doctor_contact VARCHAR(20),
    primary_hospital VARCHAR(100),
    last_doctor_visit DATE,
    next_appointment DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Volunteer attributes table
CREATE TABLE volunteer_attributes (
    volunteer_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(20) CHECK (status IN ('Available', 'Busy', 'Offline')) DEFAULT 'Available',
    skills JSONB,
    distance DECIMAL(5,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fall detections table
CREATE TABLE fall_detections (
    fall_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    region_id INT REFERENCES regions(region_id) ON DELETE SET NULL,
    is_fall BOOLEAN NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'resolved')) DEFAULT 'pending'
);

-- Trigger to ensure fall_detections is only for elderly
CREATE OR REPLACE FUNCTION check_elderly_role()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users WHERE user_id = NEW.user_id) != 'elderly' THEN
        RAISE EXCEPTION 'Fall detections can only be recorded for elderly users';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_elderly_fall
BEFORE INSERT OR UPDATE ON fall_detections
FOR EACH ROW EXECUTE FUNCTION check_elderly_role();

-- Volunteer connections table
CREATE TABLE volunteer_connections (
    connection_id SERIAL PRIMARY KEY,
    elderly_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    volunteer_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(20) CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Triggers for volunteer_connections
CREATE OR REPLACE FUNCTION check_elderly_connection()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users WHERE user_id = NEW.elderly_id) != 'elderly' THEN
        RAISE EXCEPTION 'Elderly_id must reference an elderly user';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_elderly_connection
BEFORE INSERT OR UPDATE ON volunteer_connections
FOR EACH ROW EXECUTE FUNCTION check_elderly_connection();

CREATE OR REPLACE FUNCTION check_volunteer_connection()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users WHERE user_id = NEW.volunteer_id) != 'volunteer' THEN
        RAISE EXCEPTION 'Volunteer_id must reference a volunteer user';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_volunteer_connection
BEFORE INSERT OR UPDATE ON volunteer_connections
FOR EACH ROW EXECUTE FUNCTION check_volunteer_connection();

-- Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    type VARCHAR(20) CHECK (type IN ('grocery', 'medication')),
    details JSONB,
    status VARCHAR(20) CHECK (status IN ('pending', 'in_progress', 'delivered')) DEFAULT 'pending',
    volunteer_id INT REFERENCES users(user_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP
);

-- Medication reminders table
CREATE TABLE medication_reminders (
    reminder_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    medication_name VARCHAR(100),
    dosage VARCHAR(50),
    morning BOOLEAN DEFAULT FALSE,
    afternoon BOOLEAN DEFAULT FALSE,
    evening BOOLEAN DEFAULT FALSE,
    purpose TEXT,
    frequency VARCHAR(20) CHECK (frequency IN ('daily', 'weekly', 'custom')),
    custom_days VARCHAR(50),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to ensure medication_reminders is only for elderly
CREATE OR REPLACE FUNCTION check_elderly_reminder()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users WHERE user_id = NEW.user_id) != 'elderly' THEN
        RAISE EXCEPTION 'Medication reminders can only be set for elderly users';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_elderly_reminder
BEFORE INSERT OR UPDATE ON medication_reminders
FOR EACH ROW EXECUTE FUNCTION check_elderly_reminder();

-- Family contacts table (includes lovedone role users via queries)
CREATE TABLE family_contacts (
    contact_id SERIAL PRIMARY KEY,
    elderly_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    relation VARCHAR(50),
    phone VARCHAR(20),
    address TEXT,
    last_contact TIMESTAMP,
    reminder TEXT,
    is_local_guardian BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_fall_detections_user_id ON fall_detections(user_id);
CREATE INDEX idx_fall_detections_region_id ON fall_detections(region_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_reminders_user_id ON medication_reminders(user_id);
CREATE INDEX idx_volunteer_connections_elderly_id ON volunteer_connections(elderly_id);
CREATE INDEX idx_volunteer_connections_volunteer_id ON volunteer_connections(volunteer_id);
CREATE INDEX idx_users_region_id ON users(region_id);
CREATE INDEX idx_family_contacts_elderly_id ON family_contacts(elderly_id);