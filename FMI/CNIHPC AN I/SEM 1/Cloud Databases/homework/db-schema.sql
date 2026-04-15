CREATE DATABASE shop;

CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS periods;

-- SUPPLIERS
CREATE TABLE Suppliers (
    record_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    valid_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT supplier_valid_period CHECK (valid_start < valid_end),
    CONSTRAINT supplier_transaction_period CHECK (transaction_start < transaction_end)
);

SELECT periods.add_period('Suppliers', 'valid', 'valid_start', 'valid_end');
SELECT periods.add_period('Suppliers', 'transaction', 'transaction_start', 'transaction_end');
SELECT periods.add_unique_key('Suppliers', ARRAY['supplier_id'], 'valid');
SELECT periods.add_unique_key('Suppliers', ARRAY['supplier_id'], 'transaction');

-- PRODUCTS
CREATE TABLE Products (
    record_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INT NOT NULL,
    supplier_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    sku VARCHAR(50) NOT NULL,
    description TEXT,
    valid_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT product_valid_period CHECK (valid_start < valid_end),
    CONSTRAINT product_transaction_period CHECK (transaction_start < transaction_end)
);

SELECT periods.add_period('Products', 'valid', 'valid_start', 'valid_end');
SELECT periods.add_period('Products', 'transaction', 'transaction_start', 'transaction_end');
SELECT periods.add_unique_key('Products', ARRAY['product_id'], 'valid');
SELECT periods.add_unique_key('Products', ARRAY['product_id'], 'transaction');

-- PRICING RECORDS
CREATE TABLE PricingRecords (
    record_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    valid_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT valid_nonempty CHECK (valid_start < valid_end),
    CONSTRAINT transaction_nonempty CHECK (transaction_start < transaction_end)
);

SELECT periods.add_period('PricingRecords', 'valid', 'valid_start', 'valid_end');
SELECT periods.add_period('PricingRecords', 'transaction', 'transaction_start', 'transaction_end');
SELECT periods.add_unique_key('PricingRecords', ARRAY['product_id'], 'valid');
SELECT periods.add_unique_key('PricingRecords', ARRAY['product_id'], 'transaction');

-- DISCOUNTS
CREATE TABLE Discounts (
    record_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    discount_id INT NOT NULL,
    discount_percent DECIMAL(5, 2) NOT NULL CHECK (discount_percent > 0 AND discount_percent <= 100),
    description VARCHAR(255),
    valid_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT discount_valid_period CHECK (valid_start < valid_end),
    CONSTRAINT discount_transaction_period CHECK (transaction_start < transaction_end)
);

SELECT periods.add_period('Discounts', 'valid', 'valid_start', 'valid_end');
SELECT periods.add_period('Discounts', 'transaction', 'transaction_start', 'transaction_end');
SELECT periods.add_unique_key('Discounts', ARRAY['discount_id'], 'valid');
SELECT periods.add_unique_key('Discounts', ARRAY['discount_id'], 'transaction');

-- PRODUCT DISCOUNTS
-- NOTE: Discount_id should reference record_id from Discounts for integrity.
CREATE TABLE ProductDiscounts (
    product_id INT NOT NULL,
    discount_id INT NOT NULL, -- Keep discount_id (entity id) for unique key, but link to Discounts record_id if FK is needed.
    valid_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    valid_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_start TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    transaction_end TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (product_id, discount_id, valid_start, transaction_start),
    CONSTRAINT pd_valid_period CHECK (valid_start < valid_end),
    CONSTRAINT pd_transaction_period CHECK (transaction_start < transaction_end)
);

SELECT periods.add_period('ProductDiscounts', 'valid', 'valid_start', 'valid_end');
SELECT periods.add_period('ProductDiscounts', 'transaction', 'transaction_start', 'transaction_end');
SELECT periods.add_unique_key('ProductDiscounts', ARRAY['product_id','discount_id'], 'valid');
SELECT periods.add_unique_key('ProductDiscounts', ARRAY['product_id','discount_id'], 'transaction');

CREATE FUNCTION verify_supplier_id_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Suppliers WHERE supplier_id = NEW.supplier_id) THEN
        RAISE EXCEPTION 'Referential Integrity Error: Supplier ID % does not exist in the Suppliers entity table.', NEW.supplier_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_product_check_supplier
BEFORE INSERT OR UPDATE ON Products
FOR EACH ROW
EXECUTE FUNCTION verify_supplier_id_exists();

CREATE OR REPLACE FUNCTION verify_product_id_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Products WHERE product_id = NEW.product_id) THEN
        RAISE EXCEPTION 'Referential Integrity Error: Product ID % does not exist in the Products entity table.', NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_pricing_record_check_product
BEFORE INSERT OR UPDATE ON PricingRecords
FOR EACH ROW
EXECUTE FUNCTION verify_product_id_exists();

CREATE OR REPLACE TRIGGER trg_product_discount_check_product
BEFORE INSERT OR UPDATE ON ProductDiscounts
FOR EACH ROW
EXECUTE FUNCTION verify_product_id_exists();