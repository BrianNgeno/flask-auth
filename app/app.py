#!/usr/bin/env python3
import os
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, House
from flask_cors import CORS
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True
migrate = Migrate(app, db,render_as_batch=True)

db.init_app(app)
api = Api(app)
CORS(app)



class Index(Resource):
    def get(self):
        response_body = '<h1>Hello World</h1>'
        status = 200
        headers = {}
        return make_response(response_body,status,headers)
    

class Signup(Resource):
    def post(self):
        name = request.get_json().get('name')
        password = request.get_json().get('password')

        if name and password:
            new_user = User(name=name)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session['user_id']=new_user.id
            return new_user.to_dict(),201

class Users(Resource):
    def get(self):
        users = []
        for user in User.query.all():
            user_dict={
                "name":user.name,
            }
            users.append(user_dict)
        response= make_response(
                jsonify(users),
                200
                )
        return response
    
    def post(self):
        new_user = User(
            name=request.form.get("name"),
        )

        db.session.add(new_user)
        db.session.commit()

        user_dict = new_user.to_dict()

        response = make_response(
            jsonify(user_dict),
            201
        )

        return response



class UserById(Resource):
    def get(self,id):
        user = User.query.filter_by(id=id).first()
        user_dict = user.to_dict()
        response = make_response(
        jsonify(user_dict),
        200
        )
        response.headers["Content-Type"]= "application/json"
        return response
        
    def patch(self,id):
        user = User.query.filter_by(id=id).first()

        for attr in request.form:
            setattr(user, attr, request.form.get(attr))

        db.session.add(user)
        db.session.commit()

        user_dict = user.to_dict()

        response = make_response(
            jsonify(user_dict),
            200
        )

        return response

    def delete(self,id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

        response_dict = {
            "delete_successful": True,
            "message": "User deleted."    
        }

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response




@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found:The requested resource does not exist",
        404
        )
    return response

api.add_resource(Index,'/', endpoint='landing')
api.add_resource(Users, '/users', endpoint='user')
api.add_resource(UserById,'/users/<int:id>', endpoint ='user_id')

if __name__ == '__main__':
    app.run(port=5000)