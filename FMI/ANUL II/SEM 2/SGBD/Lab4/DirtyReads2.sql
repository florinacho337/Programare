SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED --COMMITTED
BEGIN TRAN
SELECT * FROM Users
WAITFOR DELAY '00:00:10'
SELECT * FROM Users
COMMIT TRAN                                                                                                                                                   