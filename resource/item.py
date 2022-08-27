import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt  import JWT, jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                type= float,
                required = True,
                help = 'This field cannot be left blank!'
                )

    parser.add_argument('store_id',
                type= int,
                required = True,
                help = 'Every item needs a store id!'
                )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exit.".format(name)}, 400
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'},500 # internal serving error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_to_db()
            return {'message':'Item has been deleted'}
        else:
            pass 

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        # [item.json() for item in ItemModel.query.all()]
        return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))} 