-- SUPPLIERS TRIGGER TEST
-- 1. Insert
INSERT INTO Suppliers (supplier_id, name, valid_start, valid_end)
VALUES
(20, 'TestCorp Beta', '2025-10-28', '2030-10-28');

SELECT
    supplier_id,
    name,
	valid_start,
	valid_end,
    transaction_start,
    transaction_end
FROM
    Suppliers
ORDER BY
    transaction_start DESC;

-- 2. Update
UPDATE Suppliers
SET name = 'TestCorp Pro (Updated Name)'
WHERE supplier_id = 20

SELECT
    supplier_id,
    name,
    transaction_start,
    transaction_end
FROM
    Suppliers
WHERE
    supplier_id = 20
ORDER BY
    transaction_start DESC;

-- PRODUCTS TRIGGER TEST
-- 1. Insert
INSERT INTO Products (product_id, supplier_id, name, sku, description, valid_start, valid_end)
VALUES
(105, 10, 'Widget A', 'WGT-A-001', 'First Widget', '2025-10-28', '2030-10-28');

SELECT
    product_id,
    supplier_id,
    name,
    sku,
    description,
    valid_start,
    valid_end,
    transaction_start,
    transaction_end
FROM
    Products
ORDER BY
    transaction_start DESC;

-- 2. Update
UPDATE Products
SET name = 'Widget A+ (Updated Name)'
WHERE product_id = 105;

SELECT
    product_id,
    name,
    transaction_start,
    transaction_end
FROM
    Products
WHERE
    product_id = 105
ORDER BY
    transaction_start DESC;

-- PRICING RECORDS TRIGGER TEST
-- 1. Insert
INSERT INTO PricingRecords (product_id, price, valid_start, valid_end)
VALUES
(105, 49.99, '2025-10-28', '2030-10-28');

SELECT
    record_id,
    product_id,
    price,
    valid_start,
    valid_end,
    transaction_start,
    transaction_end
FROM
    PricingRecords
ORDER BY
    transaction_start DESC;

-- 2. Update
UPDATE PricingRecords
SET price = 54.99
WHERE product_id = 105;

SELECT
    record_id,
    price,
    transaction_start,
    transaction_end
FROM
    PricingRecords
WHERE
    product_id = 105
ORDER BY
    transaction_start DESC;

-- DISCOUNTS TRIGGER TEST
-- 1. Insert
INSERT INTO Discounts (discount_id, discount_percent, description, valid_start, valid_end)
VALUES
(205, 10.00, 'Holiday Sale', '2025-10-28', '2030-10-28');

SELECT
    discount_id,
    discount_percent,
    description,
    valid_start,
    valid_end,
    transaction_start,
    transaction_end
FROM
    Discounts
ORDER BY
    transaction_start DESC;

-- 2. Update
UPDATE Discounts
SET discount_percent = 15.00
WHERE discount_id = 205;

SELECT
    discount_id,
    discount_percent,
    transaction_start,
    transaction_end
FROM
    Discounts
WHERE
    discount_id = 205
ORDER BY
    transaction_start DESC;

-- PRODUCT DISCOUNTS TRIGGER TEST
-- 1. Insert
INSERT INTO ProductDiscounts (product_id, discount_id, valid_start, valid_end)
VALUES
(105, 205, '2025-10-28', '2030-10-28');

SELECT
    product_id,
    discount_id,
    valid_start,
    valid_end,
    transaction_start,
    transaction_end
FROM
    ProductDiscounts
ORDER BY
    transaction_start DESC;

-- 2. Update
UPDATE ProductDiscounts
SET valid_end = '2031-12-31'
WHERE product_id = 105
  AND discount_id = 205;

SELECT
    product_id,
    discount_id,
    valid_start,
    valid_end,
    transaction_start,
    transaction_end
FROM
    ProductDiscounts
WHERE
    product_id = 105
  AND discount_id = 205
ORDER BY
    transaction_start DESC;
