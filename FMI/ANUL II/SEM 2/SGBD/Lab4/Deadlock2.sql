--SET DEADLOCK_PRIORITY HIGH
SET DEADLOCK_PRIORITY LOW

BEGIN TRAN
UPDATE Artists SET Name='deadlock2' WHERE Aid=28
WAITFOR DELAY '00:00:10'
UPDATE Users SET Username='deadlock2' WHERE Uid=23
COMMIT TRAN

SELECT * FROM Users
SELECT * FROM Artists