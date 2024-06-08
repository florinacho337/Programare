USE Spotify

CREATE TABLE log_table
(
	id INT PRIMARY KEY IDENTITY,
	operation_type VARCHAR(20),
	table_name VARCHAR(20),
	execution_time DATETIME
)
GO

CREATE OR ALTER FUNCTION validateText (@text VARCHAR(100))
RETURNS BIT
AS
BEGIN
	DECLARE @flag BIT
	SET @flag = 1
	IF @text IS NULL OR @text = ''
		SET @flag = 0
	RETURN @flag
END
GO

CREATE OR ALTER FUNCTION validateNumber (@number INT)
RETURNS BIT
AS
BEGIN
	DECLARE @flag BIT
	SET @flag = 1
	IF @number is NULL or @number < 0
		SET @flag = 0
	RETURN @flag
END
GO

--task 1
CREATE OR ALTER PROCEDURE addUserArtist(@username VARCHAR(100), @email VARCHAR(100), @artistName VARCHAR(50))
AS
BEGIN
	BEGIN TRAN
	BEGIN TRY
		IF dbo.validateText(@username) <> 1
		BEGIN
			PRINT 'Invalid username!'
			RAISERROR('Invalid username!', 14, 1)
		END
		IF dbo.validateText(@email) <> 1
		BEGIN
			PRINT 'Invalid email!'
			RAISERROR('Invalid email!', 14, 1)
		END

		INSERT INTO Users(Username, Email) VALUES (@username, @email)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT', 'Users', CURRENT_TIMESTAMP)

		IF dbo.validateText(@artistName) <> 1
		BEGIN
			PRINT 'Invalid artist name!'
			RAISERROR('Invalid artist name!', 14, 1)
		END

		INSERT INTO Artists(Name) VALUES (@artistName)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT', 'Artists', CURRENT_TIMESTAMP)

		DECLARE @id_user INT, @id_artist INT
		SET @id_user = (SELECT MAX(Uid) from Users)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('SELECT', 'Users', CURRENT_TIMESTAMP)

		SET @id_artist = (SELECT MAX(Aid) from Artists)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('SELECT', 'Artists', CURRENT_TIMESTAMP)

		INSERT INTO ArtistFollowers(Uid, Aid, NoOfFollowers) VALUES (@id_user, @id_artist, 1)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT', 'ArtistFollowers', CURRENT_TIMESTAMP)

		COMMIT TRAN
		PRINT 'Transaction commited'
	END TRY
	BEGIN CATCH
		ROLLBACK TRAN
		PRINT ERROR_MESSAGE()
		PRINT 'Transaction rollbacked'
	END CATCH
END
GO

--with succes
EXEC addUserArtist 'username4', 'email@example.ro', 'artist3'
SELECT * FROM log_table
SELECT * FROM Users
SELECT * FROM Artists
SELECT * FROM ArtistFollowers

--without succes
EXEC addUserArtist '', '', ''
SELECT * FROM log_table
SELECT * FROM Users
SELECT * FROM Artists
SELECT * FROM ArtistFollowers

--task 2
CREATE OR ALTER PROCEDURE addUserArtist2(@username VARCHAR(100), @email VARCHAR(100), @artistName VARCHAR(50))
AS
BEGIN
	DECLARE @err BIT
	SET @err = 0
	BEGIN TRAN
	BEGIN TRY
		IF dbo.validateText(@username) <> 1
		BEGIN
			PRINT 'Invalid username!'
			RAISERROR('Invalid username!', 14, 1)
		END
		IF dbo.validateText(@email) <> 1
		BEGIN
			PRINT 'Invalid email!'
			RAISERROR('Invalid email!', 14, 1)
		END

		INSERT INTO Users(Username, Email) VALUES (@username, @email)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT', 'Users', CURRENT_TIMESTAMP)

		COMMIT TRAN
		PRINT 'Transaction commited'
	END TRY
	BEGIN CATCH
		ROLLBACK TRAN
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT ERROR', 'Users', CURRENT_TIMESTAMP)
		PRINT 'Transaction rollbacked'
		SET @err = 1
	END CATCH

	BEGIN TRAN
	BEGIN TRY
		IF dbo.validateText(@artistName) <> 1
		BEGIN
			PRINT 'Invalid artist name!'
			RAISERROR('Invalid artist name!', 14, 1)
		END

		INSERT INTO Artists(Name) VALUES (@artistName)
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT', 'Artists', CURRENT_TIMESTAMP)

		COMMIT TRAN
		PRINT 'Transaction commited'
	END TRY
	BEGIN CATCH
		ROLLBACK TRAN
		INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT ERROR', 'Artists', CURRENT_TIMESTAMP)
		PRINT 'Transaction rollbacked'
		SET @err = 1
	END CATCH

	IF @err = 1
		RETURN

	DECLARE @id_user INT, @id_artist INT
	SET @id_user = (SELECT MAX(Uid) from Users)
	INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('SELECT', 'Users', CURRENT_TIMESTAMP)

	SET @id_artist = (SELECT MAX(Aid) from Artists)
	INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('SELECT', 'Artists', CURRENT_TIMESTAMP)

	INSERT INTO ArtistFollowers(Uid, Aid, NoOfFollowers) VALUES (@id_user, @id_artist, 1)
	INSERT INTO log_table(operation_type, table_name, execution_time) VALUES ('INSERT', 'ArtistFollowers', CURRENT_TIMESTAMP)

	PRINT 'Follower adaugat'
END
GO

EXEC addUserArtist2 'username2', 'email@example.com', '' -- second not good
EXEC addUserArtist2 '', '', 'artist3' -- frist not good
SELECT * FROM log_table
SELECT * FROM Users
SELECT * FROM Artists
SELECT * FROM ArtistFollowers