-- =============================================
-- SKLAD TIZIM - DATABASE SCHEMA
-- Ombor Boshqaruv Tizimi
-- Version: 2.0
-- =============================================

-- Foydalanuvchilar jadvali
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Partiyalar jadvali
CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    batch_code TEXT NOT NULL,
    quantity INTEGER,
    quantity_sht INTEGER,
    quantity_kg REAL,
    comment TEXT,
    location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    is_archived INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    removed_at TIMESTAMP,
    removed_by INTEGER,
    removed_quantity_sht INTEGER DEFAULT 0,
    removed_quantity_kg REAL DEFAULT 0.0,
    FOREIGN KEY (removed_by) REFERENCES users(id)
);

-- Kirim/Chiqim harakatlari
CREATE TABLE IF NOT EXISTS batch_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL, -- IN / OUT
    quantity_sht INTEGER DEFAULT 0,
    quantity_kg REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(id)
);

-- Sklad so'rovlar jadvali
CREATE TABLE IF NOT EXISTS stock_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    batch_code TEXT,
    quantity_sht INTEGER DEFAULT 0,
    quantity_kg REAL DEFAULT 0.0,
    comment TEXT,
    status TEXT DEFAULT 'NEW',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seen_at TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Indekslar
CREATE INDEX IF NOT EXISTS idx_batches_status ON batches(status);
CREATE INDEX IF NOT EXISTS idx_batches_location ON batches(location);
CREATE INDEX IF NOT EXISTS idx_batches_batch_code ON batches(batch_code);
CREATE INDEX IF NOT EXISTS idx_batches_created_at ON batches(created_at);
CREATE INDEX IF NOT EXISTS idx_movements_batch_id ON batch_movements(batch_id);
CREATE INDEX IF NOT EXISTS idx_movements_type ON batch_movements(movement_type);
CREATE INDEX IF NOT EXISTS idx_movements_created_at ON batch_movements(created_at);
CREATE INDEX IF NOT EXISTS idx_requests_status ON stock_requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_created_at ON stock_requests(created_at);
