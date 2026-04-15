INSERT INTO Suppliers (supplier_id, name, valid_start, valid_end, transaction_start, transaction_end)
VALUES
(1, 'FreshFarm Foods SRL', '2023-01-01', '2024-05-16', '2023-01-01', '2024-05-15'), 
(1, 'FreshFarm AGRO SA', '2024-05-16', '2028-12-31', '2024-05-16', '2099-12-31'),
(3, 'TechMaster Corp.', '2023-03-01', '2030-12-31', '2023-03-01', '2099-12-31'),
(4, 'HomeStyle Design Ltd.', '2024-01-01', '2030-12-31', '2024-01-01', '2099-12-31'),
(5, 'BeverageWorld Distribution', '2023-06-01', '2024-12-01', '2023-06-01', '2024-12-01'),
(5, 'BW Logistics Hub', '2024-12-01', '2025-12-31', '2024-12-02', '2099-12-31'), 
(7, 'EcoPack Solutions', '2023-02-01', '2025-07-01', '2023-02-01', '2025-07-01'), 
(7, 'CleanEarth Supplies', '2025-07-01', '2035-12-31', '2025-07-02', '2099-12-31'),
(9, 'LocalHarvest Producers', '2025-01-10', '2030-12-31', '2025-01-10', '2099-12-31');

INSERT INTO Products (product_id, supplier_id, name, sku, description, valid_start, valid_end, transaction_start, transaction_end)
VALUES
-- OLD (Perioadele valide se închid înainte de startul noii versiuni)

-- ID 10: Organic Apples (v1) - Închis la 2024-05-16
(10, 1, 'Organic Apples', 'APL-ORG-01', 'Fresh organic apples 1kg (v1)', '2023-01-01', '2024-05-16', '2023-01-01', '2024-05-15'), 
-- ID 11: Wireless Mouse (v1) - Închis la 2024-06-01
(11, 3, 'Wireless Mouse Std.', 'TM-MSE-01', 'Ergonomic wireless mouse (Ambalaj vechi)', '2023-03-01', '2024-06-01', '2023-03-01', '2024-06-01'),
-- ID 12: Mechanical Keyboard (v1) - Închis la 2024-12-01
(12, 3, 'Mechanical Keyboard', 'TM-KBD-01', 'RGB mechanical keyboard (v1) - Switch Red', '2023-04-01', '2024-12-01', '2023-04-01', '2024-12-01'),
-- ID 13: Wooden Chair (v1) - Închis la 2025-04-01
(13, 4, 'Wooden Chair', 'HS-CHR-01', 'Dining wooden chair (Lemn de pin)', '2024-01-01', '2025-04-01', '2024-01-01', '2025-04-01'),
-- ID 14: Sparkling Water (v1) - Închis la 2024-12-01
(14, 5, 'Sparkling Water', 'BW-SW-01', 'Mineral sparkling water 1L (Sursa A)', '2023-06-15', '2024-12-01', '2023-06-15', '2024-12-01'),
-- ID 15: Simple Feature Phone (Scoatere din producție)
(15, 3, 'Simple Feature Phone', 'TM-PHN-01', 'Model scos din productie', '2023-07-01', '2024-03-01', '2023-07-01', '2024-03-01'),
-- ID 16: Eco Paper Cups (v1) - Închis la 2025-07-01
(16, 7, 'Eco Paper Cups', 'EP-CUP-01', 'Biodegradable paper cups 100buc (v1)', '2023-02-01', '2025-07-01', '2023-02-01', '2025-07-01'),
-- ID 17: Sofa Cushion (v1) - Închis la 2025-09-01
(17, 4, 'Sofa Cushion', 'HS-CSH-05', 'Decorative sofa cushion - Model 2024', '2025-03-20', '2025-09-01', '2025-03-20', '2025-09-01'),
-- ID 18: External HDD 1TB (Retras) - Închis la 2024-11-01
(18, 3, 'External HDD 1TB', 'TM-HDD-08', 'Portable external HDD 1TB (Retras)', '2023-10-01', '2024-11-01', '2023-10-01', '2024-11-01'),

-- CURENT (transaction_end = '2099-12-31')

-- ID 10: Organic Apples (v2)
(10, 1, 'Organic Apples', 'APL-ORG-01', 'Fresh organic apples 1kg (v2)', '2024-05-16', '2027-12-31', '2024-05-16', '2099-12-31'), 
-- ID 11: Wireless Mouse PRO (v2)
(11, 3, 'Wireless Mouse PRO', 'TM-MSE-01', 'Ergonomic wireless mouse (Model 2024)', '2024-06-01', '2028-12-31', '2024-06-01', '2099-12-31'), 
-- ID 12: Mechanical Keyboard TKL (v2)
(12, 3, 'Mechanical Keyboard TKL', 'TM-KBD-01', 'RGB mechanical keyboard (v2, TKL)', '2024-12-01', '2028-12-31', '2024-12-01', '2099-12-31'), 
-- ID 13: Wooden Chair (v2)
(13, 4, 'Wooden Chair', 'HS-CHR-01', 'Dining wooden chair (Design 2025)', '2025-04-01', '2029-12-31', '2025-04-01', '2099-12-31'), 
-- ID 20: Orange Juice 1L (NOU, ID 20)
(20, 5, 'Orange Juice 1L', 'BW-OJ-01', 'Natural squeezed orange juice 1L (Noua formula)', '2024-10-01', '2026-12-31', '2024-10-01', '2099-12-31'), 
-- ID 14: Sparkling Water Lime (v2, ID 14)
(14, 5, 'Sparkling Water Lime', 'BW-SW-01', 'Mineral sparkling water 1L (lamaie)', '2024-12-01', '2027-12-31', '2024-12-01', '2099-12-31'), 
-- ID 16: Eco Paper Cups 200pcs (v2)
(16, 7, 'Eco Paper Cups 200pcs', 'EP-CUP-01', 'Biodegradable paper cups 200buc (v2)', '2025-07-01', '2028-12-31', '2025-07-01', '2099-12-31'), 
-- ID 17: Sofa Cushion Deluxe (v2)
(17, 4, 'Sofa Cushion Deluxe', 'HS-CSH-05', 'Decorative sofa cushion - Model 2025', '2025-09-01', '2028-03-20', '2025-09-01', '2099-12-31'), 
-- ID 18: External HDD 2TB (v2)
(18, 3, 'External HDD 2TB', 'TM-HDD-08', 'Portable external HDD 2TB', '2024-11-01', '2028-11-01', '2024-11-01', '2099-12-31'), 
-- ID 19: Bananas
(19, 1, 'Bananas', 'BNN-01', 'Premium ripe bananas 1kg', '2023-02-01', '2027-12-31', '2024-08-01', '2099-12-31'), 
-- ID 21: Pears (ID nou)
(21, 1, 'Pears', 'APL-PEAR-02', 'Sweet conference pears 1kg', '2024-08-01', '2027-07-31', '2024-08-01', '2099-12-31'), 
-- ID 22: Avocado (ID nou)
(22, 1, 'Avocado', 'APL-AVO-02', 'Ripe Hass avocados 2pcs', '2025-05-01', '2027-05-01', '2025-05-01', '2099-12-31'), 
-- ID 23: Tomatoes Cherry (ID nou)
(23, 1, 'Tomatoes Cherry', 'APL-TOM-03', 'Cherry tomatoes 250g', '2024-09-01', '2027-09-01', '2024-09-01', '2099-12-31'), 
-- ID 24: Local Honey (ID nou)
(24, 9, 'Local Honey', 'LH-HON-01', 'Raw local acacia honey 500g', '2025-01-10', '2027-01-10', '2025-01-10', '2099-12-31'), 
-- ID 25: Goat Cheese (ID nou)
(25, 9, 'Goat Cheese', 'LH-CHE-02', 'Aged goat cheese 200g', '2025-04-01', '2026-04-01', '2025-04-01', '2099-12-31'), 
-- ID 26: Laptop Stand (ID nou)
(26, 3, 'Laptop Stand', 'TM-LPS-02', 'Adjustable aluminum stand', '2024-03-01', '2028-03-01', '2024-03-01', '2099-12-31'), 
-- ID 27: Webcam 1080p (ID nou)
(27, 3, 'Webcam 1080p', 'TM-WCM-03', 'Full HD 1080p webcam', '2024-03-01', '2028-03-01', '2024-03-01', '2099-12-31'), 
-- ID 28: USB-C Hub (ID nou)
(28, 3, 'USB-C Hub', 'TM-HBC-04', '7-in-1 USB-C docking station', '2025-05-15', '2028-05-15', '2025-05-15', '2099-12-31'), 
-- ID 29: Gaming Mousepad (ID nou)
(29, 3, 'Gaming Mousepad', 'TM-MPD-05', 'Large RGB mousepad', '2025-02-10', '2028-02-10', '2025-02-10', '2099-12-31'), 
-- ID 30: Bluetooth Headset (ID nou)
(30, 3, 'Bluetooth Headset', 'TM-HDS-06', 'Office Bluetooth headset', '2025-03-01', '2028-03-01', '2025-03-01', '2099-12-31'), 
-- ID 31: Router Wi-Fi 6 (ID nou)
(31, 3, 'Router Wi-Fi 6', 'TM-RTR-09', 'Dual-band Wi-Fi 6 router', '2025-09-01', '2029-09-01', '2025-09-01', '2099-12-31'), 
-- ID 32: Small Table (ID nou)
(32, 4, 'Small Table', 'HS-TBL-02', 'Small wooden side table', '2024-02-15', '2028-02-15', '2024-02-15', '2099-12-31'), 
-- ID 33: Floor Lamp (ID nou)
(33, 4, 'Floor Lamp', 'HS-LMP-03', 'Modern metallic floor lamp', '2024-07-01', '2028-07-01', '2024-07-01', '2099-12-31'), 
-- ID 34: Kitchen Shelf (ID nou)
(34, 4, 'Kitchen Shelf', 'HS-SHF-04', 'Wall mounted kitchen shelf', '2025-02-01', '2028-02-01', '2025-02-01', '2099-12-31'), 
-- ID 35: Shoe Rack (ID nou)
(35, 4, 'Shoe Rack', 'HS-SRK-06', 'Bamboo shoe rack 3-tier', '2024-10-01', '2028-10-01', '2024-10-01', '2099-12-31'), 
-- ID 36: Mirror (ID nou)
(36, 4, 'Mirror', 'HS-MIR-08', 'Round decorative wall mirror', '2025-06-01', '2029-06-01', '2025-06-01', '2099-12-31'), 
-- ID 37: Hanger Set (ID nou)
(37, 4, 'Hanger Set', 'HS-HGR-09', 'Wooden hanger set 10pcs', '2023-10-01', '2027-10-01', '2023-10-01', '2099-12-31'), 
-- ID 38: Apple Juice (ID nou)
(38, 5, 'Apple Juice', 'BW-AJ-02', 'Fresh pressed apple juice 1L', '2025-03-01', '2027-03-01', '2025-03-01', '2099-12-31'), 
-- ID 39: Oat Milk (ID nou)
(39, 5, 'Oat Milk', 'BW-OMK-03', 'Barista edition oat milk 1L', '2024-11-01', '2026-11-01', '2024-11-01', '2099-12-31'), 
-- ID 40: Espresso Beans (ID nou)
(40, 5, 'Espresso Beans', 'BW-ESB-04', 'Dark roast espresso beans 500g', '2025-08-01', '2027-08-01', '2025-08-01', '2099-12-31'), 
-- ID 41: Almond Milk (ID nou)
(41, 5, 'Almond Milk', 'BW-AMK-07', 'Unsweetened almond milk 1L', '2025-04-01', '2026-04-01', '2025-04-01', '2099-12-31'), 
-- ID 42: Energy Drink (ID nou)
(42, 5, 'Energy Drink', 'BW-END-08', 'Zero sugar energy drink 250ml', '2024-02-01', '2026-02-01', '2024-02-01', '2099-12-31'), 
-- ID 43: Canned Beans (ID nou)
(43, 5, 'Canned Beans', 'BW-CBE-09', 'Canned organic kidney beans 400g', '2025-08-01', '2027-08-01', '2025-08-01', '2099-12-31'), 
-- ID 44: Compostable Plates (ID nou)
(44, 7, 'Compostable Plates', 'EP-PLT-02', 'Biodegradable dinner plates', '2023-10-01', '2027-10-01', '2023-10-01', '2099-12-31'), 
-- ID 45: Wooden Cutlery Set (ID nou)
(45, 7, 'Wooden Cutlery Set', 'EP-CLY-03', 'Disposable wooden forks and spoons', '2024-04-01', '2028-04-01', '2024-04-01', '2099-12-31'), 
-- ID 46: Paper Straws (ID nou)
(46, 7, 'Paper Straws', 'EP-STR-04', 'Eco-friendly paper straws 50 pcs', '2025-07-01', '2029-06-01', '2025-07-01', '2099-12-31'), 
-- ID 47: Recycled Napkins (ID nou)
(47, 7, 'Recycled Napkins', 'EP-NAP-05', 'Brown recycled napkins 100 pcs', '2024-05-01', '2027-05-01', '2024-05-01', '2099-12-31'), 
-- ID 48: Hand Sanitizer (ID nou)
(48, 7, 'Hand Sanitizer', 'EP-SAN-07', 'Eco hand sanitizer 500ml', '2023-11-01', '2027-11-01', '2023-11-01', '2099-12-31'), 
-- ID 49: Laundry Pods (ID nou)
(49, 7, 'Laundry Pods', 'EP-LND-08', 'Eco laundry detergent pods 30pcs', '2024-07-01', '2028-07-01', '2024-07-01', '2099-12-31'), 
-- ID 50: Kiwi (ID nou)
(50, 1, 'Kiwi', 'APL-KWI-04', 'Fresh kiwi 500g', '2024-07-01', '2027-07-01', '2024-07-01', '2099-12-31'), 
-- ID 51: Mango (ID nou)
(51, 1, 'Mango', 'APL-MNG-05', 'Ready-to-eat mango', '2025-01-01', '2026-01-01', '2025-01-01', '2099-12-31'), 
-- ID 52: Cabbage (ID nou)
(52, 1, 'Cabbage', 'APL-CBB-06', 'White cabbage 1pc', '2024-12-01', '2027-12-01', '2024-12-01', '2099-12-31'), 
-- ID 53: Gaming Headset 7.1 (ID nou)
(53, 3, 'Gaming Headset 7.1', 'TM-GHS-10', 'High-fidelity surround sound headset', '2025-06-15', '2029-06-15', '2025-06-15', '2099-12-31'), 
-- ID 54: Desk Organizer (ID nou)
(54, 4, 'Desk Organizer', 'HS-DORG-10', 'Bamboo desk organizer', '2025-08-01', '2029-08-01', '2025-08-01', '2099-12-31'), 
-- ID 55: Protein Shake (ID nou)
(55, 5, 'Protein Shake', 'BW-PRS-10', 'Vanilla protein shake 330ml', '2025-01-01', '2027-01-01', '2025-01-01', '2099-12-31'), 
-- ID 56: Recycled Trash Bags (ID nou)
(56, 7, 'Recycled Trash Bags', 'EP-BAG-10', '100% Recycled trash bags 50pcs', '2024-09-01', '2028-09-01', '2024-09-01', '2099-12-31'), 
-- ID 57: Spelt Bread (ID nou)
(57, 9, 'Spelt Bread', 'LH-BRED-03', 'Handmade whole spelt bread 500g', '2025-09-15', '2026-09-15', '2025-09-15', '2099-12-31');

INSERT INTO PricingRecords (product_id, price, valid_start, valid_end, transaction_start, transaction_end)
VALUES
-- 1. Organic Apples (ID 10)
(10, 4.00, '2024-05-16', '2024-09-30', '2024-05-16', '2024-10-01'),
(10, 4.50, '2024-10-01', '2025-03-31', '2024-10-01', '2025-04-01'),
(10, 4.99, '2025-04-01', '2027-12-31', '2025-04-01', '2099-12-31'),

-- 2. Mechanical Keyboard TKL (ID 12)
(12, 350.00, '2024-01-01', '2024-05-31', '2024-01-01', '2024-06-01'),
(12, 389.99, '2024-06-01', '2025-01-31', '2024-06-01', '2025-02-01'),
(12, 379.99, '2025-02-01', '2028-12-31', '2025-02-01', '2099-12-31'),

-- 3. Wooden Chair (ID 13)
(13, 150.00, '2024-01-01', '2025-03-31', '2024-01-01', '2025-04-01'),
(13, 165.00, '2025-04-01', '2029-12-31', '2025-04-01', '2099-12-31'),

-- 4. Orange Juice 1L (ID 20 - NOU!)
(20, 8.50, '2024-10-01', '2025-05-31', '2024-10-01', '2025-06-01'),
(20, 9.75, '2025-06-01', '2026-12-31', '2025-06-01', '2099-12-31'),

-- 5. Bananas (ID 19)
(19, 6.00, '2024-08-01', '2025-03-31', '2024-08-01', '2025-03-31'),
(19, 5.50, '2024-04-01','2024-07-01', '2025-08-01', '2025-09-01'),
(19, 6.50, '2025-09-01', '2027-12-31', '2025-09-01', '2099-12-31'),

-- 6. Laptop Stand (ID 26)
(26, 85.00, '2024-03-01', '2025-05-31', '2024-03-01', '2025-06-01'),
(26, 75.00, '2025-06-01', '2028-03-01', '2025-06-01', '2099-12-31'),

-- 7. Compostable Plates (ID 44)
(44, 16.50, '2023-10-01', '2024-08-31', '2023-10-01', '2024-09-01'),
(44, 15.50, '2024-09-01', '2025-02-28', '2024-09-01', '2025-03-01'),
(44, 14.99, '2025-03-01', '2027-10-01', '2025-03-01', '2099-12-31'),

-- 8. External HDD 2TB (ID 18)
(18, 250.00, '2024-11-01', '2025-05-31', '2024-11-01', '2025-06-01'),
(18, 235.00, '2025-06-01', '2028-11-01', '2025-06-01', '2099-12-31'),

-- 9. Local Honey (ID 24)
(24, 10.50, '2025-01-10', '2025-09-30', '2025-01-10', '2025-10-01'),
(24, 11.25, '2025-10-01', '2027-01-10', '2025-10-01', '2099-12-31'),

-- 10. Energy Drink (ID 42)
(42, 4.50, '2024-02-01', '2025-03-31', '2024-02-01', '2025-04-01'),
(42, 4.99, '2025-04-01', '2026-02-01', '2025-04-01', '2099-12-31'),

-- Restul produselor
(11, 95.00, '2024-06-01', '2028-12-31', '2024-06-01', '2099-12-31'),
(14, 4.50, '2024-12-01', '2027-12-31', '2024-12-01', '2099-12-31'),
(16, 12.00, '2025-07-01', '2028-12-31', '2025-07-01', '2099-12-31'),
(17, 15.00, '2025-09-01', '2028-03-20', '2025-09-01', '2099-12-31'),
(21, 5.25, '2024-08-01', '2027-07-31', '2024-08-01', '2099-12-31'),
(22, 8.99, '2025-05-01', '2027-05-01', '2025-05-01', '2099-12-31'),
(23, 3.50, '2024-09-01', '2027-09-01', '2024-09-01', '2099-12-31'),
(25, 15.99, '2025-04-01', '2026-04-01', '2025-04-01', '2099-12-31'),
(27, 99.00, '2024-03-01', '2028-03-01', '2024-03-01', '2099-12-31'),
(28, 120.00, '2025-05-15', '2028-05-15', '2025-05-15', '2099-12-31'),
(29, 45.00, '2025-02-10', '2028-02-10', '2025-02-10', '2099-12-31'),
(31, 110.00, '2025-09-01', '2029-09-01', '2025-09-01', '2099-12-31'),
(33, 180.00, '2024-07-01', '2028-07-01', '2024-07-01', '2099-12-31'),
(38, 7.99, '2025-03-01', '2027-03-01', '2025-03-01', '2099-12-31'),
(45, 10.00, '2024-04-01', '2028-04-01', '2024-04-01', '2099-12-31'),
(55, 12.50, '2025-01-01', '2027-01-01', '2025-01-01', '2099-12-31');

INSERT INTO Discounts (discount_id, discount_percent, description, valid_start, valid_end, transaction_start, transaction_end)
VALUES
(1, 10.00, 'Summer Sale', '2024-06-01', '2024-09-01', '2024-05-25', '2024-09-02'),
(2, 20.00, 'Clearance', '2024-12-01', '2025-01-01', '2024-11-20', '2025-01-02'),
(3, 15.00, 'Black Friday', '2025-11-20', '2025-11-30', '2025-09-01', '2099-12-31'),
(4, 5.00, 'New Year Promo', '2026-01-01', '2026-01-10', '2025-10-01', '2099-12-31');

INSERT INTO ProductDiscounts (product_id, discount_id, valid_start, valid_end, transaction_start, transaction_end)
VALUES
-- OLD
(10, 1, '2024-06-01', '2024-09-01', '2024-05-25', '2024-09-02'),
(12, 2, '2024-12-01', '2025-01-01', '2024-11-20', '2025-01-02'),
(32, 3, '2024-11-20', '2024-11-30', '2024-10-01', '2025-01-01'),
(38, 4, '2025-01-01', '2025-01-10', '2024-12-15', '2025-03-01'),
(13, 1, '2024-07-01', '2024-08-31', '2024-06-25', '2024-09-01'),
(26, 2, '2023-12-15', '2024-01-15', '2023-12-01', '2024-01-16'),
(33, 3, '2024-11-20', '2024-11-30', '2024-10-01', '2024-12-01'),
(22, 4, '2025-01-01', '2025-01-10', '2024-12-10', '2025-01-11'),

-- CURENT (transaction_end = '2099-12-31')
(19, 1, '2025-06-01', '2025-09-01', '2025-10-23', '2099-12-31'),
(27, 2, '2025-12-01', '2026-01-01', '2025-10-23', '2099-12-31'),
(11, 3, '2025-11-20', '2025-11-30', '2025-10-23', '2099-12-31'),
(18, 3, '2025-11-20', '2025-11-30', '2025-10-23', '2099-12-31'),
(26, 3, '2025-11-20', '2025-11-30', '2025-10-23', '2099-12-31'),
(34, 3, '2025-11-20', '2025-11-30', '2025-10-23', '2099-12-31'),
(20, 4, '2026-01-01', '2026-01-10', '2025-10-23', '2099-12-31'),
(21, 4, '2026-01-01', '2026-01-10', '2025-10-23', '2099-12-31'),
(41, 4, '2026-01-01', '2026-01-10', '2025-10-23', '2099-12-31'),
(44, 4, '2026-01-01', '2026-01-10', '2025-10-23', '2099-12-31');
