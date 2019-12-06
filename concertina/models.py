from concertina.configs import db


class Bands(db.Model):
    __tablename__ = 'bands'

    name = db.Column(db.String, primary_key=True)
    formation_date = db.Column(db.Date, nullable=True)
    members = db.relationship('Musicians', backref='band')
    concerts = db.relationship('Concerts', backref='performer')
    # festivals = db.relationship('Festivals', secondary=appearances)

    @staticmethod
    def create(name, formation_date=None):
        band = Bands(name=name, formation_date=formation_date)
        db.session.add(band)
        db.session.commit()
        return band

    def play_concert(self, place, date):
        return Concerts.create(self, place, date)

    def play_on_festival(self, festival):
        return True


class Instruments(db.Model):
    __tablename__ = 'instruments'

    type = db.Column(db.String, primary_key=True)
    players = db.relationship('Musicians', backref='instrument')

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

    nationality = db.Column(db.String, nullable=True)

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
    def create(name, city, address):
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

# TODO everything below

# class Appearances(db.Model):
#     __tablename__ = 'appearances'
#
#     festival_name = db.Column(db.String)
#     festival_date = db.Column(db.Date)
#     band_name = db.Column(db.Integer, db.ForeignKey('bands.name'))
#
#     db.ForeignKeyConstraint(['festival_name', 'festival_date'], ['festivals.name', 'festivals.date_start'])
#
#
# class Genres(db.Model):
#     __tablename__ = 'genres'
#
#     name = db.Column(db.String, primary_key=True)
#     supergenre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
#     supergenre = db.relationship('Genres', backref='subgenres')
#
#
# class Albums(db.Model):
#     __tablename__ = 'albums'
#
#     band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
#     band = db.relationship('Bands', backref='albums')
#
#     name = db.Column(db.String, nullable=False)
#
#     genre_name = db.Column(db.String, db.ForeignKey('genres.name'), nullable=True)
#     genre = db.relationship('Genres', backref='genre')
#
#     db.PrimaryKeyConstraint(band_name, name)
#
#
# class Songs(db.Model):
#     __tablename__ = 'songs'
#
#     album_name = db.Column(db.String, db.ForeignKey('albums.name'), nullable=False)
#     album = db.relationship('Albums', backref='songs')
#
#     band_name = db.Column(db.String, db.ForeignKey('bands.name'), nullable=False)
#     band = db.relationship('Bands')
#
#     posisiton = db.Column(db.Integer, nullable=False)
#     name = db.Column(db.String, nullable=False)
#
#     db.PrimaryKeyConstraint(band_name, album_name, posisiton)
#
#
# class Awards(db.Model):
#     __tablename__ = 'awards'
#
#     name = db.Column(db.String, primary_key=True)
#
#
# class AwardReceptions(db.Model):
#     __tablename__ = 'award_receptions'
#
#
#     # TODO MANY TO MANY?
#     album_name = db.Column(db.String, db.ForeignKey('albums.name'), nullable=False)
#     album = db.relationship('Albums')
#     award_name = db.Column(db.String, db.ForeignKey('awards.name'), nullable=False)
#     award = db.relationship('Awards')
#
#     db.PrimaryKeyConstraint(album_name, award_name)




