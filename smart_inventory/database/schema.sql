-- ============================================================
-- Smart Inventory — MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS smart_inventory
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE smart_inventory;

-- ── Products ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS products (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(200)   NOT NULL,
    category    VARCHAR(100)   NOT NULL,
    price       DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    quantity_in_stock INT      NOT NULL DEFAULT 0 CHECK (quantity_in_stock >= 0),
    created_at  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ── Customers ────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS customers (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(200)   NOT NULL,
    email       VARCHAR(254)   NOT NULL UNIQUE,
    created_at  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ── Orders ───────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS orders (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT            NOT NULL,
    order_date  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at  DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── Order Items ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS order_items (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    order_id    INT            NOT NULL,
    product_id  INT            NOT NULL,
    quantity    INT            NOT NULL CHECK (quantity > 0),
    unit_price  DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_items_order
        FOREIGN KEY (order_id) REFERENCES orders(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_items_product
        FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;
