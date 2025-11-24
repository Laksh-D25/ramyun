from flask import Blueprint, request, session, jsonify, redirect, url_for
from ..models import User, db
import spotipy
from datetime import datetime
from .auth import get_spotify_oauth

api_bp = Blueprint('api', __name__)

def get_valid_token(user_id):
    user = db.session.get(User, user_id)
    if user.token_expiry < datetime.now():
        sp_oauth = get_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(user.refresh_token)
        
        user.access_token = token_info['access_token']
        user.token_expiry = datetime.fromtimestamp(token_info['expires_at'])
        
        db.session.commit()
        
    return user.access_token

@api_bp.route('/status', methods=['GET'])
def status():
    return {'status': 'ok'}, 200

@api_bp.route('/user/', methods=['GET'])
def show_user_data():
    if not session:
        return jsonify({'error': 'Login. http://127.0.0.1:5000/api/auth/login'}), 500
    user = db.session.execute(db.select(User).filter_by(id=session['user_id'])).scalar_one()
    response_data = {
        'id': user.id,
        'spotify_id': user.spotify_id,
        'display_name': user.display_name,
        'image_url': user.image_url,
        'last_scraped': user.last_scraped.isoformat() if user.last_scraped else None
    }
    return response_data, 200

@api_bp.route('/get-followed-playlist/', methods=['GET'])
def get_followed_playlists():
    if not session:
        return jsonify({'error': 'Login. http://127.0.0.1:5000/api/auth/login'}), 500
    user_spotify_id = db.session.execute(db.select(User.spotify_id).filter_by(id=session['user_id'])).scalar_one()
    try:
        sp = spotipy.Spotify(auth=get_valid_token(session['user_id']))
        playlists = sp.current_user_playlists()
        return jsonify(playlists), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/get-recently-played/', methods=['GET'])
def get_recently_played():
    if not session:
        return jsonify({'error': 'Login. http://127.0.0.1:5000/api/auth/login'}), 500
    try:
        sp = spotipy.Spotify(auth=get_valid_token(session['user_id']))
        recents = sp.current_user_recently_played()
        return jsonify(recents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/get-top-tracks/', methods=['GET'])
def get_top_tracks():
    if not session:
        return jsonify({'error': 'Login. http://127.0.0.1:5000/api/auth/login'}), 500
    try:
        sp = spotipy.Spotify(auth=get_valid_token(session['user_id']))
        top = sp.current_user_top_tracks()
        return jsonify(top), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500