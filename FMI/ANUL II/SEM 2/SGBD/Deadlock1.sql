BEGIN TRAN
UPDATE Users SET Username='deadlock1' WHERE Uid=23
WAITFOR DELAY '00:00:10'
UPDATE Artists SET Name='deadlock1' WHERE Aid=28
COMMIT TRAN

UPDATE Artists SET Name='artist' WHERE Aid=28   
UPDATE Users SET Username='username5' WHERE Uid=23                                                                                                                                                                                                                                                                                                                  