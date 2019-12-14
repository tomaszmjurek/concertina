CREATE TABLE BANDS(
    NAME VARCHAR(50) PRIMARY KEY,
    FORMATION_DATE DATE NULL
);

CREATE TABLE INSTRUMENTS(
    TYPE VARCHAR(50) PRIMARY KEY
);

CREATE TABLE MUSICIANS(
    NAME VARCHAR(50) PRIMARY KEY,
    BAND NOT NULL REFERENCES BANDS(NAME),
    INSTRUMENT NOT NULL REFERENCES INSTRUMENTS(TYPE)
);

CREATE TABLE PLACES(
    ID_PLACE NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NAME VARCHAR(50),
    CITY VARCHAR(50),
    COUNTRY VARCHAR(3) NULL,
    UNIQUE(NAME, CITY)
);

CREATE TABLE CONCERTS(
    BAND REFERENCES BANDS(NAME),
    ID_PLACE REFERENCES PLACES(ID_PLACE),
    CONCERT_DATE DATE NOT NULL,
    TOUR VARCHAR(50) NULL,
    PRIMARY KEY(BAND, ID_PLACE, CONCERT_DATE)
);

CREATE TABLE FESTIVALS(
    ID_FESTIVAL NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NAME VARCHAR(50),
    DATE_START DATE,
    ID_PLACE NOT NULL REFERENCES PLACES(ID_PLACE),
    UNIQUE(NAME, DATE_START)
);

CREATE TABLE APPEARANCES(
    ID_FESTIVAL REFERENCES FESTIVALS(ID_FESTIVAL),
    BAND REFERENCES BANDS(NAME),
    PRIMARY KEY(BAND, ID_FESTIVAL)
);

CREATE TABLE GENRES(
    NAME VARCHAR(50) PRIMARY KEY,
    SUPERGENRE NULL REFERENCES GENRES(NAME)
);

CREATE TABLE ALBUMS(
    ID_ALBUM NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
    BAND REFERENCES BANDS(NAME),
    NAME VARCHAR(50),
    GENRE NULL REFERENCES GENRES(NAME),
    UNIQUE(BAND, NAME)
);

CREATE TABLE SONGS(
    ID_SONG NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
    ID_ALBUM REFERENCES ALBUMS(ID_ALBUM),
    POSITION NUMBER(2),
    NAME VARCHAR(50) NOT NULL,
    UNIQUE (ID_ALBUM, POSITION)
);

CREATE TABLE AWARDS(
    NAME VARCHAR(50) PRIMARY KEY
);

CREATE TABLE AWARD_RECEPTIONS(
    ID_ALBUM REFERENCES ALBUMS(ID_ALBUM),
    AWARD NOT NULL REFERENCES AWARDS(NAME),
    PRIMARY KEY(ID_ALBUM, AWARD)
);


CREATE OR REPLACE FUNCTION ConcertsBetween(
    date_from IN DATE DEFAULT CURRENT_DATE,
    date_to IN DATE DEFAULT CURRENT_DATE + INTERVAL '30' DAY
    ) RETURN SYS_REFCURSOR IS
DECLARE
    CURSOR cur(vfrom DATE, vto DATE) IS
    SELECT * FROM CONCERTS
    WHERE CONCERT_DATE BETWEEN vfrom AND vto;
BEGIN
    RETURN cur(date_from, date_to);
END;

CREATE OR REPLACE PROCEDURE AwardAlbum(
    band_name IN BANDS.NAME%TYPE,
    album IN ALBUMS.ID_ALBUM%TYPE
) IS
BEGIN
    INSERT INTO AWARD_RECEPTIONS(ID_ALBUM, AWARD)
        VALUES(album, award_name);
END;

CREATE OR REPLACE PROCEDURE AppearOnFestival(
    band_name IN BANDS.NAME%TYPE,
    festival IN FESTIVALS.ID_FESTIVAL%TYPE
) IS
BEGIN
    INSERT INTO APPEARANCES(BAND, ID_FESTIVAL)
        VALUES(band_name, festival);
END;


DROP TABLE AWARD_RECEPTIONS;
DROP TABLE AWARDS;
DROP TABLE SONGS;
DROP TABLE ALBUMS;
DROP TABLE GENRES;
DROP TABLE MUSICIANS;
DROP TABLE INSTRUMENTS;
DROP TABLE APPEARANCES;
DROP TABLE FESTIVALS;
DROP TABLE CONCERTS;
DROP TABLE PLACES;
DROP TABLE BANDS;
