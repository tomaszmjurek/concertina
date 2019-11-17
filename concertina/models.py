from concertina.configs import db


class Bands(db.Model):
    __tablename__ = 'bands'

    id_band = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    formation_date = db.Column(db.Date, nullable=True)


class Instruments(db.Model):
    __tablename__ = 'instruments'

    type = db.Column(db.String, primary_key=True)


class Musicians(db.Model):
    __tablename__ = 'musicians'

    id_musician = db.Column(db.Integer, primary_key=True)

    id_band = db.Column(db.Integer, db.ForeignKey('bands.id_band'), nullable=False)
    band = db.relationship('Bands', backref='members')

    instrument_type = db.Column(db.String, db.ForeignKey('instruments.type'), nullable=False)
    instrument = db.relationship('Instruments', backref='players')

    name = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=True)


class Places(db.Model):
    __tablename__ = 'places'

    id_place = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)


class Concerts(db.Model):
    __tablename__ = 'concerts'

    id_band = db.Column(db.Integer, db.ForeignKey('bands.id_band'), nullable=False)
    band = db.relationship("Bands", backref='concerts')

    id_place = db.Column(db.Integer, db.ForeignKey('places.id_place'), nullable=False)
    place = db.relationship("Places", backref='concerts')

    concert_date = db.Column(db.Date, nullable=False)
    tour = db.Column(db.String, nullable=True)

    db.PrimaryKeyConstraint(id_band, id_place, concert_date)


class Festivals(db.Model):
    __tablename__ = 'festivals'

    id_festival = db.Column(db.Integer, primary_key=True)
    id_place = db.Column(db.Integer, db.ForeignKey('places.id_place'), nullable=False)
    localization = db.relationship('Places', backref='festivals')

    name = db.Column(db.String, nullable=False)
    date_start = db.Column(db.Date, nullable=True)
    date_end = db.Column(db.Date, nullable=True)


class Appearances(db.Model):
    __tablename__ = 'appearances'

    id_festival = db.Column(db.Integer, db.ForeignKey('festivals.id_festival'))
    id_band = db.Column(db.Integer, db.ForeignKey('bands.id_band'))
    db.PrimaryKeyConstraint(id_festival, id_band)


class Genres(db.Model):
    __tablename__ = 'genres'

    name = db.Column(db.String, primary_key=True)
    supergenre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
    supergenre = db.relationship('Genres', backref='subgenres')


class Albums(db.Model):
    __tablename__ = 'albums'

    id_album = db.Column(db.Integer, primary_key=True)
    id_band = db.Column(db.Integer, db.ForeignKey('bands.id_band'), nullable=False)
    band = db.relationship('Bands', backref='albums')

    name = db.Column(db.String, nullable=False)

    genre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
    genre = db.relationship('Genres', backref='genre')


class Songs(db.Model):
    __tablename__ = 'songs'

    id_album = db.Column(db.Integer, db.ForeignKey('albums.id_album'), nullable=False)
    album = db.relationship('Albums', backref='songs')

    posisiton = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    length = db.Column(db.Integer, nullable=True)

    db.PrimaryKeyConstraint(id_album, posisiton)


class Awards(db.Model):
    __tablename__ = 'awards'

    id_award = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class AwardReceptions(db.Model):
    __tablename__ = 'award_receptions'

    id_album = db.Column(db.Integer, db.ForeignKey('albums.id_album'), nullable=False)
    album = db.relationship('Albums')
    id_award = db.Column(db.Integer, db.ForeignKey('awards.id_award'), nullable=False)
    award = db.relationship('Awards')

    db.PrimaryKeyConstraint(id_album, id_award)




