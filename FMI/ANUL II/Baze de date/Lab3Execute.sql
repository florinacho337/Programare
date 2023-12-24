USE Spotify

CREATE TABLE ActualVersion(version INT)
INSERT INTO ActualVersion VALUES (0)
CREATE TABLE Procedures_VersionsDB(procedure_ID INT PRIMARY KEY IDENTITY, procedure_name varchar(50))
CREATE TABLE Opposite_Procedures_VersionsDB(procedure_ID INT PRIMARY KEY IDENTITY, procedure_name varchar(50))

INSERT INTO Procedures_VersionsDB VALUES ('modificaTipColoana'), ('addDefaultConstraint'), ('createTable'), ('addNewColumn'), ('addForeignKeyConstraint')
INSERT INTO Opposite_Procedures_VersionsDB VALUES ('undoModificareTipColoana'), ('removeDefaultConstraint'), ('deleteTable'), ('deleteColumn'), ('deleteForeignKeyConstraint')

CREATE PROCEDURE restoreVersion 
@version INT
AS
BEGIN

	IF (@version < 0 OR @version > 5)
		BEGIN 
			RAISERROR('Versiune invalida!', 16, 1) WITH NOWAIT
			RETURN;
		END
	
	DECLARE @actual_version INT
	DECLARE @function varchar(50)
	SELECT @actual_version = version
	FROM ActualVersion
		
	IF @version = @actual_version
		BEGIN
			RAISERROR('Deja esti in versiunea selectata!', 16, 1) WITH NOWAIT
			RETURN;
		END
		
	
	If @version > @actual_version
		BEGIN

			WHILE @version != @actual_version
			BEGIN

				SET @actual_version = @actual_version + 1
				SELECT @function = procedure_name
				FROM Procedures_VersionsDB 
				Where @actual_version=procedure_ID;

				EXECUTE @function;
			END


			update ActualVersion
			SET version = @version;

			RETURN;

		END
		ELSE
		BEGIN
			WHILE @version != @actual_version
			BEGIN
				SELECT @function = procedure_name
				FROM Opposite_Procedures_VersionsDB 
				WHERE @actual_version = procedure_ID;

				EXECUTE @function;

				SET @actual_version = @actual_version - 1;
			END
			update ActualVersion
			SET version = @version;

			RETURN;
		END
		RETURN;
END