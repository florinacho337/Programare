IF OBJECT_ID(N'validateUsername', N'FN') IS NOT NULL
	DROP FUNCTION validateUsername

CREATE FUNCTION validateUsername (@username VARCHAR(50))
RETURNS INT
AS
BEGIN
	IF @username IS NOT NULL
		RETURN 1
	RETURN 0
END

IF OBJECT_ID(N'validateEmail', N'FN') IS NOT NULL
	DROP FUNCTION validateEmail

CREATE FUNCTION validateEmail (@email VARCHAR(50))
RETURNS INT
AS
BEGIN
	IF @email IS NOT NULL
		RETURN 1
	RETURN 0
END

CREATE OR ALTER PROCEDURE CRUD_Users
@username VARCHAR(50),
@email VARCHAR(50),
@NoOfRows INT = 1
AS 
BEGIN 
	SET NOCOUNT ON 
	IF (dbo.validateUsername(@username) = 1 AND
		dbo.validateEmail(@email) = 1)
	BEGIN 
		--create 
		DECLARE @n INT = 0
		WHILE @n < @NoOfRows
		BEGIN 
			INSERT INTO Users(username, email) VALUES (@username, @email + CONVERT(VARCHAR(5), @n))
			SET @n = @n + 1
		END
		
		--read
		SELECT * FROM Users ORDER BY Username
		
		--update
		UPDATE Users 
		SET Username = @username + '_CRUD'
		WHERE Username = @username
		
		SELECT * FROM Users ORDER BY Username 
		
		--delete
		DELETE FROM Users 
		WHERE Username = @username + '_CRUD'
		
		SELECT * FROM Users ORDER BY Username 
		PRINT 'Operatiile CRUD pentru User au fost finalizate cu succes!'
	END
	ELSE 
		RAISERROR('Datele de intrare nu sunt valide!', 16, 1)
END

SELECT * FROM Users
EXEC CRUD_Users 'TEST', 'email', 3 

IF OBJECT_ID(N'validateName', N'FN') IS NOT NULL
	DROP FUNCTION validateName

CREATE FUNCTION validateName (@name VARCHAR(50))
RETURNS INT
AS
BEGIN
	IF @name IS NOT NULL
		RETURN 1
	RETURN 0
END

CREATE OR ALTER PROCEDURE CRUD_Artists
@name VARCHAR(50),
@NoOfRows INT = 1
AS 
BEGIN 
	SET NOCOUNT ON 
	IF dbo.validateName(@name) = 1
	BEGIN 
		--create 
		DECLARE @n INT = 0
		WHILE @n < @NoOfRows
		BEGIN 
			INSERT INTO Artists VALUES (@name)
			SET @n = @n + 1
		END
		
		--read
		SELECT * FROM Artists ORDER BY Name 
		
		--update
		UPDATE Artists 
		SET Name = @name + '_CRUD'
		WHERE Name = @name
		
		SELECT * FROM Artists ORDER BY Name 
		
		--delete
		DELETE FROM Artists  
		WHERE Name = @name + '_CRUD'
		
		SELECT * FROM Artists ORDER BY Name 
		PRINT 'Operatiile CRUD pentru Artist au fost finalizate cu succes!'
	END
	ELSE 
		RAISERROR('Datele de intrare nu sunt valide!', 16, 1)
END

SELECT * FROM Artists
EXEC CRUD_Artists 'TEST', 10

IF OBJECT_ID(N'validateNoOfFollowers', N'FN') IS NOT NULL
	DROP FUNCTION validateNoOfFollowers

CREATE FUNCTION validateNoOfFollowers (@noOfFollowers INT)
RETURNS INT
AS
BEGIN
	IF @noOfFollowers >= 0
		RETURN 1
	RETURN 0
END

CREATE OR ALTER PROCEDURE CRUD_ArtistFollowers
@UserID INT,
@ArtistID INT,
@NoOfFollowers INT
AS 
BEGIN 
	SET NOCOUNT ON 
	IF dbo.validateNoOfFollowers(@NoOfFollowers) = 1
	BEGIN 
		--create  
		INSERT INTO ArtistFollowers VALUES (@UserID, @ArtistID, @NoOfFollowers)
			
		
		--read
		SELECT * FROM ArtistFollowers ORDER BY NoOfFollowers  
		
		--update
		UPDATE ArtistFollowers 
		SET NoOfFollowers  = @NoOfFollowers + 15
		WHERE Uid = @UserID AND Aid = @ArtistID
		
		SELECT * FROM ArtistFollowers ORDER BY NoOfFollowers  
		
		--delete
		DELETE FROM ArtistFollowers
		WHERE Uid = @UserID AND Aid = @ArtistID
		
		SELECT * FROM ArtistFollowers ORDER BY NoOfFollowers  
		PRINT 'Operatiile CRUD pentru ArtistFollowers au fost finalizate cu succes!'
	END
	ELSE 
		RAISERROR('Datele de intrare nu sunt valide!', 16, 1)
END

SELECT * FROM ArtistFollowers
EXEC CRUD_ArtistFollowers 3, 8, 2975


CREATE OR ALTER VIEW ViewFollowedArtists
AS
SELECT u.Username as 'User', a.Name as FollowedArtists
FROM Users u INNER JOIN ArtistFollowers af ON u.Uid = af.Uid
INNER JOIN Artists a ON a.Aid = af.Aid

CREATE OR ALTER VIEW ViewGmailUsers
AS
SELECT a.Name, COUNT(*) as GmailUsers
FROM Artists a INNER JOIN ArtistFollowers af ON a.Aid = af.Aid
INNER JOIN Users u ON u.Uid = af.Aid
WHERE u.Email LIKE '%gmail.com'
GROUP BY a.Name

--User
CREATE NONCLUSTERED INDEX N_idx_Username ON Users(Username)
CREATE NONCLUSTERED INDEX N_idx_Email ON Users(Email)
CREATE NONCLUSTERED INDEX N_idx_Uid ON Users(Uid)

--Artist
CREATE NONCLUSTERED INDEX N_idx_Name ON Artists(Name)
CREATE NONCLUSTERED INDEX N_idx_Aid ON Artists(Aid)

--ArtistFollowers
CREATE NONCLUSTERED INDEX N_idx_Uid ON ArtistFollowers(Uid)
CREATE NONCLUSTERED INDEX N_idx_Aid ON ArtistFollowers(Aid)
CREATE NONCLUSTERED INDEX N_idx_NoOfFollowers ON ArtistFollowers(NoOfFollowers)

--Drop

--DROP INDEX N_idx_Username ON Users
--DROP INDEX N_idx_Email ON Users
--DROP INDEX N_idx_Uid ON Users
--
--DROP INDEX N_idx_Name ON Artists
--DROP INDEX N_idx_Aid ON Artists
--
--DROP INDEX N_idx_Uid ON ArtistFollowers
--DROP INDEX N_idx_Aid ON ArtistFollowers
--DROP INDEX N_idx_NoOfFollowers ON ArtistFollowers

--SET SHOWPLAN_ALL ON


