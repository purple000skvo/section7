from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item doesn't exist"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"Item with name: {name} already exists"}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting item into db."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": 'Item Deleted'}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            try:
                item = ItemModel(name, **request_data)
            except:
                return {"message": "An error occured inserting the item"}, 500
        else:
            try:
                item.price = request_data['price']
                item.store_id = request_data['store_id']
            except Exception as e:
                return {"message": "An error occured updating the item"}, 500
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
