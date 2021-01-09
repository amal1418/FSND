#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import (
Flask,
render_template,
request,
Response,
flash,
redirect,
url_for,
jsonify
)
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form 
import logging
from logging import Formatter, FileHandler
from forms import *
import sys
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)



# TODO: connect to a local postgresql database $$$$$-+-+-+-DONE-+-+-+-$$$$$

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. $$$$$-+-+-+-DONE-+-+-+-$$$$$
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  date= datetime.now()
  cityAndState =  Venue.query.distinct(Venue.city, Venue.state).all()  
  for cityState in cityAndState:
    venue_info = []
    venues = Venue.query.filter_by(city=cityState.city).filter_by(state=cityState.state).all()
    for venue in venues:
      showsCount = Shows.query.filter(Venue.id==Venue.id).filter(Shows.start_time > date).all()
      upcomingShows =  len(showsCount)
      venue_info.append({
      "id" : venue.id,
      "name" : venue.name,
      "num_upcoming_shows" : upcomingShows
      })
    data.append({
      "city": cityState.city,
      "state": cityState.state,
      "venues": venue_info
    })  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  date= datetime.now()
  search_term = request.form.get('search_term', '')
  search = '%{}%'.format(search_term)
  venues = Venue.query.filter(Venue.name.ilike(search)).all()
  venue_info = []
  response = []
  for venue in venues:
    showsCount = Shows.query.filter(Venue.id==Venue.id).filter(Shows.start_time > date).all()
    upcomingShows =  len(showsCount)
    venue_info.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcomingShows
    })
  
  response={
    "count": len(venues),
    "data": venue_info
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id 
  # TODO: replace with real venue data from the venues table, using venue_id $$$$$-+-+-+-DONE-+-+-+-$$$$$
  date= datetime.now()
  venue = Venue.query.get(venue_id)
  shows = Shows.query.join(Artist).filter(Shows.venue_id == venue_id)
  pastShows_info = []
  upcomingShows_info = []
  data =[]
  for show in shows :
    show_info={
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time)), 
    }
    if show.start_time < date:
      pastShows_info.append(show_info) 
    else:
      upcomingShows_info.append(show_info)
  
  data={
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": pastShows_info,
        "upcoming_shows": upcomingShows_info,
        "past_shows_count": len(pastShows_info),
        "upcoming_shows_count": len(upcomingShows_info)
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # TODO: modify data to be the data object returned from db insertion 
  form = VenueForm(request.form)
  venue = Venue()
  error = False
 
  try:
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.address = form.address.data
    venue.genres = form.genres.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except: 
    error = True 
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name']  + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
 
  # TODO: on unsuccessful db insert, flash an error instead. $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + ' was successfully deleted!')
    return redirect('/venues')
  except():
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + ' could not be delete.')
  finally: 
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database $$$$$-+-+-+-DONE-+-+-+-$$$$$
  data= []
  artists = Artist.query.with_entities(Artist.id, Artist.name).all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  date= datetime.now()
  search_term = request.form.get('search_term', '')
  search = '%{}%'.format(search_term)
  artists = Artist.query.filter(Artist.name.ilike(search)).all()
  artist_info = []
  response= []
  for artist in artists:
    showsCount = Shows.query.filter(Venue.id==Venue.id).filter(Shows.start_time > date).all()
    upcomingShows =  len(showsCount)
    artist_info.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": upcomingShows
    })
  response={
    "count": len(artists),
    "data": artist_info
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id $$$$$-+-+-+-DONE-+-+-+-$$$$$
  date= datetime.now()
  artist = Artist.query.get(artist_id)
  shows = Shows.query.join(Venue).filter(Shows.artist_id == artist_id)
  pastShows_info = []
  upcomingShows_info = []
  data =[]
  for show in shows :
    show_info={
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": format_datetime(str(show.start_time)), 
    }
    if show.start_time < date:
      pastShows_info.append(show_info) 
    else:
      upcomingShows_info.append(show_info)
  
  data={
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": pastShows_info,
        "upcoming_shows": upcomingShows_info,
        "past_shows_count": len(pastShows_info),
        "upcoming_shows_count": len(upcomingShows_info)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist = {
        "id": artist_id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
  }
  # TODO: populate form with fields from artist with ID <artist_id> $$$$$-+-+-+-DONE-+-+-+-$$$$$
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing  $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  artist = Artist()
  error = False

  try:
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website.data
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except: 
    error = True 
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name']  + ' could not be update.')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue = {
        "id": venue_id,
        "name": venue.name,
        "genres": venue.genres,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
  }
  # TODO: populate form with values from venue with ID <venue_id> $$$$$-+-+-+-DONE-+-+-+-$$$$$
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  venue = Venue()
  error = False

  try:
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.address = form.address.data
    venue.genres = form.genres.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except: 
    error = True 
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name']  + ' could not be update.')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  artist = Artist()
  error = False

  try:
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website.data
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except: 
    error = True 
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name']  + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead. $$$$$-+-+-+-DONE-+-+-+-$$$$$
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. $$$$$-+-+-+-DONE-+-+-+-$$$$$
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data= []
  shows = Shows.query.join(Venue).join(Artist).all()
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": format_datetime(str(show.start_time)), 
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead $$$$$-+-+-+-DONE-+-+-+-$$$$$
  error = False
  venue_id = request.form['venue_id']
  artist_id = request.form['artist_id'] 
  start_time = request.form['start_time']
  try:
    shows= Shows(
    venue_id=venue_id,
    artist_id=artist_id,
    start_time=start_time
    )
    db.session.add(shows)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
