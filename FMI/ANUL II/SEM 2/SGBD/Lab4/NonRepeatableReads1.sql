INSERT INTO Users(Username, Email) values ('username2', 'email@example.com')
BEGIN TRAN
WAITFOR DELAY '00:00:7'
UPDATE Users SET Email='email' WHERE Username='username2'
COMMIT TRAN

DELETE FROM Users where Username='username2'