INSERT INTO instruments(type)
VALUES ('Guitar'), ('Drums'), ('Vocal'), ('Bass'), ('Keyboard');

INSERT INTO genres(name)
    VALUES ('Fusion'), ('Blues'), ('Rock');
INSERT INTO genres(name, supergenre)
    VALUES ('Soft Rock', 'Rock'),
           ('Psychodelic Rock', 'Rock'),
           ('Progressive Rock', 'Rock');

INSERT INTO places(name, city, street)
    VALUES ('Stadium', 'Poznan', 'Bulgarska 17'),
           ('Arena', 'Poznan', 'Stanislawa Wyspianskiego 33'),
           ('Blue Note', 'Poznan', 'Kosciuszki 79'),
           ('U Bazyla', 'Poznan', 'Norwida 18A');

-- Rolling Stones

INSERT INTO bands(name, formation_date)
    VALUES ('The Rolling Stones', DATE'1962-1-1');

INSERT INTO musicians(name, band, instrument)
    VALUES ('Mick Jagger', 'The Rolling Stones', 'Vocal'),
           ('Keith Richards', 'The Rolling Stones', 'Guitar'),
           ('Ron Wood', 'The Rolling Stones', 'Bass'),
           ('Charlie Watts', 'The Rolling Stones', 'Keyboard');

INSERT INTO albums(band, name, genre)
    VALUES ('The Rolling Stones', 'Blue and Lonesome', 'Blues');

CALL AddSong('Blue and Lonesome', 'Just Your Fool', 1);
CALL AddSong('Blue and Lonesome', 'Commit a Crime', 2);
CALL AddSong('Blue and Lonesome', 'Blue and Lonesome', 3);
CALL AddSong('Blue and Lonesome', 'All of Your Love', 4);
CALL AddSong('Blue and Lonesome', 'I Gotta Go', 5);
CALL AddSong('Blue and Lonesome', 'Everybody Knows About My Good Thing', 6);
CALL AddSong('Blue and Lonesome', 'RideEm on Down', 7);
CALL AddSong('Blue and Lonesome', 'Hate To See You Ho', 8);
CALL AddSong('Blue and Lonesome', 'Hoo Doo Blues', 9);
CALL AddSong('Blue and Lonesome', 'Little Rain', 10);
CALL AddSong('Blue and Lonesome', 'Just Like I Treat You', 11);
CALL AddSong('Blue and Lonesome', 'I Cant Quit You Baby', 12);

-- Casiopea

INSERT INTO bands(name, formation_date)
    VALUES ('Casiopea', DATE'1976-1-1');

INSERT INTO musicians(name, band, instrument)
    VALUES ('Issei Noro', 'Casiopea', 'Guitar'),
           ('Kiyomi Otaka', 'Casiopea', 'Keyboard'),
           ('Yoshihiko Naruse', 'Casiopea', 'Bass'),
           ('Akira Jimbo', 'Casiopea', 'Drums');

INSERT INTO albums(band, name, genre)
    VALUES ('Casiopea', 'Casiopea', 'Fusion'),
           ('Casiopea', 'Super Flight', 'Fusion'),
           ('Casiopea', 'Thunder Live', 'Fusion'),
           ('Casiopea', 'Make Up City', 'Fusion'),
           ('Casiopea', 'Eyes of the Mind', 'Fusion'),
           ('Casiopea', 'Mint Jams', 'Fusion'),
           ('Casiopea', '4x4', 'Fusion');

-- CONCERTS

CALL PlanConcert('The Rolling Stones',
                'Stadium', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '1' DAY AS DATE));
CALL PlanConcert('The Rolling Stones',
                'Arena', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '2' DAY AS DATE));
CALL PlanConcert('The Rolling Stones',
                'Blue Note', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '3' DAY AS DATE));
CALL PlanConcert('The Rolling Stones',
                'U Bazyla', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '4' DAY AS DATE));

CALL PlanConcert('Casiopea',
                'Stadium', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '5' DAY AS DATE));
CALL PlanConcert('Casiopea',
                'Arena', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '6' DAY AS DATE));
CALL PlanConcert('Casiopea',
                'Blue Note', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '7' DAY AS DATE));
CALL PlanConcert('Casiopea',
                'U Bazyla', 'Poznan',
                CAST(CURRENT_DATE + INTERVAL '8' DAY AS DATE));

INSERT INTO awards(name)
    VALUES ('Platinum record'),
           ('Gold Record');



