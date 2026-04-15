SELECT * FROM V_Current_Valid_Prices;

SELECT
	vpsh.product_id,
    vpsh.sku,
    vpsh.product_name,
    vpsh.supplier_name,
    vpsh.supplier_valid_start AS "Supplier_Valid_From",
    vpsh.supplier_valid_end AS "Supplier_Valid_Until",
    vpsh.transaction_start AS "Recorded_From"
FROM
    V_Product_Supplier_History vpsh
WHERE
    product_id = 10
ORDER BY
    vpsh.supplier_valid_start;
	
SELECT * FROM V_Late_Data_Entry_PricingRecords;
SELECT * FROM V_Prices_Valid_During_Q3_2025;
SELECT * FROM V_Product_Discounts_25_11_2024_Snapshot;