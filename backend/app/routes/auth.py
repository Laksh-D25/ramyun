from flask import Blueprint, request, redirect, session, jsonify, url_for, current_app
from spotipy.oauth2 import SpotifyOAuth
from ..models import User, db
from datetime import datetime, timedelta
import time

auth_bp = Blueprint('auth', __name__)

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIPY_REDIRECT_URI'],
        scope = "user-read-private user-read-email user-top-read user-read-recently-played playlist-modify-public playlist-modify-private"
    )

@auth_bp.route('/login')
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    sp_oauth = get_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    if not token_info:
        return jsonify({'error': 'Failed to get access token'}), 400
    
    import spotipy
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    
    user = User.query.filter_by(spotify_id=user_info['id']).first()
    if not user:
        user = User(spotify_id=user_info['id'])
        db.session.add(user)
    images = user_info.get('images', [])
    user.display_name = user_info.get('display_name', '')
    user.image_url = images[0]['url'] if images else ''
    user.access_token = token_info['access_token']
    user.refresh_token = token_info['refresh_token']
    user.token_expiry = datetime.fromtimestamp(token_info['expires_at'])
    
    db.session.commit()
    
    session['user_id'] = user.id
    return redirect(url_for('api.status'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return "Logged out", 200