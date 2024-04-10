CREATE DATABASE Spotify
USE Spotify

CREATE TABLE Users
(Uid INT PRIMARY KEY IDENTITY,
Username varchar(50) NOT NULL,
Email varchar(100) UNIQUE)

CREATE TABLE Artists
(Aid INT PRIMARY KEY IDENTITY,
Name varchar(50) NOT NULL)

CREATE TABLE Podcasts
(Pid INT PRIMARY KEY IDENTITY,
Name varchar(100) NOT NULL,
NoOfEpisodes INT)

CREATE TABLE Albums
(Aid INT PRIMARY KEY IDENTITY,
ArID INT FOREIGN KEY REFERENCES Artists(Aid),
Name varchar(100) NOT NULL,
NoOfSongs INT CHECK (NoOfSongs > 0),
Year INT CHECK (Year > 1900))

CREATE TABLE Songs
(Sid INT PRIMARY KEY IDENTITY,
Name varchar(100) NOT NULL,
AlID INT FOREIGN KEY REFERENCES Albums(Aid),
Genre varchar(50),
Duration varchar(10))

CREATE TABLE Playlists
(Pid INT PRIMARY KEY IDENTITY,
Uid INT FOREIGN KEY REFERENCES Users(Uid),
Name varchar(100) NOT NULL,
NoOfSongs INT)

CREATE TABLE PlaylistSongs
(Pid INT FOREIGN KEY REFERENCES Playlists(Pid),
Sid INT FOREIGN KEY REFERENCES Songs(Sid),
CONSTRAINT pk_PlaylistSongs PRIMARY KEY(Pid, Sid))

CREATE TABLE PodcastFollowers
(Uid INT FOREIGN KEY REFERENCES Users(Uid),
Pid INT FOREIGN KEY REFERENCES Podcasts(Pid),
NoOfFollowers INT,
CONSTRAINT pk_PodcastFollowers PRIMARY KEY (Uid, Pid))

CREATE TABLE ArtistFollowers
(Uid INT FOREIGN KEY REFERENCES Users(Uid),
Aid INT FOREIGN KEY REFERENCES Artists(Aid),
NoOfFollowers INT,
CONSTRAINT pk_ArtistFOllowers PRIMARY KEY (Uid, Aid))

CREATE TABLE Follows
(Uid1 INT FOREIGN KEY REFERENCES Users(Uid),
Uid2 INT FOREIGN KEY REFERENCES Users(Uid),
NoOfFollowersU2 INT,
CONSTRAINT ck_Valid CHECK (Uid2 != Uid1),
CONSTRAINT pk_Follows PRIMARY KEY (Uid1, Uid2))

CREATE TABLE UserPreferences
(UPid INT FOREIGN KEY REFERENCES Users(Uid),
Ulanguage varchar(50) DEFAULT 'English',
Premium varchar(3) CHECK (Premium='NO' OR Premium='YES') DEFAULT 'NO',
Devices varchar(100),
ListeningActivity varchar(3) CHECK (ListeningActivity='ON' OR ListeningActivity='OFF') DEFAULT 'OFF',
FriendsActivity varchar(3) CHECK (FriendsActivity='ON' OR FriendsActivity='OFF') DEFAULT 'ON',
CONSTRAINT pk_UserPreferences PRIMARY KEY(UPid))


