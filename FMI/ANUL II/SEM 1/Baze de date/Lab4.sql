--introducere tabele
INSERT INTO Tables(Name) values ('Podcasts'), ('Playlists'), ('PlaylistSongs')

--creeare view-uri
CREATE VIEW View_Podcasts AS
SELECT * FROM Podcasts
GO

CREATE VIEW View_Playlists AS
SELECT u.Username, p.Name, p.NoOfSongs
FROM Playlists p 
INNER JOIN Users u 
ON p.Uid = u.Uid
GO

CREATE VIEW View_PlaylistSongs AS
SELECT p.Name, s.Genre, COUNT(*) AS NoOfSongs
FROM Songs s 
INNER JOIN PlaylistSongs ps  
ON s.Sid = ps.Sid
INNER JOIN  Playlists p 
ON ps.Pid = p.Pid
GROUP BY s.Genre, p.Name, p.Pid


--adaugare view-uri
INSERT INTO Views(Name) VALUES ('View_Podcasts'), ('View_Playlists'), ('View_PlaylistSongs')

--adaugare nume teste
INSERT INTO Tests(Name) VALUES ('DIV_Podcasts_10'), ('DIV_Podcasts_100'), ('DIV_Podcasts_1000'), ('DIV_Playlists_10'), 
('DIV_Playlists_100'), ('DIV_Playlists_1000'), ('DIV_PlaylistSongs_10'), ('DIV_PlaylistSongs_100'), ('DIV_PlaylistSongs_1000')

--adaugare perechi teste - view-uri
INSERT INTO TestViews(TestID, ViewID) VALUES (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 2), (7, 3), (8, 3), (9, 3)

--adaugare perechi teste-tabele
INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES (1, 1, 10, 1), (2, 1, 100, 2), (3, 1, 1000, 3), (4, 2, 10, 4), 
(5, 2, 100, 5), (6, 2, 1000, 6), (7, 3, 10, 7), (8, 3, 100, 8), (9, 3, 1000, 9)

--creeare functii de inserare
CREATE PROCEDURE insertPodcasts
@noOfRows INT
AS
BEGIN
	DECLARE @n INT = 0
	DECLARE @name VARCHAR(50)
	
	WHILE @n < @noOfRows
	BEGIN
		SET @name = 'insertedPodcast' + CONVERT(VARCHAR(5), @n)
		INSERT INTO Podcasts(Name, NoOfEpisodes) VALUES (@name, 100)
		SET @n = @n + 1
	END 
END	
GO
		
CREATE PROCEDURE insertPlaylists
@noOfRows INT
AS
BEGIN
	DECLARE @n INT = 0
	DECLARE @fk INT
	DECLARE @name VARCHAR(50)
	SELECT TOP 1 @fk = Uid FROM Users ORDER BY NEWID()
	
	WHILE @n < @noOfRows
	BEGIN
		SET @name = 'insertedPlaylist' + CONVERT(VARCHAR(5), @n)
		INSERT INTO Playlists(Uid, Name, NoOfSongs) VALUES (@fk, @name, 10)
		SET @n = @n + 1
	END
END
GO 

CREATE PROCEDURE insertPlaylistSongs
@noOfRows INT
AS
BEGIN
	INSERT INTO PlaylistSongs(Pid, Sid)
		SELECT TOP (@noOfRows) Pid, Sid 
		FROM Playlists CROSS JOIN Songs
		ORDER BY Pid DESC
END

--creeare proceduri de stergere
CREATE PROCEDURE deletePodcasts
AS
DELETE FROM Podcasts WHERE 
Name LIKE 'insertedPodcast%'


CREATE PROCEDURE deletePlaylists
AS
EXECUTE deletePlaylistSongs 
DELETE FROM Playlists WHERE 
Name LIKE 'insertedPLaylist%'


CREATE PROCEDURE deletePlaylistSongs
AS
DELETE FROM PlaylistSongs WHERE 
Pid > 7

--creeare procedura pentru view-uri
CREATE PROCEDURE viewTest
@idTest INT
AS
BEGIN
	DECLARE @viewName VARCHAR(50) = 
	(SELECT v.Name
	FROM Views v INNER JOIN TestViews tv ON tv.ViewID = v.ViewID
	WHERE tv.TestID = @idTest)
	
	DECLARE @comanda NVARCHAR(50) = 'SELECT * FROM ' + @viewName
	EXECUTE (@comanda)
END 

--creeare procedura generala
CREATE PROCEDURE runTests
AS
BEGIN
	DECLARE @idTest INT
	DECLARE @testName VARCHAR(50)
	DECLARE @tableName VARCHAR(50)
	DECLARE @noOfRows INT
	DECLARE @idTable INT
	DECLARE cursorTab CURSOR FORWARD_ONLY FOR
		SELECT t.TestID, t.Name, tb.TableID, tb.Name, NoOfRows
		FROM Tests t INNER JOIN TestTables tt ON t.TestID = tt.TestID
		INNER JOIN Tables tb ON tb.TableID = tt.TableID
		ORDER BY tt.Position
	OPEN cursorTab
	
	FETCH NEXT FROM cursorTab INTO @idTest, @testName, @idTable, @tableName, @noOfRows
	WHILE @@FETCH_STATUS = 0
	BEGIN
		DECLARE @startTime DATETIME
		DECLARE @interTime DATETIME
		DECLARE @endTime DATETIME
		DECLARE @insertProcedure NVARCHAR(50) = 'insert' + @tableName
		DECLARE @deleteProcedure NVARCHAR(50) = 'delete' + @tableName
		
		SET @startTime = GETDATE()
		EXECUTE @deleteProcedure
		EXECUTE @insertProcedure @noOfRows
		SET @interTime = GETDATE()
		EXECUTE viewTest @idTest
		SET @endTime = GETDATE()
		
		INSERT INTO TestRuns(Description, StartAt, EndAt) VALUES (@testName, @startTime, @endTime)
		
		DECLARE @idView INT = 
		(SELECT ViewID FROM TestViews
		WHERE TestID = @idTest)
		DECLARE @idTestRun INT =
		(SELECT TOP 1 TestRunID FROM TestRuns
		WHERE Description = @testName
		ORDER BY TestRunID DESC)
		
		INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt) VALUES (@idTestRun, @idTable, @startTime, @interTime)
		INSERT INTO TestRunViews(TestRunID, ViewID, StartAt, EndAt) VALUES (@idTestRun, @idView, @interTime, @endTime);
	
		FETCH NEXT FROM cursorTab INTO @idTest, @testName, @idTable, @tableName, @noOfRows
	END
	
	CLOSE cursorTab
	DEALLOCATE cursorTab
END

EXECUTE runTests 

SELECT * FROM TestRuns
SELECT * FROM TestRunTables
SELECT * FROM TestRunViews 
		
		
		
		

