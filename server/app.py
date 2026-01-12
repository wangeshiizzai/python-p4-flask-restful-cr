#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        response = make_response(
            {"message": "Welcome to the Newsletter RESTful API"},
            200
        )
        return response


api.add_resource(Home, '/')


class Newsletters(Resource):
    def get(self):
        newsletters = [n.to_dict() for n in Newsletter.query.all()]
        response = make_response(newsletters, 200)
        return response

    def post(self):
        new_newsletter = Newsletter(
            title=request.form['title'],
            body=request.form['body']
        )

        db.session.add(new_newsletter)
        db.session.commit()

        response = make_response(
            new_newsletter.to_dict(),
            201
        )
        return response


api.add_resource(Newsletters, '/newsletters')


class NewsletterByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()

        response = make_response(
            newsletter.to_dict(),
            200
        )
        return response


api.add_resource(NewsletterByID, '/newsletters/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
