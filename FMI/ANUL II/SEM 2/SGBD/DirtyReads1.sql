BEGIN TRAN
UPDATE Users SET Email='email' WHERE Uid=24
WAITFOR DELAY '00:00:07'
ROLLBACK TRAN                                                                                                            