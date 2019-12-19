CREATE TABLE BANDS(
    NAME VARCHAR PRIMARY KEY,
    FORMATION_DATE DATE NULL
);

CREATE TABLE INSTRUMENTS(
    TYPE VARCHAR PRIMARY KEY
);

CREATE TABLE MUSICIANS(
    NAME VARCHAR PRIMARY KEY,
    BAND VARCHAR REFERENCES BANDS(NAME),
    INSTRUMENT VARCHAR REFERENCES INSTRUMENTS(TYPE)
);

CREATE TABLE PLACES(
    ID_PLACE SERIAL PRIMARY KEY,
    NAME VARCHAR,
    CITY VARCHAR,
    COUNTRY VARCHAR NULL,
    UNIQUE(NAME, CITY)
);

CREATE TABLE CONCERTS(
    BAND VARCHAR REFERENCES BANDS(NAME),
    ID_PLACE INTEGER REFERENCES PLACES(ID_PLACE),
    CONCERT_DATE DATE NOT NULL,
    TOUR VARCHAR NULL,
    PRIMARY KEY(BAND, ID_PLACE, CONCERT_DATE)
);

CREATE TABLE FESTIVALS(
    ID_FESTIVAL SERIAL PRIMARY KEY,
    NAME VARCHAR,
    DATE_START DATE,
    ID_PLACE INTEGER REFERENCES PLACES(ID_PLACE) NOT NULL,
    UNIQUE(NAME, DATE_START)
);

CREATE TABLE APPEARANCES(
    ID_FESTIVAL INTEGER REFERENCES FESTIVALS(ID_FESTIVAL),
    BAND VARCHAR REFERENCES BANDS(NAME),
    PRIMARY KEY(BAND, ID_FESTIVAL)
);

CREATE TABLE GENRES(
    NAME VARCHAR PRIMARY KEY,
    SUPERGENRE VARCHAR REFERENCES GENRES(NAME) DEFAULT NULL
);

CREATE TABLE ALBUMS(
    ID_ALBUM SERIAL PRIMARY KEY ,
    BAND VARCHAR REFERENCES BANDS(NAME),
    NAME VARCHAR NOT NULL,
    GENRE VARCHAR REFERENCES GENRES(NAME) NULL,
    UNIQUE(BAND, NAME)
);

CREATE TABLE SONGS(
    ID_SONG SERIAL PRIMARY KEY ,
    ID_ALBUM INTEGER REFERENCES ALBUMS(ID_ALBUM),
    POSITION SMALLSERIAL,
    NAME VARCHAR NOT NULL,
    UNIQUE (ID_ALBUM, POSITION)
);

CREATE TABLE AWARDS(
    NAME VARCHAR PRIMARY KEY
);

CREATE TABLE AWARD_RECEPTIONS(
    ID_ALBUM INTEGER REFERENCES ALBUMS(ID_ALBUM),
    AWARD VARCHAR REFERENCES AWARDS(NAME)  NOT NULL ,
    PRIMARY KEY(ID_ALBUM, AWARD)
);

CREATE OR REPLACE PROCEDURE AddSong(album_name VARCHAR,song_name VARCHAR)
    LANGUAGE SQL AS
$$
    INSERT INTO SONGS(ID_ALBUM, NAME)
    VALUES((SELECT ID_ALBUM FROM ALBUMS WHERE NAME=album_name), song_name);
$$;

CREATE OR REPLACE PROCEDURE PlanConcert(
    band_name VARCHAR,
    place_name VARCHAR,
    place_city VARCHAR,
    date_of_concert DATE,
    tour_name VARCHAR DEFAULT NULL
) LANGUAGE SQL AS
$$
    INSERT INTO CONCERTS(BAND, CONCERT_DATE, TOUR, ID_PLACE)
        VALUES(band_name, date_of_concert, tour_name,
                (SELECT ID_PLACE FROM PLACES WHERE CITY=place_city AND NAME=place_name));
$$;

CREATE OR REPLACE FUNCTION getConcertsInTour(tour_name VARCHAR)
RETURNS SETOF concerts AS
$$
    BEGIN
       RETURN QUERY (SELECT * FROM CONCERTS WHERE tour = tour_name);
    END
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION getConcertsByDate(start_date DATE DEFAULT CURRENT_DATE, days_number INTEGER DEFAULT 30)
RETURNS SETOF concerts AS
$$
    BEGIN
       RETURN QUERY (SELECT * FROM concerts WHERE concert_date < start_date + days_number * (INTERVAL '1' DAY));
    END
$$ LANGUAGE 'plpgsql';



-- DROP TABLE AWARD_RECEPTIONS;
-- DROP TABLE AWARDS;
-- DROP TABLE SONGS;
-- DROP TABLE ALBUMS;
-- DROP TABLE GENRES;
-- DROP TABLE MUSICIANS;
-- DROP TABLE INSTRUMENTS;
-- DROP TABLE APPEARANCES;
-- DROP TABLE FESTIVALS;
-- DROP TABLE CONCERTS;
-- DROP TABLE PLACES;
-- DROP TABLE BANDS;
