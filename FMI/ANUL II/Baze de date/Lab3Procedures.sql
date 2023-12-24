USE Spotify

CREATE PROCEDURE modificaTipColoana 
AS 
ALTER TABLE PodcastFollowers 
ALTER COLUMN NoOfFollowers varchar(50)
PRINT 'Tip coloana modificat cu succes!';

CREATE PROCEDURE undoModificareTipColoana
AS
ALTER TABLE PodcastFollowers 
ALTER COLUMN NoOfFollowers int
PRINT 'Tip coloana modificat cu succes!';


CREATE PROCEDURE addDefaultConstraint
AS
ALTER TABLE ArtistFollowers 
ADD CONSTRAINT df_0 DEFAULT 0
FOR NoOfFollowers
PRINT 'Constrangere default adaugata cu succes!';

CREATE PROCEDURE removeDefaultConstraint
AS
ALTER TABLE ArtistFollowers
DROP CONSTRAINT df_0
PRINT 'Constrangere default stearsa cu succes!';

CREATE PROCEDURE createTable
AS
CREATE TABLE PodcastEpisodes
(Eid INT PRIMARY KEY IDENTITY,
Name varchar(50),
Pid INT
)
PRINT 'Tabel creeat cu succes!';

CREATE PROCEDURE deleteTable
AS
DROP TABLE PodcastEpisodes
PRINT 'Tabel sters cu succes!';

CREATE PROCEDURE addNewColumn
AS
ALTER TABLE PodcastEpisodes
ADD Duration varchar(10)
PRINT 'Coloana adaugata cu succes!';

CREATE PROCEDURE deleteColumn
AS
ALTER TABLE PodcastEpisodes
DROP COLUMN Duration
PRINT 'Coloana stearsa cu succes!';

CREATE PROCEDURE addForeignKeyConstraint
AS
ALTER TABLE PodcastEpisodes
ADD CONSTRAINT fk_PodcastEpisodes_Pid FOREIGN KEY(Pid) REFERENCES Podcasts(Pid)
PRINT 'Cheie straina adaugata cu succes!';

CREATE PROCEDURE deleteForeignKeyConstraint
AS
ALTER TABLE PodcastEpisodes
DROP CONSTRAINT fk_PodcastEpisodes_Pid
PRINT 'Cheie straina stearsa cu succes!';
