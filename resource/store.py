from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message':'store not found'},404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message':'store created'}
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error has occured when creating this store.'}, 500
        
        return store.json(), 201
            
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_to_db()
        else:
            return {"message":"Store doesn't exit."}
        return {'message':'Store deleted.'}

class StoreList(Resource):
    def get(self):
        # [item.json() for item in ItemModel.query.all()]
        return {'store': list(map(lambda x: x.json(), StoreModel.query.all()))} 