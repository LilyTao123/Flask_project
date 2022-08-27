from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt  import JWT

from security import authenticate, identity
from resource.user import UserRegister
from resource.item import Item, ItemList
from resource.store import Store, StoreList
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Turn off flask_sqlalchemy modification track, but sqlalchemy itself still works
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'll'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList,'/stores')

api.add_resource(UserRegister,'/register')



if __name__ =='__main__':
    db.init_app(app)
    app.run(port=5000, debug =True)