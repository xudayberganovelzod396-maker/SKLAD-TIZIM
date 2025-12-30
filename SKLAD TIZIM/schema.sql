-- SKLAD TIZIMI DATABASE SCHEMA
-- Simple warehouse management system

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',  -- 'admin' or 'viewer'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Batches table (PARTIYALAR)
CREATE TABLE batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    batch_code TEXT NOT NULL,
    quantity INTEGER,
    quantity_sht INTEGER,
    quantity_kg REAL,
    comment TEXT,
    location TEXT NOT NULL,  -- Format: A-1-1, B-1-1, etc.
    status TEXT NOT NULL DEFAULT 'ACTIVE',  -- 'ACTIVE' or 'REMOVED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    removed_at TIMESTAMP,
    removed_by INTEGER,
    FOREIGN KEY (removed_by) REFERENCES users(id)
);

-- Insert test data
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('user', 'user123', 'viewer');

INSERT INTO batches (product_name, batch_code, quantity, quantity_sht, quantity_kg, location, status, comment) VALUES
('Kabel', 'P-001', 100, 100, 50, 'A-1-1', 'ACTIVE', 'Test'),
('Transformer', 'P-002', 50, 50, 25, 'B-1-1', 'ACTIVE', 'Test'),
('Kondensator', 'P-003', 200, 200, 100, 'A-2-1', 'ACTIVE', 'Test');
