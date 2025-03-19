#!/usr/bin/env python

from flask import Flask, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

pets = {}
birds = {}

@api.route('/pets/<name>')
@api.doc(params={'name': 'Name of the pet'})
class Pets(Resource):
    def get(self, name):
        if name not in pets:
            return {'message': 'Pet not found'}
        return {name: pets[name]}

    def put(self, name):
        pets[name] = request.json
        return {name: pets[name]}

    def delete(self, name):
        if name not in pets:
            return {'success': False}
        del pets[name]
        return {'success': True}

    def post(self, name):
        pet_new_name = name
        if name in pets:
            n = 1
            while pet_new_name in pets:
                pet_new_name = f'{name}{n}'
                n = n + 1
        pets[pet_new_name] = request.json
        return {pet_new_name: pets[pet_new_name]}


def validate_bird_data(data):
    if 'name' not in data:
        return {'error': 'no name provided'}
    if 'species' not in data:
        return {'error': 'no species provided'}
    if 'color' not in data:
        return {'error': 'no color provided'}
    return ""

@api.route('/birds/<name>')
@api.doc(params={'name': 'Name of the bird'})
class Birds(Resource):
    def get(self, name):
        if name == "":
            return birds
        if name not in pets:
            return {'message': 'Bird not found'}
        return {name: birds[name]}

    def put(self, name):
        validation = validate_bird_data(request.json)
        if validation != "":
            return validation
        birds[name] = request.json
        return {name: birds[name]}

    def delete(self, name):
        if name not in birds:
            return {'success': False}
        del birds[name]
        return {'success': True}

    def post(self, name):
        validation = validate_bird_data(request.json)
        if validation != "":
            return validation
        bird_new_name = name
        if name in birds:
            n = 1
            while bird_new_name in birds:
                bird_new_name = f'{name}{n}'
                n = n + 1
        birds[bird_new_name] = request.json
        return {bird_new_name: birds[bird_new_name]}

if __name__ == '__main__':
    app.run(debug=True)
