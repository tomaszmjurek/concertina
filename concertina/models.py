from concertina.configs import db

appearances_table = db.Table(
    'appearances',
    db.Column('band_name', db.String, db.ForeignKey('bands.name')),
    db.Column('festival_name', db.String),
    db.Column('festival_date', db.Date),
    db.ForeignKeyConstraint(['festival_name', 'festival_date'],
                            ['festivals.name', 'festivals.date_start'])
)

receptions_table = db.Table(
    'award_receptions',
    db.Column('album_name', db.String),
    db.Column('album_band_name', db.String),
    db.Column('award_name', db.String, db.ForeignKey('awards.name')),
    db.ForeignKeyConstraint(['album_name', 'album_band_name'],
                            ['albums.name', 'albums.band_name'])
)


class Bands(db.Model):
    __tablename__ = 'bands'

    name = db.Column(db.String, primary_key=True)
    formation_date = db.Column(db.Date, nullable=True)
    members = db.relationship('Musicians', backref='band')
    concerts = db.relationship('Concerts', backref='performer')
    festivals = db.relationship('Festivals', secondary=appearances_table,
                                backref=db.backref('bands', lazy='dynamic'))

    @staticmethod
    def create(name, formation_date=None):
        band = Bands(name=name, formation_date=formation_date)
        db.session.add(band)
        db.session.commit()
        return band

    def play_concert(self, place, date):
        return Concerts.create(self, place, date)

    def release_album(self, name, genre=None):
        return Albums.create(name, self, genre)

    def appear_on_festival(self, festival):
        festival.bands.append(self)


class Instruments(db.Model):
    __tablename__ = 'instruments'

    type = db.Column(db.String, primary_key=True)

    @staticmethod
    def create(type):
        instrument = Instruments(type=type)
        db.session.add(instrument)
        db.session.commit()
        return instrument


class Musicians(db.Model):
    __tablename__ = 'musicians'

    name = db.Column(db.String, primary_key=True)

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
    instrument_type = db.Column(db.String, db.ForeignKey('instruments.type'), nullable=False)
    instrument = db.relationship('Instruments', backref='players')

    @staticmethod
    def create(name, band, instrument, nationality=None):
        musician = Musicians(
            name=name,
            band=band,
            instrument=instrument,
            nationality=nationality,
        )
        db.session.add(musician)
        db.session.commit()
        return musician


class Places(db.Model):
    __tablename__ = 'places'

    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)

    db.PrimaryKeyConstraint(name, city)

    @staticmethod
    def create(name, city, address=None):
        place = Places(name=name, city=city, address=address)
        db.session.add(place)
        db.session.commit()
        return place


class Concerts(db.Model):
    __tablename__ = 'concerts'

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)

    place_name = db.Column(db.String, nullable=False)
    place_city = db.Column(db.String, nullable=False)
    db.ForeignKeyConstraint([place_name, place_city],
                            [Places.name, Places.city])
    place = db.relationship('Places', backref='concerts')

    concert_date = db.Column(db.Date, nullable=False)
    tour = db.Column(db.String, nullable=True)


    db.PrimaryKeyConstraint(band_name, place_name, place_city, concert_date)

    @staticmethod
    def create(performer, place, concert_date):
        concert = Concerts(performer=performer, place=place, concert_date=concert_date)
        db.session.add(concert)
        db.session.commit()
        return concert


class Festivals(db.Model):
    __tablename__ = 'festivals'

    name = db.Column(db.String, nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    place_name = db.Column(db.String, nullable=False)
    place_city = db.Column(db.String, nullable=False)
    place = db.relationship('Places', backref='festivals')

    db.ForeignKeyConstraint([place_name, place_city],
                            [Places.name, Places.city])
    db.PrimaryKeyConstraint(name, date_start)

    @staticmethod
    def create(name, date_start, place):
        festival = Festivals(name=name, date_start=date_start, place=place)
        db.session.add(festival)
        db.session.commit()
        return festival

    def host_band(self, band):
        self.bands.append(band)


class Genres(db.Model):
    __tablename__ = 'genres'

    name = db.Column(db.String, primary_key=True)
    supergenre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
    supergenre = db.relationship('Genres', remote_side=name, backref=db.backref('subgenres'))

    @staticmethod
    def create(name, supergenre=None):
        g_name = None if not supergenre else supergenre.name
        genre = Genres(name=name, supergenre_name=g_name)
        db.session.add(genre)
        db.session.commit()
        return genre


class Albums(db.Model):
    __tablename__ = 'albums'

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
    band = db.relationship('Bands', backref='albums')

    name = db.Column(db.String, nullable=False)

    genre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
    genre = db.relationship('Genres', backref='genre')

    awards = db.relationship('Awards', secondary=receptions_table,
                             backref=db.backref('awarded_albums', lazy='dynamic'))

    db.PrimaryKeyConstraint(band_name, name)

    @staticmethod
    def create(name, band, genre=None):
        album = Albums(band=band, name=name, genre=genre)
        db.session.add(album)
        db.session.commit()
        return album

    def add_songs(self, titles):
        if isinstance(titles, str):
            return Songs.create(titles, self)

        if isinstance(titles, list):
            songs = []
            for title in titles:
                song = Songs.create(title, self)
                songs.append(song)
            return songs


class Songs(db.Model):
    __tablename__ = 'songs'

    album_name = db.Column(db.String, nullable=False)
    band_name = db.Column(db.String, nullable=False)
    album = db.relationship('Albums', backref='songs')

    position = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)

    db.ForeignKeyConstraint([album_name, band_name],
                            [Albums.name, Albums.band_name])
    db.PrimaryKeyConstraint(band_name, album_name, position)

    @staticmethod
    def create(name, album):
        position = len(album.songs) + 1
        song = Songs(name=name, album=album, position=position)
        db.session.add(song)
        db.session.commit()
        return song


class Awards(db.Model):
    __tablename__ = 'awards'

    name = db.Column(db.String, primary_key=True)

    @staticmethod
    def create(name):
        award = Awards(name=name)
        db.session.add(award)
        db.session.commit()
        return award

    def award_album(self, album):
        self.awarded.albums.append(album)