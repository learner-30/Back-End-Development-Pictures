from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
        
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for d in data:
        if d['id'] == id:
            return jsonify(d), 200
    
    return {'message':'URL was not found'}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json

    if not picture:
        return {"message": "Invalid input parameter"}, 422
    
    for d in data:
        if d['id'] == picture['id']:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
    
    data.append(picture)
    return picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json

    if not picture:
        return {"message": "Invalid input parameter"}, 422
    
    for d in data:
        if d['id'] == picture['id']:
            d['id'] = picture['id']
            d['pic_url'] = picture['pic_url']
            d['event_country'] = picture['event_country']
            d['event_state'] = picture['event_state']
            d['event_city'] = picture['event_city']
            d['event_date'] = picture['event_date']
            return picture, 200

    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for d in data:
        if d['id'] == id:
            data.remove(d)
            return {}, 204
    
    return {"message": "picture not found"}, 404
