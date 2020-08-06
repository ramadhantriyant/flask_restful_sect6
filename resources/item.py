from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every item needs store id!"
    )

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': "An error occured when retrieving the item"}, 500

        if item:
            return item.json()
        return {'message': "Item not found!"}, 404

    @jwt_required()
    def post(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': "An error occured when retrieving the item"}, 500

        if item:
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': "An error occured when inserting the item"}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': "An error occured when retrieving the item"}, 500

        if not item:
            return {'message': f"An item with name '{name}' does not exists."}, 400

        try:
            item.delete_from_db()
        except:
            return {'message': "An error occured when deleting the item"}, 500

        return {'message': "Item deleted"}, 201

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
            try:
                item.save_to_db()
            except:
                return {'message': "An error occured when saving the item"}, 500
        else:
            item = ItemModel(name, data['price'], data['store_id'])
            try:
                item.save_to_db()
            except:
                return {'message': "An error occured when saving the item"}, 500

        return item.json(), 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
