SET TRANSACTION ISOLATION LEVEL REPEATABLE READ --SERIALIZABLE
BEGIN TRAN
SELECT * FROM Users
WAITFOR DELAY '00:00:10'
SELECT * FROM Users
COMMIT TRAN