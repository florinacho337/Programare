--playlist-uri si melodiile continute
SELECT p.Name as Playlist, s.Name as Song, a.Name as Album, s.Duration
FROM Playlists p , PlaylistSongs ps , Songs s , Albums a 
WHERE p.Pid = ps.Pid AND s.Sid = ps.Sid AND a.Aid = s.AlID

--userii si artistii urmariti de fiecare
SELECT u.Username as 'User', a.Name as FollowedArtists
FROM Users u INNER JOIN ArtistFollowers af ON u.Uid = af.Uid
INNER JOIN Artists a ON a.Aid = af.Aid

--userii si podcasturile urmarite de fiecare
SELECT u.Username as 'User', p.Name as FollowedPodcasts
FROM Podcasts p INNER JOIN PodcastFollowers pf ON p.Pid = pf.Pid 
INNER JOIN Users u ON u.Uid = pf.Uid

--artistii si melodiile fiecaruia
SELECT ar.Name as Artist, al.Name as Album, s.Name as Song, s.Duration
FROM Artists ar, Albums al, Songs s 
WHERE al.ArID = ar.Aid AND s.AlID = al.Aid 
ORDER BY ar.Aid  

--numarul de melodii al fiecarui artist
SELECT ar.Name as Artist, COUNT(*) as NoOfSongs 
FROM Songs s, Artists ar, Albums al 
WHERE al.ArID = ar.Aid AND s.AlID = al.Aid
GROUP BY ar.Name 

--userii si prietenii carora le pot urmari activitatea
SELECT u1.Username as 'User', u2.Username as FriendsShown
FROM Users u1, Follows f, Users u2, UserPreferences up1, UserPreferences up2
WHERE u1.Uid = f.Uid1 AND u2.Uid = f.Uid2 AND up1.FriendsActivity = 'ON' AND up2.ListeningActivity = 'ON' AND u1.Uid = up1.UPid AND u2.Uid = up2.UPid 

--podcasturile si limbile userilor care le urmaresc
SELECT DISTINCT p.Name as Podcast, up.Ulanguage as UserLanguage  
FROM Podcasts p, PodcastFollowers pf, UserPreferences up 
WHERE p.Pid = pf.Pid AND up.UPid = pf.Uid

--playlist-urile care au mai mult de jumatate din melodii de genul 'Alternative'
SELECT p.Name as Playlist, p.NoOfSongs, COUNT(*) as AlternativeSongs
FROM Playlists p INNER JOIN PlaylistSongs ps ON p.Pid = ps.Pid 
INNER JOIN Songs s ON s.Sid = ps.Sid AND s.Genre = 'Alternative'
GROUP BY p.Name, p.NoOfSongs 
HAVING COUNT(*) >= p.NoOfSongs / 2

--melodiile fiecarui user care sunt aparute inainte de 2010
SELECT DISTINCT u.Username as 'User', s.Name as Song, a.[Year]
FROM Users u, Songs s, Albums a, Playlists p, PlaylistSongs ps
WHERE p.Uid = u.Uid AND p.Pid = ps.Pid AND s.Sid = ps.Sid AND s.AlID = a.Aid AND a.Year < 2010

--artistii care au mai mult de 10 melodii per album in medie
SELECT ar.Name as Artist, COUNT(*) as Albums, AVG(NoOfSongs) as AvgSongsPerAlbum
FROM Artists ar INNER JOIN Albums al ON al.ArID = ar.Aid
GROUP BY ar.Name
HAVING AVG(NoOfSongs) >= 10

