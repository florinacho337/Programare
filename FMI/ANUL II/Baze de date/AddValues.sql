USE Spotify

INSERT INTO Users(Username, Email)
VALUES ('florWIN', 'florin422004@yahoo.com'), ('andr3w', 'andreas_neagu@gmail.com'), ('teuo', 'teodor.dumitru7@gmail.com'), 
('flordecires', 'florentina.horvath9@gmail.com'), ('steeeefi', 'stefania.marin60@yahoo.com'), ('bobo2005', 'bogdan_micu@yahoo.com'), 
('eemas', 'timotei.pop@gmail.com'), ('Maslina', 'oliviapop99@yahoo.com'), ('Domynis', 'domi.bacs@gmail.com'), ('Claus', 'claudiu.ene25@yahoo.com')

INSERT INTO UserPreferences(UPid, Ulanguage, Devices, ListeningActivity)
VALUES (1, 'Romanian', 'Phone, Laptop, TV', 'ON')

INSERT INTO UserPreferences(UPid, Ulanguage, Devices, ListeningActivity)
VALUES (5, 'Romanian', 'Phone, Laptop', 'ON'), (9, 'English', 'Phone, Laptop', 'ON'),(10, 'Romanian', 'Phone, Laptop, Car', 'ON')

INSERT INTO UserPreferences(UPid, Devices, FriendsActivity)
VALUES (3, 'Phone, Laptop', 'OFF'), (6, 'Laptop', 'OFF')

INSERT INTO UserPreferences(UPid, Premium, Devices, ListeningActivity)
VALUES (2, 'YES', 'Phone, Laptop', 'ON'), (4, 'YES', 'Phone, Laptop, TV', 'ON')

INSERT INTO UserPreferences(UPid, Ulanguage, Devices, ListeningActivity, FriendsActivity)
VALUES (7, 'Spanish', 'Phone', 'ON', 'OFF'), (8, 'Italian', 'Laptop, TV', 'ON', 'OFF')

INSERT INTO Artists(Name)
VALUES ('byron'), ('COMA'), ('Nothing But Thieves'), ('Ian'), ('Muse'), ('Coldplay'), ('The Mono Jacks'), ('Dora Gaitanovici'), ('Deliric'),
('Tash Sultana'), ('Subcarpati'), ('Ed Sheeran'), ('The Weeknd'), ('Valeria Stoica'), ('Metallica'), ('Arctic Monkeys')

INSERT INTO Artists(Name)
VALUES ('Madalina Paval')

INSERT INTO Albums(ArID, Name, NoOfSongs, Year)
VALUES (1, 'Efemeride', 10, 2023), (11, 'Satele Unite ale Balcanilor', 13, 2016), (9, 'Deliric X Silent Strike', 17, 2016), (1, 'Noua', 12, 2019), 
(6, 'Parachutes', 10, 2000), (9, 'Deliric X Silent Strike II', 16, 2019),  (1, 'Marea', 1, 2015), (2, 'Nerostitele', 14, 2006), 
(14, 'I Don''t Like Roses', 9, 2020), (2, 'Acordul parintilor', 6, 2023), (7, 'Norul noua', 10, 2023), (2, 'Orizont', 10, 2016), 
(11, 'Piele de Gaina', 16, 2014), (2, 'Light', 12, 2008), (6, 'Mylo Xyloto', 14, 2011), (3, 'Moral Panic (The Complete Edition)', 16, 2021), 
(16, 'AM', 12, 2013), (3, 'Broken Machine (Deluxe)', 15, 2017), (5, 'Black Holes and Revelations', 12, 2006), (7, 'Gloria', 11, 2020), 
(5, 'Absolution', 15, 2004), (7, 'Usor Distorsionat', 10, 2017), (8, 'Descantec', 9, 2022), (9, 'Inspectia Tehnica Periodica', 21, 2011), 
(17, 'Roiesc', 8, 2022), (16, 'Favourite Worst Nightmare', 12, 2007), (17, 'Oamenii se fac dor', 7, 2019), (11, 'Zori si Asfintit', 18, 2018)

INSERT INTO Albums(ArID, Name, NoOfSongs, Year)
VALUES (14, 'The Will', 1, 2023), (14, 'All We Wanna Do', 1, 2023)

INSERT INTO ArtistFollowers(Uid, Aid, NoOfFollowers)
VALUES (1, 1, 19225), (1, 2, 11224), (1, 3, 1047614), (1, 8, 2975), (1, 9, 87929), (1, 11, 110006), (1, 14, 10413), (1, 17, 4392), (2, 2, 11224), 
(2, 5, 7682678), (2, 6, 47713116), (2, 12, 114970531), (3, 4, 453414), (4, 1, 19225), (4, 7, 16803), (4, 8, 2975), (4, 10, 1626206), 
(4, 13, 73623354), (4, 17, 4392), (5, 3, 1047614), (5, 4, 453414), (5, 6, 47713116), (5, 7, 16803), (5, 16, 22069685), (6, 2, 11224),
(6, 3, 1047614), (6, 5, 7682678), (6, 8, 2975), (6, 15, 26117955), (7, 3, 1047614), (7, 4, 453414), (7, 9, 87929), (7, 10, 1626206), (7, 11, 110006), 
(7, 13, 73623354), (8, 1, 19225), (8, 3, 1047614), (8, 6, 47713116), (8, 11, 110006), (8, 12, 114970531), (8, 13, 73623354), (8, 15, 26117955), 
(9, 1, 19225), (9, 2, 11224), (9, 6, 47713116), (9, 15, 26117955), (9, 16, 22069685), (10, 4, 453414), (10, 6, 47713116), (10, 9, 87929), 
(10, 12, 114970531), (10, 13, 73623354), (10, 16, 22069685)

INSERT INTO Follows(Uid1, Uid2, NoOfFollowersU2)
VALUES (1, 2, 10)

INSERT INTO Follows(Uid1, Uid2, NoOfFollowersU2)
VALUES (1, 4, 22), (1, 5, 3), (1, 7, 19), (1, 9, 7), (2, 3, 16), (2, 6, 67), (2, 7, 19), (2, 8, 14), (2, 10, 11)

INSERT INTO Follows(Uid1, Uid2, NoOfFollowersU2)
VALUES (3, 1, 15), (3, 5, 3), (3, 6, 67), (3, 10, 11), (4, 1, 15), (4, 2, 10), (4, 8, 14), (4, 9, 7), (5, 1, 15), (5, 9, 7), (6, 2, 10), 
(6, 3, 16), (6, 8, 14), (7, 1, 15), (7, 2, 10), (7, 3, 16), (7, 10, 11), (8, 1, 15), (8, 2, 10), (8, 4, 22), (8, 6, 67), (8, 9, 7), 
(8, 10, 11), (9, 1, 15), (9, 4, 22), (9, 5, 3), (9, 8, 14), (10, 1, 15), (10, 2, 10), (10, 3, 16), (10, 6, 67), (10, 7, 19), (10, 8, 14)

INSERT INTO Podcasts(Name, NoOfEpisodes)
VALUES ('Mind Arhitect', 91), ('George Buhnici | #IGDLCC', 201), ('Retrospective Agile', 28), ('MCN Podcast', 45), ('Vin de-o poveste', 133),
('Vocea Natiei', 201), ('Recorder Talks', 86), ('Fain & Simplu Podcast', 160), ('Huberman Lab', 124), ('TED Talks Daily', 227)

INSERT INTO PodcastFollowers(Uid, Pid, NoOfFollowers)
VALUES (1, 1, 35867), (1, 2, 87954), (1, 6, 29845), (1, 9, 589442), (2, 3, 545), (2, 4, 15447), (2, 6, 29845), (2, 10, 729084), (3, 1, 35867),
(3, 5, 9487), (3, 6, 29845), (3, 8, 31299), (4, 3, 545), (4, 4, 15447), (4, 8, 31299), (4, 10, 729084), (5, 2, 87954), (5, 4, 15447), (5, 7, 12335),
(5, 8, 31299), (6, 1, 35867), (6, 5, 9487), (6, 6, 29845), (6, 9, 589442), (6, 10, 729084), (7, 2, 87954), (7, 4, 15447), (7, 5, 9487), (7, 8, 31299),
(8, 1, 35867), (8, 3, 545), (8, 4, 15447), (8, 7, 12335), (9, 2, 87954), (9, 4, 15447), (9, 5, 9487), (9, 6, 29845), (10, 3, 545), (10, 7, 12335),
(10, 8, 31299), (10, 10, 729084)

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Cine sunt eu sa ma opun?', 1, 'Alternative', '3:23'), ('Monstrul de sub pat', 1, 'Alternative', '4:24'), ('FMR', 1, 'Alternative', '4:27'),
('Fericiti mereu', 1, 'Alternative', '4:03'), ('Cadou', 1, 'Alternative', '4:01'), ('Prea tarziu', 1, 'Alternative', '4:45'), 
('Incurcaturi', 1, 'Alternative', '4:22'), ('Memento', 1, 'Alternative', '5:37'), ('Oricat ai vrea sa fii mai mult', 1, 'Alternative', '3:43'),
('In infern', 1, 'Alternative', '10:50') 

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Rabda inima', 2, 'Underground, Hip-Hop, Folklore', '5:55'), ('Dintr-o Lume In Alta Lume - Intro', 2, 'Underground, Hip-Hop, Folklore', '5:44'), 
('De Dor Si De Bucurie', 2, 'Underground, Hip-Hop, Folklore', '5:36'), ('Vremea Mea', 2, 'Underground, Hip-Hop, Folklore', '5:37'), 
('Un Cati Un', 2, 'Underground, Hip-Hop, Folklore', '3:19'), ('Sunet Vechi', 2, 'Underground, Hip-Hop, Folklore', '5:01'), 
('Romanul Nu Moare', 2, 'Underground, Hip-Hop, Folklore', '3:41'), ('Tumbe, Tumbe', 2, 'Underground, Hip-Hop, Folklore', '5:37'), 
('Lunea Tahina', 2, 'Underground, Hip-Hop, Folklore', '6:46'), ('Balada Lui Gruia', 2, 'Underground, Hip-Hop, Folklore', '7:16'), 
('Doina', 2, 'Underground, Hip-Hop, Folklore', '3:49'), ('Outro', 2, 'Underground, Hip-Hop, Folklore', '4:33'), 
('Cata nedreptate', 2, 'Underground, Hip-Hop, Folklore', '4:27')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Antidot', 3, 'Hip-Hop, Electronic', '3:39'), ('Cursa', 3, 'Hip-Hop, Electronic', '3:18'), ('Trecator', 3, 'Hip-Hop, Electronic', '3:40'),
('Panopticon', 3, 'Hip-Hop, Electronic', '2:08'), ('Maine', 3, 'Hip-Hop, Electronic', '3:22'), ('Eroare', 3, 'Hip-Hop, Electronic', '3:36'),
('Tesla', 3, 'Hip-Hop, Electronic', '3:30'), ('Porc', 3, 'Hip-Hop, Electronic', '2:51'), ('Venin', 3, 'Hip-Hop, Electronic', '2:59'),
('Doua', 3, 'Hip-Hop, Electronic', '3:47'), ('Simian', 3, 'Hip-Hop, Electronic', '3:54'), ('$Efu', 3, 'Hip-Hop, Electronic', '3:38'),
('Independent', 3, 'Hip-Hop, Electronic', '2:43'), ('Plastic', 3, 'Hip-Hop, Electronic', '2:45'), ('Orasul', 3, 'Hip-Hop, Electronic', '3:23'),
('Gaia', 3, 'Hip-Hop, Electronic', '3:20'), ('Alpha', 3, 'Hip-Hop, Electronic', '2:19')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Acasa', 4, 'Alternative', '5:10'), ('Consumatori De Vise', 4, 'Alternative', '4:36'), ('Azi', 4, 'Alternative', '4:23'),
('Apa si Cer', 4, 'Alternative', '5:00'), ('Continuum', 4, 'Alternative', '5:50'), ('Fara Cuvinte', 4, 'Alternative', '3:02'),
('Anima', 4, 'Alternative', '3:49'), ('Sobolani Si Ciocoi', 4, 'Alternative', '4:15'), ('Razi', 4, 'Alternative', '4:24'),
('El Dorado', 4, 'Alternative', '4:09'), ('Noua', 4, 'Alternative', '5:17'), ('Cantec De Leagan', 4, 'Alternative', '4:49')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Don''t Panic', 5, 'Alternative', '2:16'), ('Shiver', 5, 'Alternative', '5:04'), ('Spies', 5, 'Alternative', '5:18'),
('Sparks', 5, 'Alternative', '3:47'), ('Yellow', 5, 'Alternative', '4:26'), ('Trouble', 5, 'Alternative', '4:33'),
('Parachutes', 5, 'Alternative', '0:46'), ('High Speed', 5, 'Alternative', '4:16'), ('We Never Change', 5, 'Alternative', '4:09'),
('Everything''s Not Lost - Includes Hidden Track ''Life Is For Living''', 5, 'Alternative', '7:16')

INSERT INTO Songs (Name, AlID, Genre, Duration)
VALUES ('Cine', 6, 'Hip-Hop, Electronic', '2:26'), ('Van Gogh', 6, 'Hip-Hop, Electronic', '2:52'), ('Tacerea E De Aur', 6, 'Hip-Hop, Electronic', '3:42'),
('Azi', 6, 'Hip-Hop, Electronic', '2:46'), ('Cernobil', 6, 'Hip-Hop, Electronic', '2:07'), ('Alarma', 6, 'Hip-Hop, Electronic', '2:10'),
('Romania Vrea Sa Ma Ucida', 6, 'Hip-Hop, Electronic', '3:07'), ('Am Visat Ca Schimbam Lumea', 6, 'Hip-Hop, Electronic', '3:09'),
('Omul Serii', 6, 'Hip-Hop, Electronic', '3:19'), ('Ceata', 6, 'Hip-Hop, Electronic', '2:52'), ('Zambim Fals', 6, 'Hip-Hop, Electronic', '3:21'),
('Tras Pe Dreapta', 6, 'Hip-Hop, Electronic', '3:29'), ('Cioburi De Mine', 6, 'Hip-Hop, Electronic', '3:30'), 
('Ce Crezi Tu', 6, 'Hip-Hop, Electronic', '3:25'), ('La Munca!', 6, 'Hip-Hop, Electronic', '2:58'), ('In Jurul Soarelui', 6, 'Hip-Hop, Electronic', '3:03')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Marea', 7, 'Alternative', '3:51'), ('All We Wanna Do', 30, 'Indie', '3:06'), ('The Will', 29, 'Indie', '2:10'), ('Be My Friend', 9, 'Indie', '3:09'),
('Distante', 9, 'Indie', '4:15'), ('Empty Air', 9, 'Indie', '3:00'), ('Get Back', 9, 'Indie', '4:00'), ('Gravity', 9, 'Indie', '3:47'), 
('Just a Boy', 9, 'Indie', '3:31'), ('Poate', 9, 'Indie', '3:32'), ('Remember', 9, 'Indie', '4:14'), ('The Writer', 9, 'Indie', '3:55')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Hectic', 8, 'Rock', '2:49'), ('Mai presus de cuvinte', 8, 'Rock', '4:01'), ('Canta-mi povestea', 8, 'Rock', '3:54'), ('Urmarirea', 8, 'Rock', '1:33'), 
('O zi dupa', 8, 'Rock', '4:23'), ('Culori', 8, 'Rock', '4:14'), ('Treci', 8, 'Rock', '4:20'), ('Maini catre cer', 8, 'Rock', '3:29'), 
('Oriunde oricum', 8, 'Rock', '4:10'), ('Coboara-ma-n Rai', 8, 'Rock', '3:49'), ('Pentru o raza-n orizont', 8, 'Rock', '4:18'), 
('Trei minute', 8, 'Rock', '4:13'), ('Canta-mi povestea - Acustic', 8, 'Rock', '3:51'), ('Un loc sa ajung', 8, 'Rock', '5:17')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Aurora', 10, 'Rock', '2:41'), ('NYX', 10, 'Rock', '3:50'), ('Iza', 10, 'Rock', '3:53'), ('Calista', 10, 'Rock', '3:33'), 
('Naufragii(feat Maru)', 10, 'Rock', '3:25'), ('Lauri', 10, 'Rock', '4:08'), ('Cumparator', 27, 'Urban Folklore', '4:31'), 
('Tot de Dor', 27, 'Urban Folklore', '4:00'), ('Canta-mi Doina', 27, 'Urban Folklore', '3:19'), ('Nu Te Supara, Neicuta', 27, 'Urban Folklore', '4:19'),
('Cata-ti, dorule, alt loc!', 27, 'Urban Folklore', '4:22'), ('Tu stii ce stii', 27, 'Urban Folklore', '4:17'), ('Lumina si Dorul', 27, 'Urban Folklore', '4:52')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('O sa incep de luni', 11, 'Alternative', '3:12'), ('Rauri albe', 11, 'Alternative', '5:25'), ('Un semn', 11, 'Alternative', '4:32'), 
('Aici acum', 11, 'Alternative', '5:29'), ('Undeva', 11, 'Alternative', '5:27'), ('Calator', 11, 'Alternative', '5:30'), ('Urgent', 11, 'Alternative', '6:06'),
('Spune', 11, 'Alternative', '5:12'), ('Mai stai un pic', 11, 'Alternative', '5:10'), ('Somn usor', 11, 'Alternative', '4:18')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Orizont', 12, 'Rock', '3:36'), ('Un semn', 12, 'Rock', '4:00'), ('Dor', 12, 'Rock', '3:51'), ('Delicii', 12, 'Rock', '3:44'), ('Vezi', 12, 'Rock', '4:10'),
('Montagne Russe', 12, 'Rock', '4:21'), ('Document', 12, 'Rock', '4:19'), ('Chip', 12, 'Rock', '4:50'), ('Cel mai frumos loc de pe pamant', 12, 'Rock', '4:19'),
('La hotar', 12, 'Rock', '4:07')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Pe La Noi Prin Babilon', 13, 'Underground, Hip-Hop, Folklore', '4:31'), ('Codrule, Marite Domn', 13, 'Underground, Hip-Hop, Folklore', '3:41'),
('Avion Cu Motor', 13, 'Underground, Hip-Hop, Folklore', '3:28'), ('Sarpe De Dudau', 13, 'Underground, Hip-Hop, Folklore', '3:47'), 
('Interludiu', 13, 'Underground, Hip-Hop, Folklore', '1:28'), ('Oamenii Sunt Inca Frumosi', 13, 'Underground, Hip-Hop, Folklore', '4:51'),
('M-a Facut Muma Frumoasa', 13, 'Underground, Hip-Hop, Folklore', '3:32'), ('Rege Pe Deal', 13, 'Underground, Hip-Hop, Folklore', '4:01'),
('2000 De Km', 13, 'Underground, Hip-Hop, Folklore', '5:33'), ('Frunzulita, Iarba Deasa', 13, 'Underground, Hip-Hop, Folklore', '5:44'),
('Scrisoare Din Trecut', 13, 'Underground, Hip-Hop, Folklore', '4:38'), ('Da Cu Arcu''', 13, 'Underground, Hip-Hop, Folklore', '3:17'),
('Orientat', 13, 'Underground, Hip-Hop, Folklore', '4:54'), ('Rau Necesar', 13, 'Underground, Hip-Hop, Folklore', '4:14'), 
('Ca O Molie', 13, 'Underground, Hip-Hop, Folklore', '4:41'), ('Viata-i Mare', 13, 'Underground, Hip-Hop, Folklore', '8:21')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Stai - Unplugged', 14, 'Rock', '7:57'), ('Mai presus de cuvinte - Unplugged', 14, 'Rock', '5:16'), ('Biz - Unplugged', 14, 'Rock', '4:59'),
('Hectic - Unplugged', 14, 'Rock', '4:56'), ('Daddy - Unplugged', 14, 'Rock', '4:24'), ('Culori - Unplugged', 14, 'Rock', '5:59'), 
('In mine in soapta - Unplugged', 14, 'Rock', '4:10'), ('Morphine - Unplugged', 14, 'Rock', '4:57'), ('Un loc sa ajung - Unplugged', 14, 'Rock', '7:48'),
('Coboara-ma-n Rai - Unplugged', 14, 'Rock', '5:31'), ('Canta-mi povestea - Piano Version', 14, 'Rock', '4:56'), 
('Blestem (Cine iubeste si lasa) - Unplugged', 14, 'Rock', '6:25')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Mylo Xyloto', 15, 'Alternative', '0:42'), ('Hurts Like Heaven', 15, 'Alternative', '4:02'), ('Paradise', 15, 'Alternative', '4:38'), 
('Charlie Brown', 15, 'Alternative', '4:45'), ('Us Against the World', 15, 'Alternative', '3:59'), ('M.M.I.X.', 15, 'Alternative', '0:48'), 
('Every Teardrop Is a Waterfall', 15, 'Alternative', '4:00'), ('Major Minus', 15, 'Alternative', '3:30'), ('U.F.O.', 15, 'Alternative', '2:17'), 
('Princess of China', 15, 'Alternative', '3:59'), ('Up in Flames', 15, 'Alternative', '3:13'), ('A Hopeful Transmission', 15, 'Alternative', '0:33'),
('Don''t Let It Break Your Heart', 15, 'Alternative', '3:54'), ('Up with the Birds', 15, 'Alternative', '3:45')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Unperson', 16, 'Indie-Rock', '3:24'), ('Futureproof', 16, 'Indie-Rock', '3:27'), ('Is Everybody Going Crazy?', 16, 'Indie-Rock', '3:57'),
('Free If We Want It', 16, 'Indie-Rock', '3:52'), ('Miracle, Baby', 16, 'Indie-Rock', '3:40'), ('Impossible', 16, 'Indie-Rock', '4:08'), 
('If I Were You', 16, 'Indie-Rock', '3:28'), ('There Was Sun', 16, 'Indie-Rock', '4:03'), ('Can You Afford to Be An Individual?', 16, 'Indie-Rock', '3:56'),
('Phobia', 16, 'Indie-Rock', '4:04'), ('Before We Drift Away', 16, 'Indie-Rock', '4:14'), ('Ce n''est Rien', 16, 'Indie-Rock', '3:00'), 
('Moral Panic', 16, 'Indie-Rock', '3:40'), ('Real Love Song', 16, 'Indie-Rock', '3:42'), ('This Feels Like The End', 16, 'Indie-Rock', '4:02'),
('Your Blood', 16, 'Indie-Rock', '4:50')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Do I Wanna Know?', 17, 'Indie-Rock', '4:32'), ('R U Mine?', 17, 'Indie-Rock', '3:21'), ('One For The Road', 17, 'Indie-Rock', '3:26'), 
('Arabella', 17, 'Indie-Rock', '3:27'), ('I Want It All', 17, 'Indie-Rock', '3:05'), ('No. 1 Party Anthem', 17, 'Indie-Rock', '4:03'), 
('Mad Sounds', 17, 'Indie-Rock', '3:35'), ('Fireside', 17, 'Indie-Rock', '3:01'), ('Why''d You Only Call Me When You''re High?', 17, 'Indie-Rock', '2:41'),
('Snap Out Of It', 17, 'Indie-Rock', '3:13'), ('Knee Socks', 17, 'Indie-Rock', '4:17'), ('I Wanna Be Yours', 17, 'Indie-Rock', '3:03')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('I Was Just a Kid', 18, 'Indie-Rock', '4:30'), ('Amsterdam', 18, 'Indie-Rock', '4:32'), ('Sorry', 18, 'Indie-Rock', '3:34'), 
('Broken Machine', 18, 'Indie-Rock', '3:54'), ('Live Like Animals', 18, 'Indie-Rock', '4:10'), ('Soda', 18, 'Indie-Rock', '3:56'), 
('I''m Not Made by Design', 18, 'Indie-Rock', '3:52'), ('Particles', 18, 'Indie-Rock', '3:55'), ('Get Better', 18, 'Indie-Rock', '3:19'), 
('Hell, Yeah', 18, 'Indie-Rock', '3:06'), ('Afterlife', 18, 'Indie-Rock', '4:43'), ('Reset Me', 18, 'Indie-Rock', '3:31'), 
('Number 13', 18, 'Indie-Rock', '2:57'), ('Sorry - Acoustic', 18, 'Indie-Rock', '3:34'), ('Particles - Piano Version', 18, 'Indie-Rock', '3:39')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Take a Bow', 19, 'Rock', '4:35'), ('Starlight', 19, 'Rock', '4:00'), ('Supermassive Black Hole', 19, 'Rock', '3:32'), 
('Map of the Problematique', 19, 'Rock', '4:18'), ('Soldier''s Poem', 19, 'Rock', '2:04'), ('Invincible', 19, 'Rock', '5:01'), ('Assassin', 19, 'Rock', '3:31'),
('Exo-Politics', 19, 'Rock', '3:53'), ('City of Delusion', 19, 'Rock', '4:48'), ('Hoodoo', 19, 'Rock', '3:43'), ('Knights of Cydonia', 19, 'Rock', '6:06'),
('Glorious', 19, 'Rock', '4:41')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Nemuritori', 20, 'Alternative', '4:46'), ('Ce Se Intampla?', 20, 'Alternative', '4:50'), ('Gloria', 20, 'Alternative', '3:27'), 
('Om', 20, 'Alternative', '3:37'), ('Umeri Aurii', 20, 'Alternative', '4:32'), ('Caleidoscop', 20, 'Alternative', '5:21'), ('Spuneai', 20, 'Alternative', '4:35'),
('Caffe Sospeso', 20, 'Alternative', '4:55'), ('Noua Vieti', 20, 'Alternative', '3:18'), ('Ce Ramane', 20, 'Alternative', '4:41'), ('Zbor', 20, 'Alternative', '6:31')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Intro', 21, 'Rock', '0:22'), ('Apocalypse Please', 21, 'Rock', '4:12'), ('Time is Running Out', 21, 'Rock', '3:57'), ('Sing for Absolution', 21, 'Rock', '4:54'),
('Stockholm Syndrome', 21, 'Rock', '4:57'), ('Falling Away with You', 21, 'Rock', '4:40'), ('Interlude', 21, 'Rock', '0:37'), ('Hysteria', 21, 'Rock', '3:47'),
('Blackout', 21, 'Rock', '4:22'), ('Butterflies and Hurricanes', 21, 'Rock', '5:01'), ('The Small Print', 21, 'Rock', '3:29'), ('Endlessly', 21, 'Rock', '3:48'),
('Thoughts of a Dying Atheis', 21, 'Rock', '3:07'), ('Ruled by Secrecy', 21, 'Rock', '4:52'), ('Fury', 21, 'Rock', '5:02')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Acum Incepe Totul', 22, 'Alternative', '4:48'), ('Imperfect', 22, 'Alternative', '3:33'), ('Stai', 22, 'Alternative', '4:16'), 
('Un Sfert De Secunda', 22, 'Alternative', '4:35'), ('Unde Esti?', 22, 'Alternative', '4:27'), ('Tine-Ma', 22, 'Alternative', '3:33'), 
('Uneori', 22, 'Alternative', '5:09'), ('1000 De Da', 22, 'Alternative', '3:54'), ('O Fi Un Vis', 22, 'Alternative', '3:51'), ('Infinit', 22, 'Alternative', '4:52')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Fat-Frumos', 23, 'Alternative', '5:06'), ('Cosanzeana', 23, 'Alternative', '4:49'), ('Ana', 23, 'Alternative', '3:00'), ('Manole', 23, 'Alternative', '5:56'),
('Descantec', 23, 'Alternative', '3:58'), ('Soarele', 23, 'Alternative', '4:17'), ('Luna', 23, 'Alternative', '5:29'), ('Moldoveanu', 23, 'Alternative', '4:37'),
('Miorita', 23, 'Alternative', '5:19'), ('100 de ploi', 25, 'Urban Folklore', '5:03'), ('Luna', 25, 'Urban Folklore', '4:25'), 
('Iesi, Soare!', 25, 'Urban Folklore', '4:37'), ('Soarta muta', 25, 'Urban Folklore', '4:18'), ('Vino pan la Bucuresti', 25, 'Urban Folklore', '3:56'),
('Duilala', 25, 'Urban Folklore', '5:31'), ('Nu ai nume', 25, 'Urban Folklore', '4:38'), ('Uda', 25, 'Urban Folklore', '4:44')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Brainstorm', 26, 'Indie-Rock', '2:52'), ('Teddy Picker', 26, 'Indie-Rock', '2:45'), ('D is for Dangerous', 26, 'Indie-Rock', '2:18'),
('Balaclava', 26, 'Indie-Rock', '2:51'), ('Fluorescent Adolescent', 26, 'Indie-Rock', '3:03'), ('Only Ones Who Know', 26, 'Indie-Rock', '3:04'),
('Do Me a Favour', 26, 'Indie-Rock', '3:29'), ('This House is a Circus', 26, 'Indie-Rock', '3:11'), ('If You Were There, Beware', 26, 'Indie-Rock', '4:36'),
('The Bad Thing', 26, 'Indie-Rock', '2:25'), ('Old Yellow Bricks', 26, 'Indie-Rock', '3:13'), ('505', 26, 'Indie-Rock', '4:13')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Buna Dimineata', 28, 'Underground, Hip-Hop, Folklore', '4:11'), ('Graba Strica Treaba', 28, 'Underground, Hip-Hop, Folklore', '3:34'), 
('De Ce Eu?', 28, 'Underground, Hip-Hop, Folklore', '5:00'), ('Da-I Foale', 28, 'Underground, Hip-Hop, Folklore', '4:38'), 
('Ochiu'' Dracului', 28, 'Underground, Hip-Hop, Folklore', '5:41'), ('Marcel Temelie', 28, 'Underground, Hip-Hop, Folklore', '6:02'), 
('''84-''85', 28, 'Underground, Hip-Hop, Folklore', '3:55'), ('Folclor Nemuritor', 28, 'Underground, Hip-Hop, Folklore', '5:29'),
('Raionul De Karme', 28, 'Underground, Hip-Hop, Folklore', '5:17'), ('Asfintit', 28, 'Underground, Hip-Hop, Folklore', '5:57'), 
('Greieri Si Sfinti', 28, 'Underground, Hip-Hop, Folklore', '9:10'), ('Eroul Generatiei', 28, 'Underground, Hip-Hop, Folklore', '6:36'),
('Animalul Din Mine', 28, 'Underground, Hip-Hop, Folklore', '4:45'), ('Ce Bine Ca Stiu Canta', 28, 'Underground, Hip-Hop, Folklore', '5:00'),
('Cerc Inchis', 28, 'Underground, Hip-Hop, Folklore', '4:30'), ('Muntele Nu Plange', 28, 'Underground, Hip-Hop, Folklore', '5:03'), 
('Subcarpati', 28, 'Underground, Hip-Hop, Folklore', '6:42'), ('Zori', 28, 'Underground, Hip-Hop, Folklore', '5:17')

INSERT INTO Songs(Name, AlID, Genre, Duration)
VALUES ('Din 94', 24, 'Hip-Hop', '4:32'), ('Deschide Ochii', 24, 'Hip-Hop', '3:54'), ('Piese De Schimb', 24, 'Hip-Hop', '3:05'), 
('Povesti Cu Noi', 24, 'Hip-Hop', '3:10'), ('Shaorma (SKit)', 24, 'Hip-Hop', '0:53'), ('Cu De Toate', 24, 'Hip-Hop', '3:49'), ('Cox', 24, 'Hip-Hop', '3:12'),
('Poate Tu', 24, 'Hip-Hop', '4:05'), ('Negru', 24, 'Hip-Hop', '3:09'), ('Sange De Porc', 24, 'Hip-Hop', '4:20'), ('Nu-I Loc De Joaca', 24, 'Hip-Hop', '3:46'),
('Cine E De Vina? - Skit', 24, 'Hip-Hop', '0:38'), ('Film De Actiune', 24, 'Hip-Hop', '2:56'), ('Fraiere', 24, 'Hip-Hop', '3:26'), 
('Te Stiu De-O Viata', 24, 'Hip-Hop', '3:47'), ('Linii De Tramvai', 24, 'Hip-Hop', '3:14'), ('Stiu Pe Cineva', 24, 'Hip-Hop', '3:14'), ('Ctc', 24, 'Hip-Hop', '3:02'),
('N-Are Cine Ce Sa Ca Sa', 24, 'Hip-Hop', '2:54'), ('2020', 24, 'Hip-Hop', '4:30'), ('Demoncratie', 24, 'Hip-Hop', '3:35')

INSERT INTO Playlists(Uid, Name, NoOfSongs)
VALUES (1, 'Rock romanesc', 13), (1, 'Good vibez', 25) 

INSERT INTO Playlists(Uid, Name, NoOfSongs)
VALUES (2, 'Woo', 16), (5, 'Masina', 21), (7, 'Relax', 7), (8, 'Sing along', 19), (10, 'no name', 11)

INSERT INTO PlaylistSongs(Pid, Sid)
VALUES (1, 10), (1, 93), (1, 100), (1, 118), (1, 128), (1, 135), (1, 136), (1, 268), (1, 273), (1, 275), (1, 134), (1, 108), (1, 79), (2, 5), (2, 11), (2, 35), (2, 43), 
(2, 74), (2, 78), (2, 79), (2, 80), (2, 88), (2, 93), (2, 109), (2, 117), (2, 118), (2, 121), (2, 126), (2, 133), (2, 145), (2, 168), (2, 182), (2, 201), (2, 209),
(2, 225), (2, 239), (2, 303), (2, 280)

INSERT INTO PlaylistSongs (Pid, Sid)
VALUES (3, 1), (3, 43), (3, 56), (3, 82), (3, 109), (3, 126), (3, 136), (3, 168), (3, 193), (3, 196), (3, 239), (3, 270), (3, 284), (3, 294), (3, 269), (3, 185), (4, 10),
(4, 35), (4, 42), (4, 73), (4, 80), (4, 121), (4, 146), (4, 168), (4, 183), (4, 204), (4, 208), (4, 214), (4, 225), (4, 248), (4, 253), (4, 280), (4, 286), (4, 291), 
(4, 292), (4, 303), (4, 324), (5, 9), (5, 57), (5, 299), (5, 302), (5, 306), (5, 210), (5, 201), (6, 11), (6, 28), (6, 42), (6, 66), (6, 100), (6, 143), (6, 196), 
(6, 209), (6, 268), (6, 273), (6, 286), (6, 299), (6, 303), (6, 333), (6, 253), (6, 204), (6, 182), (6, 147), (6, 83), (7, 88), (7, 42), (7, 61), (7, 72), (7, 117), 
(7, 146), (7, 197), (7, 225), (7, 240), (7, 274), (7, 326)








