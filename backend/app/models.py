from . import db

class User(db.Model):
    __tablename__ = 'user' 
    
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.Text)
    email = db.Column(db.Text)
    image_url = db.Column(db.Text)
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    token_expiry = db.Column(db.DateTime)
    last_scraped = db.Column(db.DateTime)

class TrackCache(db.Model):
    __tablename__ = 'track_cache'
    
    spotify_uri = db.Column(db.String(255), primary_key=True)
    mbid = db.Column(db.String(255))
    title = db.Column(db.Text)
    artist = db.Column(db.Text)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    bpm = db.Column(db.Integer)
    mood_tags = db.Column(db.Text)