BEGIN TRAN
WAITFOR DELAY '00:00:7'
INSERT INTO Users(Username, Email) values ('username2', 'email@example.com')
COMMIT TRAN


DELETE FROM Users where Username='username2'