-- TRIGGER SUPPLIERS
CREATE OR REPLACE FUNCTION trg_suppliers_manage_transaction_time()
RETURNS TRIGGER AS $$
BEGIN
  IF current_setting('recursion_guard.in_trigger', true) = 'true' THEN
    RETURN NEW;
  END IF;

  PERFORM set_config('recursion_guard.in_trigger', 'true', true);

  IF TG_OP = 'INSERT' THEN
    NEW.transaction_start := NOW();
    NEW.transaction_end   := '2099-12-31'::timestamp;

  ELSIF TG_OP = 'UPDATE' THEN
    UPDATE suppliers
      SET transaction_end = now() - interval '1 microsecond',
	  	  valid_end = now() - interval '1 microsecond'
      WHERE supplier_id = OLD.supplier_id
        AND transaction_end = '2099-12-31'::timestamp;

    INSERT INTO suppliers (
      supplier_id, name, valid_start, valid_end,
      transaction_start, transaction_end
    )
    VALUES (
      OLD.supplier_id,
      NEW.name,
      now(),
      NEW.valid_end,
      now(),
      '2099-12-31'::timestamp
    );

    RETURN NULL;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_suppliers_transaction
BEFORE INSERT OR UPDATE ON Suppliers
FOR EACH ROW
EXECUTE FUNCTION trg_suppliers_manage_transaction_time();

-- TRIGGER PRODUCTS
CREATE OR REPLACE FUNCTION trg_products_manage_transaction_time()
RETURNS TRIGGER AS $$
BEGIN
    IF current_setting('recursion_guard.in_trigger', true) = 'true' THEN
      RETURN NEW;
    END IF;

    PERFORM set_config('recursion_guard.in_trigger', 'true', true);

    IF TG_OP = 'INSERT' THEN
        NEW.transaction_start := NOW();
        NEW.transaction_end   := '2099-12-31'::timestamp;

    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE Products
        SET transaction_end = NOW() - interval '1 microsecond',
			valid_end = NOW() - interval '1 microsecond'
        WHERE product_id = OLD.product_id
          AND transaction_end = '2099-12-31'::timestamp;

        INSERT INTO Products (
            product_id, supplier_id, name, sku, description,
            valid_start, valid_end, transaction_start, transaction_end
        )
        VALUES (
            OLD.product_id, NEW.supplier_id, NEW.name, NEW.sku, NEW.description,
            now(), NEW.valid_end, NOW(), '2099-12-31'::timestamp
        );

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_products_transaction
BEFORE INSERT OR UPDATE ON Products
FOR EACH ROW EXECUTE FUNCTION trg_products_manage_transaction_time();

-- TRIGGER PRICING RECORDS
CREATE OR REPLACE FUNCTION trg_pricingrecords_manage_transaction_time()
RETURNS TRIGGER AS $$
BEGIN
    IF current_setting('recursion_guard.in_trigger', true) = 'true' THEN
      RETURN NEW;
    END IF;

    PERFORM set_config('recursion_guard.in_trigger', 'true', true);

    IF TG_OP = 'INSERT' THEN
        NEW.transaction_start := NOW();
        NEW.transaction_end   := '2099-12-31'::timestamp;

    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE PricingRecords
        SET transaction_end = NOW() - interval '1 microsecond',
			valid_end = NOW() - interval '1 microsecond'
        WHERE record_id = OLD.record_id
          AND transaction_end = '2099-12-31'::timestamp;

        INSERT INTO PricingRecords (
            product_id, price, valid_start, valid_end,
            transaction_start, transaction_end
        )
        VALUES (
            NEW.product_id, NEW.price, now(), NEW.valid_end,
            NOW(), '2099-12-31'::timestamp
        );

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_pricingrecords_transaction
BEFORE INSERT OR UPDATE ON PricingRecords
FOR EACH ROW EXECUTE FUNCTION trg_pricingrecords_manage_transaction_time();

-- TRIGGER DISCOUNTS
CREATE OR REPLACE FUNCTION trg_discounts_manage_transaction_time()
RETURNS TRIGGER AS $$
BEGIN
    IF current_setting('recursion_guard.in_trigger', true) = 'true' THEN
      RETURN NEW;
    END IF;

    PERFORM set_config('recursion_guard.in_trigger', 'true', true);

    IF TG_OP = 'INSERT' THEN
        NEW.transaction_start := NOW();
        NEW.transaction_end   := '2099-12-31'::timestamp;

    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE Discounts
        SET transaction_end = NOW() - interval '1 microsecond',
			valid_end = NOW() - interval '1 microsecond'
        WHERE discount_id = OLD.discount_id
          AND transaction_end = '2099-12-31'::timestamp;

        INSERT INTO Discounts (
            discount_id, discount_percent, description,
            valid_start, valid_end, transaction_start, transaction_end
        )
        VALUES (
            OLD.discount_id, NEW.discount_percent, NEW.description,
            now(), NEW.valid_end, NOW(), '2099-12-31'::timestamp
        );

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_discounts_transaction
BEFORE INSERT OR UPDATE ON Discounts
FOR EACH ROW EXECUTE FUNCTION trg_discounts_manage_transaction_time();

-- TRIGGER PRODUCT DISCOUNTS
CREATE OR REPLACE FUNCTION trg_productdiscounts_manage_transaction_time()
RETURNS TRIGGER AS $$
BEGIN
    IF current_setting('recursion_guard.in_trigger', true) = 'true' THEN
      RETURN NEW;
    END IF;

    PERFORM set_config('recursion_guard.in_trigger', 'true', true);

    IF TG_OP = 'INSERT' THEN
        NEW.transaction_start := NOW();
        NEW.transaction_end   := '2099-12-31'::timestamp;

    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE ProductDiscounts
        SET transaction_end = NOW() - interval '1 microsecond',
			valid_end = NOW() - interval '1 microsecond'
        WHERE product_id = OLD.product_id
          AND discount_id = OLD.discount_id
          AND transaction_end = '2099-12-31'::timestamp;

        INSERT INTO ProductDiscounts (
            product_id, discount_id, valid_start, valid_end,
            transaction_start, transaction_end
        )
        VALUES (
            OLD.product_id, OLD.discount_id,
            now(), NEW.valid_end,
            NOW(), '2099-12-31'::timestamp
        );

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_productdiscounts_transaction
BEFORE INSERT OR UPDATE ON ProductDiscounts
FOR EACH ROW EXECUTE FUNCTION trg_productdiscounts_manage_transaction_time();