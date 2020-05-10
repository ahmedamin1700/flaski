from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import Item


class ItemResource(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = ItemResource.parser.parse_args()

        item = Item(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred while inserting the item.'}, 500

        return item.json()

    @jwt_required()
    def delete(self, name):
        item = Item.find_by_name(name)

        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item does not exist.'}, 404

    @jwt_required()
    def put(self, name):
        data = ItemResource.parser.parse_args()
        item = Item.find_by_name(name)

        if item is None:
            item = Item(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemListResource(Resource):
    TABLE_NAME = 'items'

    def get(self):
        # return {'items': [item.json() for item in Item.query.all()]}
        return {'items': list(map(lambda x: x.json(), Item.query.all()))}