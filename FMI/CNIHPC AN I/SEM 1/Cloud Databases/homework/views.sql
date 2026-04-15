-- Show current prices
CREATE VIEW V_Current_Valid_Prices AS
SELECT
    pr.product_id,
    p.name AS product_name,
    pr.price,
    pr.valid_start,
    pr.valid_end
FROM
    PricingRecords pr
JOIN
    Products p ON pr.product_id = p.product_id
WHERE
    CURRENT_DATE BETWEEN pr.valid_start AND pr.valid_end
    AND pr.transaction_end = '2099-12-31'::date;

-- All versions of a product
CREATE VIEW V_Product_Supplier_History AS
SELECT
    p.product_id,
    p.name AS product_name,
    s.name AS supplier_name,
    p.sku,
    p.valid_start AS supplier_valid_start,
    p.valid_end AS supplier_valid_end,
    p.transaction_start,
    p.transaction_end
FROM
    Products p
JOIN
    Suppliers s ON p.supplier_id = s.supplier_id
ORDER BY
    p.product_id, p.valid_start;

-- Show late data entries from PricingRecords table
CREATE VIEW V_Late_Data_Entry_PricingRecords AS
SELECT
    pr.product_id,
    pr.price,
    pr.valid_start,
    pr.valid_end,
    pr.transaction_start,
    (pr.transaction_start - pr.valid_start) AS lag_days
FROM
    PricingRecords pr
WHERE
    pr.transaction_start > pr.valid_start

-- Show valid prices during third quarter of 2025
CREATE VIEW V_Prices_Valid_During_Q3_2025 AS
SELECT
    p.name AS product_name,
    pr.price,
    pr.valid_start,
    pr.valid_end
FROM
    PricingRecords pr
JOIN
    Products p ON pr.product_id = p.product_id
WHERE
    pr.valid_start <= DATE '2025-09-30'
    AND pr.valid_end >= DATE '2025-07-01'
    AND pr.transaction_end = DATE '2099-12-31';

-- All discounts valid on 25th November 2024
CREATE VIEW V_Product_Discounts_25_11_2024_Snapshot AS
SELECT
    pd.product_id,
    p.name AS product_name,
    d.discount_id,
    d.description AS discount_name,
    d.discount_percent,
    pd.valid_start AS promo_valid_start,
    pd.valid_end AS promo_valid_end,
    pd.transaction_start AS record_start_date,
    pd.transaction_end AS record_end_date
FROM
    ProductDiscounts pd
JOIN
    Discounts d ON pd.discount_id = d.discount_id
JOIN
    Products p ON pd.product_id = p.product_id
WHERE
    '2024-11-25' BETWEEN pd.transaction_start AND pd.transaction_end
    AND '2024-11-25' BETWEEN pd.valid_start AND pd.valid_end;