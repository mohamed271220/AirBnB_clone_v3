#!/usr/bin/python3
"""
Create a flask app that will serve the API, views module
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city_id(city_id):
    """
    Return places
    """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Return place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Delete place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    Create place
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if 'user_id' not in data:
        return abort(400, "Missing user_id")
    user_id = data['user_id']
    if storage.get(User, user_id) is None:
        return abort(404)
    if 'name' not in data:
        return abort(400, "Missing name")
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Update place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
