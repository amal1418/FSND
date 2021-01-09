from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(120))
    Show = db.relationship('Shows', backref='venue', lazy=True)

    def __repr__(self):
	    return f'<Venue ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, website: {self.website}, seeking_talent: {self.seeking_talent}, seeking_description: {self.seeking_description}, Show: {self.Show}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate $$$$$-+-+-+-DONE-+-+-+-$$$$$

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(120))
    Show = db.relationship('Shows', backref='artist', lazy=True)

    def __repr__(self):
	    return f'<Artist ID: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, website: {self.website}, seeking_venue: {self.seeking_venue}, seeking_description: {self.seeking_description}, Show: {self.Show}>'


class Shows(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    start_time = db.Column(db.DateTime())
    
    def __repr__(self):
	    return f'<Shows ID: {self.id}, start_time: {self.start_time}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate $$$$$-+-+-+-DONE-+-+-+-$$$$$

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. $$$$$-+-+-+-DONE-+-+-+-$$$$$
