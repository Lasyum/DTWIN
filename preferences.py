from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Preference
from .. import db

bp = Blueprint('preferences', __name__, url_prefix='/preferences')

@bp.route('', methods=['GET'])
@jwt_required()
def get_preferences():
    user_id = get_jwt_identity()
    preferences = Preference.query.filter_by(user_id=user_id).all()
    return jsonify({pref.key: pref.value for pref in preferences}), 200

@bp.route('', methods=['POST'])
@jwt_required()
def set_preference():
    user_id = get_jwt_identity()
    data = request.get_json()
    for key, value in data.items():
        pref = Preference.query.filter_by(user_id=user_id, key=key).first()
        if pref:
            pref.value = value
        else:
            pref = Preference(key=key, value=value, user_id=user_id)
            db.session.add(pref)
    db.session.commit()
    return jsonify({"msg": "Preferences updated"}), 200