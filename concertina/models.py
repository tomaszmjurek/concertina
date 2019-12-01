from concertina.configs import db


class Bands(db.Model):
    __tablename__ = 'bands'

    name = db.Column(db.String, primary_key=True)
    formation_date = db.Column(db.Date, nullable=True)


class Instruments(db.Model):
    __tablename__ = 'instruments'

    type = db.Column(db.String, primary_key=True)


class Musicians(db.Model):
    __tablename__ = 'musicians'

    name = db.Column(db.String, primary_key=True)

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
    band = db.relationship('Bands', backref='members')

    instrument_type = db.Column(db.String, db.ForeignKey('instruments.type'), nullable=False)
    instrument = db.relationship('Instruments', backref='players')

    nationality = db.Column(db.String, nullable=True)


class Places(db.Model):
    __tablename__ = 'places'

    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)

    db.PrimaryKeyConstraint(name, city)


class Concerts(db.Model):
    __tablename__ = 'concerts'

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
    band = db.relationship("Bands", backref='concerts')

    place_name = db.Column(db.String, db.ForeignKey('places.name'), nullable=False)
    place_city = db.Column(db.String, db.ForeignKey('places.city'), nullable=False)
    place = db.relationship("Places", backref='concerts')

    concert_date = db.Column(db.Date, nullable=False)
    tour = db.Column(db.String, nullable=True)

    db.PrimaryKeyConstraint(band_name, place_name, place_city, concert_date)


class Festivals(db.Model):
    __tablename__ = 'festivals'

    name = db.Column(db.String, nullable=False)
    date_start = db.Column(db.Date, nullable=True)
    place_name = db.Column(db.String, db.ForeignKeyConstraint('places.name'), null=False)
    place_city = db.Column(db.String, db.ForeignKeyConstraint('places.city'), null=False)
    localization = db.relationship('Places', backref='festivals')

    db.PrimaryKeyConstraint(name, date_start)


class Appearances(db.Model):
    __tablename__ = 'appearances'

    # TODO MANY TO MANY?
    festival_name = db.Column(db.String, db.ForeignKeyConstraint('festivals.name'))
    festival_date = db.Column(db.Date, db.ForeignKey('festivals.date_start'))
    band_name = db.Column(db.Integer, db.ForeignKey('bands.id_band'))
    db.PrimaryKeyConstraint(festival_name, festival_date, band_name)


class Genres(db.Model):
    __tablename__ = 'genres'

    name = db.Column(db.String, primary_key=True)
    supergenre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
    supergenre = db.relationship('Genres', backref='subgenres')


class Albums(db.Model):
    __tablename__ = 'albums'

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
    band = db.relationship('Bands', backref='albums')

    name = db.Column(db.String, nullable=False)

    genre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
    genre = db.relationship('Genres', backref='genre')

    db.PrimaryKeyConstraint(band_name, name)


class Songs(db.Model):
    __tablename__ = 'songs'

    album_name = db.Column(db.String, db.ForeignKey('albums.name'), nullable=False)
    album = db.relationship('Albums', backref='songs')

    band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
    band = db.relationship('Bands')

    posisiton = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)

    db.PrimaryKeyConstraint(band_name, album_name, posisiton)


class Awards(db.Model):
    __tablename__ = 'awards'

    name = db.Column(db.String, primary_key=True)


class AwardReceptions(db.Model):
    __tablename__ = 'award_receptions'


    # TODO MANY TO MANY?
    album_name = db.Column(db.String, db.ForeignKey('albums.name'), nullable=False)
    album = db.relationship('Albums')
    award_name = db.Column(db.String, db.ForeignKey('awards.name'), nullable=False)
    award = db.relationship('Awards')

    db.PrimaryKeyConstraint(album_name, award_name)




