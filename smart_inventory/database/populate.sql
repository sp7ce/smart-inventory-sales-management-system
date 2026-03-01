-- ============================================================
-- Smart Inventory — Sample Data Population Script
-- Run this AFTER schema.sql
-- ============================================================

USE smart_inventory;

-- ── Products ─────────────────────────────────────────────────

INSERT INTO products (name, category, price, quantity_in_stock) VALUES
('Laptop Pro 15"',       'Electronics',  1299.99, 45),
('Wireless Mouse',       'Accessories',    29.99, 150),
('Mechanical Keyboard',  'Accessories',    89.99, 80),
('USB-C Hub',            'Accessories',    49.99, 120),
('27" 4K Monitor',       'Electronics',   449.99, 30),
('Webcam HD 1080p',      'Electronics',    79.99, 65),
('Noise-Cancelling Headphones', 'Audio',  199.99, 55),
('Bluetooth Speaker',    'Audio',          59.99, 90),
('External SSD 1TB',     'Storage',       109.99, 70),
('RAM 16 GB DDR5',       'Components',     74.99, 100),
('Graphics Card RTX',    'Components',    599.99, 25),
('Laptop Stand',         'Accessories',    39.99, 110),
('Desk Lamp LED',        'Office',         34.99, 85),
('Ergonomic Chair',      'Office',        349.99, 20),
('Power Strip 6-Outlet', 'Office',         19.99, 200);

-- ── Customers ────────────────────────────────────────────────

INSERT INTO customers (name, email) VALUES
('Alice Martin',   'alice.martin@example.com'),
('Bob Johnson',    'bob.johnson@example.com'),
('Carol Williams', 'carol.williams@example.com'),
('David Brown',    'david.brown@example.com'),
('Eva Davis',      'eva.davis@example.com'),
('Frank Wilson',   'frank.wilson@example.com'),
('Grace Lee',      'grace.lee@example.com'),
('Henry Taylor',   'henry.taylor@example.com');

-- ── Orders & Items ───────────────────────────────────────────

-- Order 1 — Alice
INSERT INTO orders (customer_id, order_date) VALUES (1, '2025-09-05 10:15:00');
SET @o1 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o1, 1, 1, 1299.99),
(@o1, 2, 2,   29.99),
(@o1, 4, 1,   49.99);

-- Order 2 — Bob
INSERT INTO orders (customer_id, order_date) VALUES (2, '2025-09-12 14:30:00');
SET @o2 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o2, 3, 1, 89.99),
(@o2, 7, 1, 199.99);

-- Order 3 — Carol
INSERT INTO orders (customer_id, order_date) VALUES (3, '2025-10-01 09:00:00');
SET @o3 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o3, 5, 2, 449.99),
(@o3, 6, 1, 79.99);

-- Order 4 — Alice (second order)
INSERT INTO orders (customer_id, order_date) VALUES (1, '2025-10-18 16:45:00');
SET @o4 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o4, 9, 1, 109.99),
(@o4, 10, 2, 74.99);

-- Order 5 — David
INSERT INTO orders (customer_id, order_date) VALUES (4, '2025-11-02 11:20:00');
SET @o5 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o5, 11, 1, 599.99),
(@o5, 10, 1,  74.99),
(@o5, 3, 1,  89.99);

-- Order 6 — Eva
INSERT INTO orders (customer_id, order_date) VALUES (5, '2025-11-15 13:10:00');
SET @o6 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o6, 14, 1, 349.99),
(@o6, 13, 2,  34.99),
(@o6, 12, 1,  39.99);

-- Order 7 — Frank
INSERT INTO orders (customer_id, order_date) VALUES (6, '2025-12-03 08:50:00');
SET @o7 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o7, 1, 1, 1299.99),
(@o7, 8, 2,   59.99);

-- Order 8 — Grace
INSERT INTO orders (customer_id, order_date) VALUES (7, '2025-12-20 15:00:00');
SET @o8 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o8, 2, 3,  29.99),
(@o8, 15, 2, 19.99);

-- Order 9 — Henry
INSERT INTO orders (customer_id, order_date) VALUES (8, '2026-01-10 10:05:00');
SET @o9 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o9, 7, 1, 199.99),
(@o9, 9, 2, 109.99);

-- Order 10 — Bob (second order)
INSERT INTO orders (customer_id, order_date) VALUES (2, '2026-01-25 17:30:00');
SET @o10 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o10, 5, 1, 449.99),
(@o10, 12, 2, 39.99),
(@o10, 15, 1, 19.99);

-- Order 11 — Carol (second order)
INSERT INTO orders (customer_id, order_date) VALUES (3, '2026-02-08 12:00:00');
SET @o11 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o11, 6, 2, 79.99),
(@o11, 4, 1, 49.99);

-- Order 12 — David (second order)
INSERT INTO orders (customer_id, order_date) VALUES (4, '2026-02-20 09:30:00');
SET @o12 = LAST_INSERT_ID();
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(@o12, 8, 1, 59.99),
(@o12, 13, 1, 34.99);
