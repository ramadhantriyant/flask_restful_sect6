from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': f"Store {name} doesn't exists!"}

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"Store {name} is already exists!"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred when inserting the store"}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        if StoreModel.find_by_name(name):
            store = StoreModel(name)
            try:
                store.delete_from_db()
            except:
                return {'message': "An error occurred when deleting the store"}, 500
            return {'message': f"Store {name} deleted!"}, 201

        return {'message': f"Store {name} doesn't exists!"}, 404

class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}
